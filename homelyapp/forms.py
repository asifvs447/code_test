from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import UserProfiles, RentoutProperties
from django.forms import CharField, PasswordInput

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username','password','email']
        widgets = {
            'password': PasswordInput(),
        }

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfiles
        fields = ['account_type','phone']


class RentoutPropertyForm(ModelForm):
    class Meta:
        model = RentoutProperties
        fields = ['house_name','house_address']