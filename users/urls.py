from django.urls import path

from . import views

app_name = 'users'


urlpatterns = [
    path('register/', views.UserEstandarRegisterCreateView.as_view(), name='register'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.LogoutUser.as_view(), name='logout'),
    path('update/', views.UpdatePassword.as_view(), name='password'),
    path('verification/<pk>', views.CodeVerificationView.as_view(), name='verification'),
]
