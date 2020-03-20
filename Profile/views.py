from random import randint
from .models import *
from .forms import *

from django.conf import settings
from django.contrib import messages
from django.views.generic import View
from django.core.mail import send_mail
from django.shortcuts import render,redirect
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout
from django.contrib.sites.shortcuts import get_current_site


def HomeView(request):
    return render(request,'homepage.html')
#SIGNUP
class PostView(View):
    
    def get(self,request):
        form=UserRegistrationForm()
        return render(request,'signupnew.html',{'form':form})
    def post(self,request):
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(request.POST.get('password'))
            user.is_active=False
            user.save()
            user.otp_gen()
            current_site = get_current_site(request)
            subject='Activate Your Account Confirmation'
            to='python-trainee@mobiloitte.com'
            recv = user.email
            message = render_to_string('account_activate.html',
                                       {
                                           'user': user,
                                           'domain': current_site.domain,
                                           'id': user.uuid,
                                           'otp': user.otp,
                                       })

            send_mail(subject,message,to,[recv])
            print(message)
            return render(request, 'done.html')
        # return render (request,self.template_name)
        return render(request, 'signupnew.html', {'form':form})
# OTP/ACTIVATE
class Activate(View):
    template_name = 'otp.html'
    def get(self, request, uuid):
        try:
            user = MyUser.objects.get(uuid=uuid)
            return render(request, self.template_name,{'user':user})
        except (TypeError, ValueError, OverflowError,user.DoesNotExist):
            user=None
        if user is not None:
            user.is_active=True
            user.save()
            return render(request,self.template_name)
            return HttpResponse('The confirmation link was invalid, possibly because it has already been used.')
    def post(self,request,uuid):
        
        try:
            user = MyUser.objects.get(uuid=uuid)
        except Exception as e:
            message =""""USER NOT FOUND"""
            return render(request,'otp.html', {'message':message})
        if user.otp ==request.POST.get('otp'):
            user.is_otpverify=True
            user.is_active=True
            user.save()
            return redirect('/login')
        return HttpResponse('invalid otp')
#LOGIN

class UserProfile(View):
    def get(self, request):
        return render(request, 'loginnew.html')
    def post(self,request):

        username = request.POST.get('email')
        password = request.POST.get('password')
        print(">>>>>>>>>..", username, ">>>>>>>>>>>>>>", password)
        
        user = authenticate(email=username, password=password)
        print(">>>>>>>>>>>>>>.", user)
        user_details = {}
        
        if user:
            if user.is_active:
                user_details["uuid"] = user.uuid
                user_details["firstName"] = user.firstName  
                user_details['lastName'] = user.lastName
                user_details["email"] = user.email
                login(request,user)
                return render(request, 'show.html', user_details)
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details given")
  
        return render(request, 'loginnew.html', {})
  
       
#LOGOUT
@method_decorator(login_required, name='dispatch')
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/')

@method_decorator(login_required, name='dispatch')
class UpdateView(View):
    
    def get(self,request,uuid):
        user = MyUser.objects.get(uuid=uuid)
        print("User :  ", user)
        return render(request,'update.html',{'form':user})
    def post(self,request,uuid):
        form = UserUpdateForm
        instance=MyUser.objects.get(uuid=uuid)
        update_form=UserUpdateForm(request.POST or None,instance=instance)
        if update_form.is_valid():
            update_form.save()
            print("error",update_form.errors)
            return redirect('/login')
        return render(request,'update.html',{'form':form})
#DELETE
@method_decorator(login_required, name='dispatch')
class DestroyView(View):
    def get(self,request,uuid):
        form=MyUser.objects.get(uuid=uuid)
        form.delete()
        return redirect('/')


#FORGOT

def forgot_view(request):
    return render(request,'forgetnew.html')


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/login')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})

class ForgotPassword(View):
    def get(self, request):
        return render(request, 'forgotnew.html')

    def post(self, request):
        
        email = request.POST.get('email')
        try:
            user = MyUser.objects.get(email=email)
        
            if user is not None:
                current_site = get_current_site(request)
                form = ForgotPasswordform
                subject='Password Reset'
                from_email='python-trainee@mobiloitte.com'
                recv = user.email
                message =f"{current_site.domain}/reset_password/{user.uuid}"
                # message = render_to_string('forgot_password.html',
                #                        {
                #                            'user': user,
                #                            'domain': current_site.domain,
                #                            'id': user.uuid,
                                           
                #                        })

                send_mail(subject,message,from_email,[recv])
                print(message)
                return render(request,'forgotnew.html', {'form':form})
            
            return HttpResponse("invalid email")
        except:
            return HttpResponse("user not exist")

class ResetPassword(View):
    def get(self,request,uuid):
        user = MyUser.objects.get(uuid=uuid)
        print("User :  ", user.password)
        return render(request,'resetpassword.html',{'form':user})
    def post(self,request,uuid):
        form = ResetPasswordForm
        instance=MyUser.objects.get(uuid=uuid)
        update_form=ResetPasswordForm(request.POST or None,instance=instance)
        if update_form.is_valid():
            user = update_form.save(commit=False)
            user.set_password(request.POST.get('password'))
            user.save(())
            print("error",update_form.errors)
            return redirect('/login')
        return render(request,'resetpassword.html',{'form':form})

