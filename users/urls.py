from django.urls import path

from users.views import TelerSignInView, TelerSignUpView, TelerSignedInView, TelerUserSignout, TelerUserActivation

urlpatterns = [
    path('signin/',
         TelerSignInView.as_view(),
         name='signin'
         ),
    path('signup/',
         TelerSignUpView.as_view(),
         name='signup'
         ),
    path('signed-in/',
         TelerSignedInView.as_view(),
         name='signed-in'
         ),
    path('signout/',
         TelerUserSignout.as_view(),
         name='signout'
         ),
    path('activate/<uidb64>/<token>',
         TelerUserActivation.as_view(),
         name='activate'
         )

]
