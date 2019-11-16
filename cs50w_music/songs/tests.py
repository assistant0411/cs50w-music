from django.test import Client, TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from songs.models import Song, Playlist, Album
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
import datetime


class IndexTest(TestCase):
    #def setUp(self):

    def test_index(self):

        # Set up client to make requests
        c = Client()

        # Send get request to index page and store response
        response = c.get("/")

        # Make sure status code is 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Make sure three flights are returned in the context
        #self.assertEqual(response.context["flights"].count(), 3)


class BaseAPITest(TestCase):
    def setUp(self):
        self.client = APIClient(enforce_csrf_checks=True)

        self.old_user_data = {
            'username': 'old_user',
            'password': 'old_password'
        }
        self.old_user = get_user_model().objects.create_user(**self.old_user_data)


class RegistrationAPITests(BaseAPITest):

    def setUp(self):
        super().setUp()
        self.new_user_data = {
            'username': 'new_user',
            'password': 'new_password',
            'password_confirmation': 'new_password',
            'birth_date': datetime.date.today() - datetime.timedelta(days=1),
            'country': 'BG'

        }

    def test_user_registration(self):
        """User registration should be successful with proper credentials and non-taken username."""
        response = self.client.post(reverse('songs:user-register'), self.new_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_user_model().objects.count(), 2) # self.old_user and new_user
        self.assertEqual(response.json()["user"]["username"], self.new_user_data["username"])
        self.assertIn('token', response.data)

    def test_fail_user_registration_username_taken(self):
        """User registration should fail if username is already taken."""
        old_user_data = self.old_user_data.copy()
        old_user_data.update({"password_confirmation": self.old_user_data["password"]})
        response = self.client.post(reverse('songs:user-register'), old_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(get_user_model().objects.count(), 1) # self.old_user
        self.assertEqual(response.json()["username"][0], 'A user with that username already exists.')

    def test_fail_user_registration_password_mismatch(self):
        """User registration should fail if password_confirmation doesn't match password."""
        new_user_data = self.new_user_data.copy()
        new_user_data["password_confirmation"] += "_2"
        response = self.client.post(reverse('songs:user-register'), new_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(get_user_model().objects.count(), 1) # self.old_user
        self.assertEqual(response.json()["non_field_errors"][0], 'Passwords do not match')

    def test_fail_user_registration_short_password(self):
        """User registration should fail if the provided password is less than 8 characters."""
        new_user_data = self.new_user_data.copy()
        new_user_data["password"] = "pass"
        response = self.client.post(reverse('songs:user-register'), new_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(get_user_model().objects.count(), 1) # self.old_user
        self.assertEqual(response.json()["non_field_errors"][0], 'This password is too short. It must contain at least 8 characters.')

    def test_fail_user_registration_future_birthday(self):
        """User registration should fail if the provided birth date is in the future."""
        new_user_data = self.new_user_data.copy()
        new_user_data["birth_date"] = datetime.date.today() + datetime.timedelta(days=1)
        response = self.client.post(reverse('songs:user-register'), new_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(get_user_model().objects.count(), 1) # self.old_user
        self.assertRegex(response.json()["birth_date"][0], r'Ensure this value is less than or equal to \d{4}-\d{2}-\d{2}.')

    def test_fail_user_registration_invalid_country(self):
        """User registration should fail if the provided country doesn't exist."""
        new_user_data = self.new_user_data.copy()
        new_user_data["country"] = 'AA'
        response = self.client.post(reverse('songs:user-register'), new_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(get_user_model().objects.count(), 1) # self.old_user
        self.assertRegex(response.json()["country"][0], r'.* is not a valid choice.')

    def test_fail_user_registration_skip_username(self):
        """User registration should fail if username is not provided."""
        new_user_data = self.new_user_data.copy()
        new_user_data.pop("username")
        response = self.client.post(reverse('songs:user-register'), new_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(get_user_model().objects.count(), 1) # self.old_user
        self.assertEqual(response.json()["username"][0], 'This field is required.')

    def test_fail_user_registration_skip_password(self):
        """User registration should fail if password is not provided."""
        new_user_data = self.new_user_data.copy()
        new_user_data.pop("password")
        response = self.client.post(reverse('songs:user-register'), new_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(get_user_model().objects.count(), 1) # self.old_user
        self.assertEqual(response.json()["password"][0], 'This field is required.')

    def test_fail_user_registration_skip_password_confirmation(self):
        """User registration should fail if password confirmation is not provided."""
        new_user_data = self.new_user_data.copy()
        new_user_data.pop("password_confirmation")
        response = self.client.post(reverse('songs:user-register'), new_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(get_user_model().objects.count(), 1) # self.old_user
        self.assertEqual(response.json()["password_confirmation"][0], 'This field is required.')


class LoginAPITests(BaseAPITest):
    def test_user_login(self):
        """User login should be successful correct credentials."""
        response = self.client.post(reverse('songs:user-login'), self.old_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["user"]["username"], self.old_user_data["username"])
        self.assertIn('token', response.data)

    def test_fail_user_login_wrong_username(self):
        """User login should fail with incorrect credentials."""
        old_user_data = self.old_user_data.copy()
        old_user_data["username"] += "_2"
        response = self.client.post(reverse('songs:user-login'), old_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["non_field_errors"][0], 'Invalid Details.')

    def test_fail_user_login_wrong_password(self):
        """User login should fail with incorrect credentials."""
        old_user_data = self.old_user_data.copy()
        old_user_data["password"] += "_2"
        response = self.client.post(reverse('songs:user-login'), old_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["non_field_errors"][0], 'Invalid Details.')

    def test_fail_user_login_skip_username(self):
        """User login should fail if username is not provided."""
        old_user_data = self.old_user_data.copy()
        old_user_data.pop("username")
        response = self.client.post(reverse('songs:user-login'), old_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["username"][0], 'This field is required.')

    def test_fail_user_login_skip_password(self):
        """User login should fail if password is not provided."""
        old_user_data = self.old_user_data.copy()
        old_user_data.pop("password")
        response = self.client.post(reverse('songs:user-login'), old_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["password"][0], 'This field is required.')