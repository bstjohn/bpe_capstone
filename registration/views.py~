from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse 
from django.http import HttpResponseRedirect 
from django.contrib import auth
from django.core.context_processors import csrf
from django.template import Context, RequestContext, loader
from django.template.loader import get_template    # get_template fun
from django.views.generic.base import TemplateView # how display template
from forms import MyRegistrationForm               # import from /forms.py

def register_user(request):

    if request.method == 'POST':
        form = MyRegistrationForm(request.POST)

        if form.is_valid():
	   form.save() # save the form
           # here we can add email to verfiy!!!!
           return HttpResponseRedirect('/registration_success/')
        else:
           return HttpResponseRedirect('/registration_fail/')

    args = {} 
    args.update(csrf(request))

    args['form'] = MyRegistrationForm()
    print args 

    return render_to_response('registration/register.html', args)

def register_success(request):
    return render_to_response('registration/register_success.html')

def register_success(request):
    return render_to_response('registration/register_fail.html')

#def registration(request):
#    return render(request, 'registration/registration.html')
