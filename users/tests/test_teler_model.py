# Create your tests here.
from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase

from users.forms import UserLoginForm
from users.models import Teler


class TestTelerModel(TestCase):

    def test_sign_in_form_valid_details(self):
        test_user_1 = get_user_model().objects.create_user(email='telet@test1.com', username='telet@test1.com', )
        test_user_1.set_password('12345')
        test_user_1.save()

        test_teler_1 = Teler.objects.create(user=test_user_1,
                                            gender='M',
                                            mobile_number='07940236488',
                                            date_of_birth=date(year=1998, month=4, day=11)
                                            )
        test_teler_1.save()

        self.assertEqual(str(test_teler_1), 'telet@test1.com')