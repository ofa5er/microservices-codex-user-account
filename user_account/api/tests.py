#
# @Author: Fakher Oueslati 
# @Date: 2017-07-23 22:21:18 
# @Last Modified by:   Fakher Oueslati 
# @Last Modified time: 2017-07-23 22:21:18 
#
# /api/tests.py

from django.test import TestCase
from .models import UserAccount
from rest_framework.test import APIClient
from rest_framework import status
from django.core.urlresolvers import reverse


class ModelTestCase(TestCase):
    """This class defines the test suite for the user_account model."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.uid = "qweqw121212sdasdasd"
        self.first_name = "qweqw121212sdasdasd"
        self.last_name = "qweqw121212sdasdasd"
        self.address = "qweqw121212sdasdasd"
        self.email = "qweqw121212sdasdasd"
        self.billing_address = "13213123"
        self.shipping_address = "13213123"
        self.user_account = UserAccount(uid=self.uid)

    def test_model_can_create_a_user_account(self):
        """Test the user account model can create a user account."""
        old_count = UserAccount.objects.count()
        self.user_account.save()
        new_count = UserAccount.objects.count()
        self.assertNotEqual(old_count, new_count)

class ViewTestCase(TestCase):
    """Test suite for the api views."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()
        self.uid = {'uid': '13123aaed123123asdd'}
        self.response = self.client.post(
            reverse('create'),
            self.uid,
            format="json")

    def test_api_can_create_a_user_account(self):
        """Test the api has user account creation capability."""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
