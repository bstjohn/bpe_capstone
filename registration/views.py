from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf
from django.template import Context, RequestContext, loader
from django.template.loader import get_template  # get_template fun
from django.views.generic.base import TemplateView  # how display template
from registration.forms import MyRegistrationForm  # import from /forms.py
from django.contrib.auth.models import User
from registration.forms import PersonForm


def register_user(request):
    if request.method == 'POST':
        form = MyRegistrationForm(request.POST)

        if form.is_valid():
            save_it = form.save(commit=False)
            save_it.save()
            form = PersonForm(request.POST)
            save_it = form.save(commit=False)
            save_it.save()
            # here we can add email to verfiy!!!!
            subject = 'Thank you for register as BPA user from BPA project'
            message = 'Hi ' + save_it.username + ', welcome to use BPA web applictation, we hope you enjoy it!'
            from_email = settings.EMAIL_HOST_USER
            to_list = [save_it.email, settings.EMAIL_HOST_USER]

            send_mail(subject, message, from_email, to_list, fail_silently=False)
            # message.success(request, 'Thanks you for regist BPA user, the email comfirmation sent')
            return HttpResponseRedirect('/registration_success/')
        else:
            return HttpResponseRedirect('/registration_fail/')

    args = {}
    args.update(csrf(request))

    args['form'] = MyRegistrationForm()
    print
    args

    return render_to_response('registration/register.html', args)


def register_success(request):
    return render_to_response('registration/register_success.html')


def register_fail(request):
    return render_to_response('registration/register_fail.html')

