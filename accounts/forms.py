from allauth.account.forms import SignupForm
from django import forms

class MyCustomSignupForm(SignupForm):
    phone_number = forms.CharField(max_length=10)


    def save(self, request):
        
        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(MyCustomSignupForm, self).save(request)

        # Add your own processing here.
        user.phone_number = self.cleaned_data['phone_number']
        user.save()

        # You must return the original result.
        return user