# User registration view site.

# Bonneville Power Adminstration Front-End
# Copyright (C) 2015  Shu Ping Chu
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

# views.py is the set of functions that you implement it to describe how to 
# display the information of your website when we visit the url
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import render_to_response             # allows to render tmeplate back to browser
from django.http import HttpResponse                        # response to that http
from django.http import HttpResponseRedirect                # redirect browser to another url
from django.contrib import auth                             # take care using user login, logout, password
from django.core.context_processors import csrf             # for security protect
from django.template import Context, RequestContext, loader # for template language ex: "{{ }}" <--variable inside
from django.template.loader import get_template             # get_template helper function, to know where the templates are
from django.views.generic.base import TemplateView          # how display template
from registration.forms import MyRegistrationForm           # import from /forms.py
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from registration.forms import UserProfileForm
from django.views.generic import ListView, DetailView
from django.contrib.auth import get_user_model
from registration.models import UserProfile
from django.contrib.admin.views.decorators import staff_member_required

# User registration feature required only admin login
@staff_member_required
def register_user(request):
    if request.method == 'POST':
        form = MyRegistrationForm(request.POST)

        if form.is_valid():
            save_it = form.save(commit=False)
            save_it.save()
            messages.add_message(request, messages.SUCCESS, "New user " + save_it.username + " was created")
            # here we can add email to verfiy!!!!
            subject = 'Thank you for register as BPA user from BPA project'
            message = 'Hi ' + save_it.username + ', welcome to use BPA web applictation, we hope you enjoy it!'
            from_email = settings.EMAIL_HOST_USER
            to_list = [save_it.email, settings.EMAIL_HOST_USER]

            send_mail(subject, message, from_email, to_list, fail_silently=False)
            messages.success(request, 'Thanks you for regist BPA user, the email comfirmation sent')
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

# @login_required: This function will automatically at background check if user login, if not login
# it will redirectly the user to login page (force login)
# Edit user profile
@login_required 
def user_profile(request):
    if not request.user.is_authenticated():
        return HrttpResponseRedirect('/login/')
    if request.method == 'POST': # check if post
        form = UserProfileForm(request.POST, instance=request.user.profile) # take exist profile and fill-in to form
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/users/'+ request.user.username)
    else:
        user = request.user
        profile = user.profile # trigger django to create a user profile and populate
        form = UserProfileForm(instance=profile)

    args = {}
    args.update(csrf(request))
    
    args['form'] = form
    
    return render_to_response('registration/profile.html', args)


# Define a user profile detail view
class UserProfileDetailView(DetailView):
    model = get_user_model()
    slug_field = "username" # paramater "username" as key (aka: pk) for dynamic user url link
    template_name = "registration/user_detail.html"

    # always create user profile before retriving object
    def get_object(self, queryset=None):
        user = super(UserProfileDetailView, self).get_object(queryset)
        UserProfile.objects.get_or_create(user=user)
        return user

# logout user
def logout(request):
    auth.logout(request)
    return render_to_response('registration/logout.html')
