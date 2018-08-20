from django.contrib.auth import views as auth_views
from django.urls import path, include
from accounts.views.person import PersonSignUpView

urlpatterns = [
    path('signup',
         PersonSignUpView.as_view(),
         name='person-signup'),
]
