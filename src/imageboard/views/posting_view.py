# Standard library imports
import os
import hashlib
import datetime
from io import BytesIO

# Django imports
from django.shortcuts import redirect, render
from django.conf import settings
from django.contrib.auth import get_user
from django.db import transaction, DatabaseError
from django.db.models import F, Subquery
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.core.files.base import ContentFile

# Third party imports
import PIL.Image
import bleach

# App imports
from hexchan import config

from imageboard.models import Board, Thread, Post, Image
from imageboard.forms import PostingForm
from imageboard.views.parts import push_to_session_list
from imageboard import exceptions as i_ex
from imageboard.wakabamark import extract_refs
from imageboard.utils import get_client_ip

from captcha.interface import check_captcha, set_captcha
from captcha import exceptions as c_ex

from moderation.interface import check_bans, check_text, check_image
from moderation import exceptions as m_ex


@csrf_exempt
@transaction.atomic
def posting_view(request):
    response = None

    # Check messsage contents and DB objects
    try:
        # Check request type
        if not request.POST:
            raise i_ex.BadRequestType

        # Check for bans
        check_bans(request)

        # Check posting limit
        check_posting_limit(request)

        # Get form data
        form = PostingForm(request.POST)
        if not form.is_valid():
            raise i_ex.FormValidationError(form.errors)

        # Check captcha
        check_captcha_for_request(request, form)

        # Get form type
        form_type = form.cleaned_data['form_type']

        # Get and check board object
        board_id = form.cleaned_data['board_id']
        board = get_board(board_id)

        #  If creating post in a thread - get and check that thread
        if form_type == 'new_post':
            # Get and check  thread
            thread_id = form.cleaned_data['thread_id']
            thread = get_thread(thread_id)
        else:
            thread = None

        # Get list of uploaded image objects
        images_and_checksums = get_images(request.FILES.getlist('images'))

        # Check message
        check_message_content(cleaned_data=form.cleaned_data, images=images_and_checksums)

    except (i_ex.ImageboardError, c_ex.CaptchaError, m_ex.ModerationError) as e:
        # Render error page if something went wrong
        response = render(request, 'imageboard/posting_error_page.html', context={'exception': e}, status=403)

    else:
        # Create thread, op post, save images, bump board's thread counter
        with transaction.atomic():
            # Bump board's post HID counter
            board.last_post_hid = (F('last_post_hid') + 1) if board.last_post_hid is not None else 0
            board.save()
            board.refresh_from_db()

            if form_type == 'new_thread':
                thread = create_thread(request, board)
                post = create_post(request, board, thread, form.cleaned_data, is_op=True)
                create_images(post, images_and_checksums)
                create_refs(request, board, thread, post)
                thread.op = post
                thread.save()
                flush_old_threads(request, board)
                push_to_session_list(request, 'user_posts', post.id)
                push_to_session_list(request, 'user_threads', thread.id)
            else:
                post = create_post(request, board, thread, form.cleaned_data)
                create_images(post, images_and_checksums)
                create_refs(request, board, thread, post)

                # Close thread if post limit is reached
                if thread.posts.count() >= thread.max_posts_num:
                    thread.is_locked = True

                thread.save()
                push_to_session_list(request, 'user_posts', post.id)
                push_to_session_list(request, 'user_thread_replies', thread.id)

            # Write latest posting time to the session
            request.session['latest_post_at'] = timezone.now().timestamp()

        # Redirect to the current thread
        # TODO: make a form checkbox for selecting destination - board or thread
        response = redirect('thread_page', board_hid=board.hid, thread_hid=thread.hid)

    finally:
        # Set new captcha on both failures and successes
        set_captcha(request)

    return response


def get_board(board_id: int) -> Board:
    """Get valid Board model object."""
    try:
        board = Board.objects.select_for_update().get(id=board_id, is_deleted=False)
    except Board.DoesNotExist:
        raise i_ex.BoardNotFound

    # Check board status
    if board.is_locked:
        raise i_ex.BoardIsLocked

    return board


def get_thread(thread_id: int) -> Thread:
    """Get valid Thread model object."""
    try:
        thread = Thread.objects.select_for_update().get(id=thread_id, is_deleted=False)
    except Thread.DoesNotExist:
        raise i_ex.ThreadNotFound

    # Check thread status
    if thread.is_locked:
        raise i_ex.ThreadIsLocked

    # Check thread posts num
    if thread.posts.count() >= thread.max_posts_num:
        raise i_ex.PostLimitWasReached

    return thread


