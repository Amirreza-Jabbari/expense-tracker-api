from django.urls import path
from .views import *
from . import views

app_name = 'user'

urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create'),
    path('get/<str:email>/', RetrieveUserView.as_view(), name='get'),
    path('list/', ListUserView.as_view(), name='list'),
    path('update/<str:email>/', UpdateUserView.as_view(), name='update'),
    path('delete/<str:email>/', DeleteUserView.as_view(), name='delete'),
    path('password-reset-request/', views.PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('reset-password/', views.password_reset, name='password_reset'),
    path('reset-password/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

]