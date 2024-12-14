from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Newsletter


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'send_newsletter_action')

    def send_newsletter_action(self, obj):
        return format_html('<a class="button" href="{}">Send</a>',
                           reverse('newsletter:admin_send_newsletter', args=[obj.id]))
    send_newsletter_action.short_description = 'Send Newsletter'
