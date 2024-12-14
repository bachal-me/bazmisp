from django.shortcuts import get_object_or_404, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib import messages
from .models import Newsletter
from django.http import HttpResponse
from django.contrib.auth.models import User


def send_newsletter(request, newsletter_id):
    newsletter = get_object_or_404(Newsletter, id=newsletter_id)
    subscribers = User.objects.filter(is_active=True)

    subject = newsletter.title
    html_content = render_to_string('newsletter/email_template.html', {'newsletter': newsletter})

    for subscriber in subscribers:
        send_mail(
            subject=subject,
            message='',  # leave plain-text message empty if not needed
            from_email=settings.EMAIL_FROM_USER,
            recipient_list=[subscriber.email],
            html_message=html_content  # this sets the HTML content
        )

    messages.success(request, "Newsletter sent to all active subscribers.")
    return redirect('/admin/newsletter/newsletter/')