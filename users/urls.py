from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterView, SuccessView, CancelView, CustomLoginView

app_name = UsersConfig.name

urlpatterns = [
    path('', RegisterView.as_view(template_name='users/register.html'), name='register'),
    path('login/', CustomLoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('success/', SuccessView.as_view(template_name='users/success.html'), name='success'),
    path('cancel/', CancelView.as_view(template_name='users/cancel.html'), name='cancel'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
