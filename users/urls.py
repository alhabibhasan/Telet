from django.urls import path

from users.views.account_activation_views import *
from users.views.password_reset_views import *
from users.views.authentication_views import *

urlpatterns = [
    path('signin/',
         UserSignInView.as_view(),
         name='signin'
         ),
    path('signup/',
         UserSignUpView.as_view(),
         name='signup'
         ),
    path('signout/',
         UserSignoutView.as_view(),
         name='signout'
         ),
    path('activate/',
         TelerSendEmailActivationEmailView.as_view(),
         name='send_activation_email'
         ),
    path('activate/<uidb64>/<token>/',
         TelerUserActivation.as_view(),
         name='activate'
         ),
    path('password-reset/',
         TelerPasswordResetView.as_view(),
         name='password_reset'
         ),
    path('password-reset/confirm/<uidb64>/<token>/',
         TelerPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'
         ),
    path('password-change/',
         TelerPasswordChangeView.as_view(),
         name='password_change'
         ),

]
