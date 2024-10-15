from django.urls import path
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from . import views

urlpatterns = [
    path('register/', views.signUpView, name='signup'),
    path('logout/', views.logOutView, name='logout'),
    path('profile/<int:pk>/', views.UserDetailView.as_view(), name="profile"),
    path('update-profile/<int:pk>', views.userUpdateProfileView, name='update_profile'),
    path('<int:pk>/delete', views.deleteProfile, name='delete_profile'),
    path('password-reset/', PasswordResetView.as_view(
        template_name='UserApp/password_reset.html'), name='password_reset'),
    path('password-reset/done/',
         PasswordResetDoneView.as_view(
             template_name='UserApp/password_reset_done.html'),
         name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>',
         PasswordResetConfirmView.as_view(
             template_name='UserApp/password_reset_confirm.html'),
         name="password_reset_confirm"),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(template_name='UserApp/password_reset_complete.html'),
         name="password_reset_complete"),
]
