from django import forms
from    .models import MyUser
from django.contrib.auth.models import User

class UserRegistrationForm(forms.ModelForm):
    class Meta:
        widgets = {
            'password': forms.PasswordInput(),
            'cnfpassword':forms.PasswordInput(),
        }
        model=MyUser
        fields=['firstName','lastName','email','password']
    
        

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model=MyUser
        fields = ['firstName','lastName',"email",]


class SignUpForm(forms.ModelForm):
    class Meta:
        model=MyUser
        fields='__all__'


class ForgotPasswordform(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['email']
    
class ResetPasswordForm(forms.ModelForm):
    new_password = forms.CharField(max_length=30)
    class Meta:
        model = MyUser
        fields = ['password']
    
    def clean(self):
        cleaned_data = super(ResetPasswordForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("new_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )

# class ForgotPasswordForm(forms.ModelForm):
#     class Meta:
#         model=MyUser
#         fields = '__all__'

