from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from allauth.account.forms import SignupForm
from django.core.mail import EmailMultiAlternatives


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="Email")

    class Meta:
        model = User
        fields = (
            "email",
            "password1",
            "password2",
        )

class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)

        subject = 'Welcome to our news portal!'
        text = f'{user.username}, you have successfully registered!'
        html = (
            f'<b>{user.username}</b>, you have successfully registered in '
            f'<a href="http://127.0.0.1:8000/news"></a>!'
        )
        msg = EmailMultiAlternatives(
            subject=subject, body=text, from_email=None, to=[user.email]
        )
        msg.attach_alternative(html, "text/html")
        msg.send()

        return user