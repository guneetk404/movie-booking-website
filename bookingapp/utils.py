from django.core.mail import EmailMultiAlternatives
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse


def emailsending(email, subject, message):
    msg = EmailMultiAlternatives(subject=subject, from_email="MegaCinema255@gmail.com", to=[email], body=message)
    msg.send()
    return 0


def send_password_reset_link(request,user):
    token = RefreshToken.for_user(user).access_token
    print(token)
    current_site = get_current_site(request).domain
    relativeLink = '/changepassword/'
    absurl = 'http://'+current_site+relativeLink+'?token='+str(token)
    email_body = 'Hi '+user.first_name+',\n\n'+'Please set your new password by clicking on the link below:\n\n'+absurl+'\n\n'+'Thank you.'
    emailsending(user.email,'Password Reset',email_body)
    return True