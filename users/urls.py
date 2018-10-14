from django.urls import path

from users.views import TelerLoginView, TelerSignUpView, TelerLoggedInView, TelerUserLogout

urlpatterns = [
    path('login/',
         TelerLoginView.as_view(),
         name='user-login'
         ),
    path('signup/',
         TelerSignUpView.as_view(),
         name='user-signup'
         ),
    path('logged-in/',
         TelerLoggedInView.as_view(),
         name='user-logged-in'
         ),
    path('log-out/',
         TelerUserLogout.as_view(),
         name='user-logout'
         ),

]
