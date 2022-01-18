from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

VERIFY_USER_URL = reverse('email_verify')


class TestEmailVerification(TestCase):
    """Test the users API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_verification_otp(self):
        """test for verification to fail with wrong otp"""
        data = {
            'email': 'test@coding.com',
            'otp': '12345',
        }
        res = self.client.post(VERIFY_USER_URL, data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_with_no_filled_fields(self):
        """test to verify that email and otp fields must be supplied"""
        data = {
            'email': '',
        }
        res = self.client.post(VERIFY_USER_URL, data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
