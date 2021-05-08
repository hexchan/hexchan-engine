from django.conf import settings


def admin_email(request):
    emails = [email for name, email in settings.ADMINS]
    email = emails[0] if emails else None
    email_user, email_host = email.split('@')
    return {
        'admin_email': email,
        'admin_email_user': email_user,
        'admin_email_host': email_host,
    }
