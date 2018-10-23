from django.test import TestCase


class TestLogoutRequiredMixin(TestCase):
    """

    Will test the mixin when different http methods are used to access a class
    e.g. PUT, PATCH, GET, POST, DELETE, OPTIONS etc.
    The dispatch method should be ran in all such cases.

    """
    # def test_logout_required_mixin(self):
