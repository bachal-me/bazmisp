from django.urls import path
from .views import send_newsletter, subscribe_to_newsletter, unsubscribe

app_name = 'newsletter'

urlpatterns = [
    path('subscribe/', subscribe_to_newsletter, name='subscribe'),
    path('send/<int:newsletter_id>/', send_newsletter, name='admin_send_newsletter'),
    path('unsubscribe/<str:email>/', unsubscribe, name='unsubscribe'),
]
