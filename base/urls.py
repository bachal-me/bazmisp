from django.urls import path
from .views import *

urlpatterns = [
   path("", home, name="home"),
   path("checkout", checkout_membership, name="checkout"),
   path("success/", payment_success, name="success"),
]