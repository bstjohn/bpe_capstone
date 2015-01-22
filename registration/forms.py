from django import forms
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm

# Customize registration form
# 'required=true': field cannot empty
class MyRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    register_code = forms.CharField(required=True)

    # embedded class within the scope of the MyRegistrationForm class, to hold anything form the
    # form field, also can put any attribute in this class
    class Meta:
        model = User # whose the form is
        fields = ('register_code',
                  'username', 
                  'password1', 
                  'password2', 
                  'email', 
                  'first_name', 
                  'last_name')

        def save(self, commit=True):
	    user = super(UserCreationForm, self).save(commit=False)
            user.email = self.cleaned_data['email'] # save email data into the cleaned data
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.register_code = self.cleaned_data['register_code']

            if commit: # if commit == true
	        user.save()

            return user
