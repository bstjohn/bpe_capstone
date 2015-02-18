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
from registration.forms import MyRegistrationForm           # import from /forms.py
from django.contrib.auth.models import User
from registration.forms import PersonForm

from django.contrib.auth.decorators import login_required
from forms import UserProfileForm

from django.views.generic import ListView, DetailView
from django.contrib.auth import get_user_model
from models import UserProfile

def register_user(request):
    # look at request object, look if there is an post using request.method
    if request.method == 'POST':
        form = MyRegistrationForm(request.POST) # pass the value using MyRegistrationForm to form object
        
        # check if the info is correct!!
        if form.is_valid():
            save_it = form.save(commit=False)
            save_it.save()
            form = PersonForm(request.POST)
            save_it = form.save(commit=False)
            save_it.save()
            # Email to user for verfiy!!!!
            subject = 'Thank you for register as BPA user from BPA project'
            message = 'Hi ' + save_it.username + ', welcome to use BPA web applictation, we hope you enjoy it!'
            from_email = settings.EMAIL_HOST_USER
            to_list = [save_it.email, settings.EMAIL_HOST_USER]

            send_mail(subject, message, from_email, to_list, fail_silently=False)
            # message.success(request, 'Thanks you for regist BPA user, the email comfirmation sent')
            return HttpResponseRedirect('/registration_success/')
        else:
            return HttpResponseRedirect('/registration_fail/')

    # for security check
    args = {} 
    args.update(csrf(request)) 

    args['form'] = MyRegistrationForm() # put the empty form
    print args

    return render_to_response('registration/register.html', args)

# This is easy way to render to response certain template.
def register_success(request):
    #{'username': request.POST.get('username','')}
    return render_to_response('registration/register_success.html')

""" or we can do in this way
def register_success(request):
    t = get_template('registration/register_success.html')
    html = t.render(Context({'name':name}))
    return HttpResponse(html)
"""

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















