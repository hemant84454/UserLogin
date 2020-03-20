from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
app_name = 'Profile'


urlpatterns=[
    path('',views.HomeView, name='home'),
    path('signup/',views.PostView.as_view(), name='signup'),
    # path('show/',views.RetriveView.as_view(),name='show'),
    path('update/<uuid:uuid>',login_required(views.UpdateView.as_view()),name='update'),
    path('delete/<uuid:uuid>',views.DestroyView.as_view()),
    # path('otp/(?P<id>[0-9]+)$',views.Otp_Check.as_view(),name='otp'),
    path('login/', views.UserProfile.as_view(), name="login"),
    path('logout',views.LogoutView.as_view(),name='logout'),
    path('activate/<uuid:uuid>',views.Activate.as_view(),name='activate'),
    path('forgot/',views.ForgotPassword.as_view(), name='forgot'),
    path('change_password/', views.change_password, name='change_password'),
    path('reset_password/<uuid:uuid>', views.ResetPassword.as_view(), name="reset_password"),

]