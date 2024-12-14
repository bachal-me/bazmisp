from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from .forms import EmailLoginForm
from .models import Profile
from .utils import generate_token
from bazm.decorators import anonymous_required
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.core.mail import EmailMessage
from django.contrib import messages
import threading

class EmailThread(threading.Thread):
    
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)
        
    def run(self):
        return self.email.send()

def send_activation_email(user, request):
    current_site = get_current_site(request)
    email_subject = "Activate your account"
    email_body = render_to_string('users/activate.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user),
    })

    email = EmailMessage(subject=email_subject, body=email_body, from_email=settings.EMAIL_FROM_USER, to=[user.email])
    EmailThread(email).start()

@anonymous_required(redirect_url='home')
def signup_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # Ensure the profile is created
            Profile.objects.get_or_create(user=user)

            send_activation_email(user, request)
            messages.success(request, 'Signup successful! Check your mailbox to activate your account.')
            return redirect('login')

        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = UserRegistrationForm()
    return render(request, 'users/signup.html', {"form": form})

def logout_view(request):
    logout(request)
    return redirect("/")

@anonymous_required(redirect_url='home')
def login_view(request):
    if request.method == 'POST':
        form = EmailLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                account = Profile.objects.get(user=user)
                if account.is_verified:
                    login(request, user)
                    return redirect('home')
                else:
                    messages.error(request, "Check your email and verify your account to log in")
                    return render(request, 'users/login.html', {'form': form})               
            else:
                 messages.error(request, 'Invalid email or password')
    else:
        form = EmailLoginForm()
    return render(request, 'users/login.html', {'form': form})

def activate_user(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and generate_token.check_token(user, token):
        account = Profile.objects.get(user=user)
        account.is_verified = True
        account.save()
        print("Your account is activated, you can login now.")
        return redirect('login')
    else:
        return render(request, 'users/activate_failed.html', {"user": user})