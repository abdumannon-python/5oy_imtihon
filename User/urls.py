from django.urls import path
from . import views
urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('register/',views.RegisterView.as_view(),name='register'),
    path('verify-otp/',views.VerifyEmailView.as_view(),name='verify_otp'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/',views.LogoutView.as_view(),name='logout'),
    path('resend-otp/',views.ResendOTPView.as_view(),name='resend_otp'),
    path('user/update/<int:pk>',views.UserUdateView.as_view(),name='userupdate'),
]