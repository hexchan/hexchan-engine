# Standard library imports
from io import BytesIO

# Django imports
from django.shortcuts import redirect, render
from django.contrib.auth import get_user
from django.db import transaction
from django.db.models import F
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.core.files.base import ContentFile
from django.views.generic import FormView

# Third party imports
import PIL.Image

# App imports
from hexchan import config

from imageboard.models import Board, Thread, Post, Image, Captcha
from imageboard.forms import PostingForm
from imageboard.views.parts import push_to_session_list
from imageboard.wakabamark import extract_refs
from imageboard.utils.get_client_ip import get_client_ip


class PostingView(FormView):
    form_class = PostingForm

    @csrf_exempt
    @transaction.atomic
    def dispatch(self, *args, **kwargs):
        return super(PostingView, self).dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(PostingView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        with transaction.atomic():
            # Get form type
            form_type = form.cleaned_data['form_type']

            # Get board
            board_id = form.cleaned_data['board_id']
            board = Board.objects.select_for_update().get(id=board_id, is_deleted=False)

            # Bump board's post HID counter
            board.last_post_hid = (F('last_post_hid') + 1) if board.last_post_hid is not None else 0
            board.save()
            board.refresh_from_db()

            # TODO: Merge new thread and reply code routes
            if form_type == 'new_thread':
                thread = self.create_thread(self.request, board)
                post = self.create_post(self.request, board, thread, form.cleaned_data, is_op=True)
                self.create_images(post, form.cleaned_data['images'])
                self.create_refs(self.request, board, thread, post)
                thread.op = post
                thread.save()
                self.flush_old_threads(self.request, board)
                push_to_session_list(self.request, 'user_posts', post.id)
                push_to_session_list(self.request, 'user_threads', thread.id)
                self.delete_used_captcha(self.request, board)
            else:
                thread_id = form.cleaned_data['thread_id']
                thread = Thread.objects.select_for_update().get(id=thread_id, is_deleted=False)
                post = self.create_post(self.request, board, thread, form.cleaned_data)
                self.create_images(post, form.cleaned_data['images'])
                self.create_refs(self.request, board, thread, post)

                # TODO: move this logic to the thread model
                # Close thread if post limit is reached
                if thread.posts.count() >= thread.max_posts_num:
                    thread.is_locked = True

                thread.save()
                push_to_session_list(self.request, 'user_posts', post.id)
                push_to_session_list(self.request, 'user_thread_replies', thread.id)
                self.delete_used_captcha(self.request, board, thread)

            # Write latest posting time to the session
            self.request.session['latest_post_at'] = timezone.now().timestamp()

        # Redirect to the current thread
        # TODO: make a form checkbox for selecting destination - board or thread
        return redirect('thread_page', board_hid=board.hid, thread_hid=thread.hid)

    def form_invalid(self, form):
        # TODO: delete used captcha on failed validations?

        return render(
            self.request,
            'imageboard/posting_error_page.html',
            context={'form': form},
            status=403
        )

    def create_images(self, post: Post, images) -> None:
        """Save all images in request."""
        for image_file in images:
            # Create Django image object
            image = Image.objects.create(
                post=post,
                original_name=image_file.name,
                mimetype=image_file.content_type,
                size=image_file.size,
                checksum=image_file.md5_checksum,
            )

            # Save image object to the database
            image.save()

            # Update with image
            image.file = image_file

            # TODO: move thumb generation logic into the Image model
            # Load image with PIL
            image_pil_object = PIL.Image.open(image_file)

            # Create thumbnail with PIL library
            # Convert image to RGBA format when needed (for example, if image has indexed pallette 8bit per pixel mode)
            thumbnail_pil_object = image_pil_object.convert('RGBA')
            thumbnail_pil_object.thumbnail(
                size=config.IMAGE_THUMB_SIZE,
                resample=PIL.Image.BICUBIC,
            )

            # Background image
            bg_pil_object = PIL.Image.new(
                mode='RGBA',
                size=thumbnail_pil_object.size,
                color=config.THUMB_ALPHA_COLOR
            )

            # Apply background
            thumbnail_pil_object = PIL.Image\
                .alpha_composite(
                    bg_pil_object,
                    thumbnail_pil_object
                )\
                .convert('RGB')

            # Save thumbnail to in-memory file as BytesIO
            thumb_file = BytesIO()
            thumbnail_pil_object.save(
                thumb_file,
                config.THUMB_TYPE,
                **config.THUMB_OPTIONS,
            )
            thumb_file.seek(0)

            # Set save=False, otherwise it will run in an infinite loop
            image.thumb_file.save(
                image.make_thumb_file_name(),
                ContentFile(thumb_file.read()),
                save=False
            )

            # Save everything
            image.save()

    def create_thread(self, request, board: Board) -> Thread:
        thread = Thread.objects.create(
            hid=board.last_post_hid,
            board=board,
            max_posts_num=board.default_max_posts_num,
        )
        return thread

    def create_post(self, request, board: Board, thread: Thread, cleaned_data: dict, is_op: bool = False) -> Post:
        post = Post.objects.create(
            hid=board.last_post_hid,
            thread=thread,

            text=cleaned_data['text'],
            title=cleaned_data['title'],
            author=cleaned_data['author'] if cleaned_data['author'] else board.default_username,

            is_op=is_op,

            created_by=get_user(request) if request.user.is_authenticated else None,

            ip_address=get_client_ip(request),
            session_id=request.session.session_key,
        )
        return post

    def create_refs(self, request, board, thread, post):
        # TODO: move to the Post model
        ref_ids = extract_refs(post.text)
        ref_posts = Post.objects.filter(thread__board=board, hid__in=ref_ids)
        post.refs.add(*ref_posts)

    def flush_old_threads(self, request, board):
        # TODO: move to the Thread model or signals
        if board.threads.count() > board.max_threads_num:
            old_threads = Thread.objects \
                .filter(board=board, is_deleted=False) \
                .order_by('board', '-is_sticky', '-hid')[board.max_threads_num:]

            for thread in old_threads:
                thread.is_locked = True
                thread.is_deleted = True
                thread.save()

    def delete_used_captcha(self, request, board, thread=None):
        ip_address = get_client_ip(request)

        Captcha.objects\
            .filter(
                board=board,
                thread=thread,
                ip_address=ip_address,
            )\
            .delete()
