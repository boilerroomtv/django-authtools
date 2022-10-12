from django.urls import include, re_path
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import admin

from django.urls import reverse_lazy

from authtools import views
from authtools.forms import FriendlyPasswordResetForm

from auth_tests.urls import CustomRequestAuthenticationForm, uid_token

admin.autodiscover()


def dumbview(request):
    return HttpResponse('dumbview')


urlpatterns = [
    re_path(r'^reset_and_login/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.PasswordResetConfirmAndLoginView.as_view()),
    re_path(r'^logout-then-login/$', views.LogoutView.as_view(url=reverse_lazy('login')), name='logout_then_login'),
    re_path(r'^friendly_password_reset/$',
        views.PasswordResetView.as_view(form_class=FriendlyPasswordResetForm),
        name='friendly_password_reset'),
    re_path(r'^login_required/$', login_required(dumbview), name='login_required'),
    # From django.contrib.auth.tests.url

    re_path(r'^password_reset_extra_email_context/$', views.PasswordResetView.as_view(extra_email_context=dict(greeting='Hello!'))),
    re_path(r'^password_reset/html_email_template/$', views.PasswordResetView.as_view(html_email_template_name='registration/html_password_reset_email.html')),
    re_path(r'^', include('authtools.urls')),
]

urlpatterns += [
    re_path(r'^reset/post_reset_login/{}/$'.format(uid_token),
        views.PasswordResetConfirmView.as_view(post_reset_login=True)),
    re_path(r'^custom_request_auth_login/$',
        views.LoginView.as_view(authentication_form=CustomRequestAuthenticationForm)),
    re_path(
        r'^reset/post_reset_login_custom_backend/{}/$'.format(uid_token),
        views.PasswordResetConfirmView.as_view(
            post_reset_login=True,
            post_reset_login_backend='django.contrib.auth.backends.AllowAllUsersModelBackend',
        ),
    ),
    re_path(r'^logout/allowed_hosts/$', views.LogoutView.as_view(success_url_allowed_hosts={'otherserver'})),
    re_path(r'^login/allowed_hosts/$', views.LoginView.as_view(success_url_allowed_hosts={'otherserver'})),
]