def check_message_content(cleaned_data, images):
    # Check with wordfilters
    check_text(cleaned_data['text'])

    # Check honeypot. Yes, the email field is a honeypot!
    if len(cleaned_data['email']) > 0:
        raise i_ex.BadMessageContent

    # Check if empty message
    if not cleaned_data['text'] and not images:
        raise i_ex.MessageIsEmpty

    # TODO: remember to check password with regex when saving it


def get_images(raw_images):
    images_and_checksums = []

    # Check number of files
    if len(raw_images) > config.FILE_MAX_NUM:
        raise i_ex.TooManyFiles

    # Check file(s) for field 'file'
    for image_file in raw_images:
        if image_file.size > config.FILE_MAX_SIZE:
            raise i_ex.FileIsTooLarge

        if image_file.content_type not in config.FILE_MIME_TYPES:
            raise i_ex.BadFileType

        # Calculate checksum
        checksum_obj = hashlib.md5()
        for chunk in image_file.chunks(config.IMAGE_CHUNK_SIZE):
            checksum_obj.update(chunk)
        checksum = checksum_obj.hexdigest()

        # Look for banned images
        check_image(checksum, image_file.size)

        images_and_checksums.append((image_file, checksum,))

    return images_and_checksums


def create_images(post: Post, images_and_checksums) -> None:
    """Save all images in request."""
    for image_file, checksum in images_and_checksums:
        # Create Django image object
        image = Image(
            post=post,
            original_name=image_file.name,
            mimetype=image_file.content_type,
            size=image_file.size,
            checksum=checksum,
        )

        # Save image object to the database
        image.save()

        # Update with image
        image.file = image_file

        # Load image with PIL
        image_pil_object = PIL.Image.open(image_file)

        # Create thumbnail with PIL library
        # Convert image to RGBA format when needed (for example, if image has indexed pallette 8bit per pixel mode)
        thumbnail_pil_object = image_pil_object.convert('RGBA')
        thumbnail_pil_object.thumbnail(config.IMAGE_THUMB_SIZE, PIL.Image.ANTIALIAS)

        # Save thumbnail to in-memory file as BytesIO
        thumb_file = BytesIO()
        thumbnail_pil_object.save(thumb_file, config.THUMB_TYPE)
        thumb_file.seek(0)

        # Set save=False, otherwise it will run in an infinite loop
        image.thumb_file.save(
            image.make_thumb_file_name(),
            ContentFile(thumb_file.read()),
            save=False
        )

        # Save everything
        image.save()


def create_thread(request, board: Board) -> Thread:
    thread = Thread(
        hid=board.last_post_hid,
        board=board,
        max_posts_num=board.default_max_posts_num,
    )
    thread.save()
    return thread


def create_post(request, board: Board, thread: Thread, cleaned_data: dict, is_op: bool = False) -> Post:
    title = bleach.clean(cleaned_data['title'])
    author = bleach.clean(cleaned_data['author'])
    email = bleach.clean(cleaned_data['email'])
    text = bleach.clean(cleaned_data['text'])
    password = cleaned_data['password']

    post = Post(
        hid=board.last_post_hid,
        thread=thread,

        text=text,
        title=title,
        author=author if author else board.default_username,
        email=email,  # TODO: save emails
        password=password,  # TODO: save passwords

        is_op=is_op,

        created_by=get_user(request) if request.user.is_authenticated else None,

        ip_address=get_client_ip(request),
        session_id=request.session.session_key,
    )
    post.save()
    return post


def create_refs(request, board, thread, post):
    ref_ids = extract_refs(post.text)
    ref_posts = Post.objects.filter(thread__board=board, hid__in=ref_ids)
    post.refs.add(*ref_posts)


def check_captcha_for_request(request, form):
    captcha_data = form.cleaned_data['captcha']
    captcha_public_id = captcha_data.get('public_id')
    captcha_solution = captcha_data.get('solution')

    if request.user.is_authenticated:
        pass
    else:
        check_captcha(request, captcha_public_id, captcha_solution)


def flush_old_threads(request, board):
    if board.threads.count() > board.max_threads_num:
        old_threads = Thread.objects \
            .filter(board=board, is_deleted=False) \
            .order_by('board', '-is_sticky', '-hid')[board.max_threads_num:]

        for thread in old_threads:
            thread.is_locked = True
            thread.is_deleted = True
            thread.save()


def check_posting_limit(request):
    latest_post_at = request.session.get('latest_post_at')
    if latest_post_at:
        latest_post_at_datetime = datetime.datetime.fromtimestamp(latest_post_at, tz=timezone.utc)
        now = timezone.now()
        timeout = datetime.timedelta(seconds=config.POSTING_TIMEOUT)
        if (now - latest_post_at_datetime) < timeout:
            raise i_ex.NotSoFast
