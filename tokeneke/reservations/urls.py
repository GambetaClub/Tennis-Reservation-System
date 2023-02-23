from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.views.i18n import JavaScriptCatalog

urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.register, name='register'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('edit_all_events', views.edit_all_events, name='edit_all_events'),
    # Still need to finish the password reset process
    path('reset_password', auth_views.PasswordResetView.as_view(template_name="auth/password_reset.html"), name="reset_password"),
    path('reset_password_sent', auth_views.PasswordResetDoneView.as_view(template_name="auth/password_reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name="auth/password_reset_form.html"),  name="password_reset_confirm"),
    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(template_name="auth/password_reset_done.html"),  name="password_reset_complete"),
    # Still need to finish the password reset process
    path('create_event', views.create_event, name='create_event'),
    path('create_clinic', views.create_clinic, name='create_clinic'),
    path('edit_event/<int:event_id>', views.edit_event, name='edit_event'),
    path('edit_clinic/<int:clinic_id>', views.edit_clinic, name='edit_clinic'),
    path('edit_date/<int:date_id>', views.edit_date, name='edit_date'),
    path('event/<int:event_id>', views.event, name='event'),
    path('event/<int:event_id>/participants', views.event_participants, name='event_participants'),
    path('add_participant', views.add_participant, name='add_participant'),
    path('my_events', views.my_events, name='my_events')
    
]

urlpatterns += [ path('jsi18n.js', JavaScriptCatalog.as_view(packages=['recurrence']), name='jsi18n'), ]

