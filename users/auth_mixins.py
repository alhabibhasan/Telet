from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect


class TelerLogOutRequiredMixin(AccessMixin):
    """
    This mixin is used to prevent certain views from being accessed if the user accessing is logged in.
    Example uses:
            - Prevent logged in users from accessing the login page
            - Prevent logged in users from accessing the 'forgot your password' page
            - etc

    You need to specify :
            - A redirect URL
            - An optional message to be displayed to the user

    """
    redirect_url = None
    redirect_error_message = ''

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if len(self.redirect_error_message) > 0:
                messages.error(request, self.redirect_error_message)

            if self.redirect_url is not None:
                print(self.redirect_url)
                return redirect(self.redirect_url)
        return super().dispatch(request, *args, **kwargs)
