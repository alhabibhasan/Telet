from django.urls import path

from users.views import CreateUserView, UserLoginView

urlpatterns = [
    path('signup/',
         CreateUserView.as_view(),
         name='user-signup'
         ),
    path('signin/',
         UserLoginView.as_view(),
         name='user-signin'
         ),
]
