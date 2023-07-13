from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

from django.views.i18n import JavaScriptCatalog

urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.register, name='register'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('edit_all_events', views.edit_all_events, name='edit_all_events'),
    path('reset_password', auth_views.PasswordResetView.as_view(
        template_name="auth/password_reset.html"), name="reset_password"),
    path('reset_password_sent', auth_views.PasswordResetDoneView.as_view(
        template_name="auth/password_reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(
        template_name="auth/password_reset_form.html"),  name="password_reset_confirm"),
    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(
        template_name="auth/password_reset_done.html"),  name="password_reset_complete"),
    path('create_event', views.create_event, name='create_event'),
    path('create_activity', views.create_activity, name='create_activity'),
    path('edit_profile', views.edit_profile, name='edit_profile'),
    path('edit_event/<int:event_id>', views.edit_event, name='edit_event'),
    path('edit_activity/<int:activity_id>',
         views.edit_activity, name='edit_activity'),
    path('filter_events', views.filter_events, name='filter_events'),
    path('edit_date/<int:date_id>', views.edit_date, name='edit_date'),
    path('event/<int:event_id>', views.event, name='event'),
    path('event/<int:event_id>/participants',
         views.event_participants, name='event_participants'),
    path('add_participant', views.add_participant, name='add_participant'),
    path('my_events', views.my_events, name='my_events'),
    path('calendar/', views.calendar_resolver, name='calendar'),
    path('calendar/<str:date>', views.calendar_view, name='calendar_view')


]

urlpatterns += [path('jsi18n.js',
                     JavaScriptCatalog.as_view(packages=['recurrence']), name='jsi18n'), ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
