from django.urls import path

from users.views import CreateUserView

urlpatterns = [
    path('signup/',
         CreateUserView.as_view(),
         name='user-signup'
         ),
]