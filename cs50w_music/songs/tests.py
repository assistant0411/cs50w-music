from django.test import Client, TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from songs.models import Song, Playlist, Album
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
import datetime
from django.db.models import Max


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

        self.yesterday = datetime.date.today() - datetime.timedelta(days=1)
        self.tomorrow = datetime.date.today() + datetime.timedelta(days=1)

        self.old_user_data = {
            'username': 'old_user',
            'password': 'old_password',
            'first_name': 'Old',
            'last_name': 'User',
            'birth_date': self.yesterday,
            'country': 'US'
        }
        self.old_user = get_user_model().objects.create_user(**self.old_user_data)

        self.old_user_2_data = {
            'username': 'old_user_2',
            'password': 'old_password_2'
        }
        self.old_user_2 = get_user_model().objects.create_user(**self.old_user_2_data)

        self.new_user_data = {
            'username': 'new_user',
            'password': 'new_password',
            'password_confirmation': 'new_password',
            'first_name': 'New',
            'last_name': 'User',
            'birth_date': self.yesterday,
            'country': 'BG'
        }


class RegistrationAPITests(BaseAPITest):
    def test_user_registration(self):
        """User registration should be successful with proper credentials and non-taken username."""
        response = self.client.post(reverse('songs:user-register'), self.new_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_user_model().objects.count(), 3) # self.old_user, old_user_2 and new_user
        self.assertEqual(response.json()["user"]["username"], self.new_user_data["username"])
        self.assertIn('token', response.data)

    def test_fail_user_registration_username_taken(self):
        """User registration should fail if username is already taken."""
        old_user_data = self.old_user_data.copy()
        old_user_data.update({"password_confirmation": self.old_user_data["password"]})
        response = self.client.post(reverse('songs:user-register'), old_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(get_user_model().objects.count(), 2) # self.old_user and old_user_2
        self.assertEqual(response.json()["username"][0], 'A user with that username already exists.')

    def test_fail_user_registration_password_mismatch(self):
        """User registration should fail if password_confirmation doesn't match password."""
        new_user_data = self.new_user_data.copy()
        new_user_data["password_confirmation"] += "_2"
        response = self.client.post(reverse('songs:user-register'), new_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(get_user_model().objects.count(), 2) # self.old_user and old_user_2
        self.assertEqual(response.json()["non_field_errors"][0], 'Passwords do not match')

    def test_fail_user_registration_short_password(self):
        """User registration should fail if the provided password is less than 8 characters."""
        new_user_data = self.new_user_data.copy()
        new_user_data["password"] = "pass"
        response = self.client.post(reverse('songs:user-register'), new_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(get_user_model().objects.count(), 2) # self.old_user and old_user_2
        self.assertEqual(response.json()["non_field_errors"][0], 'This password is too short. It must contain at least 8 characters.')

    def test_fail_user_registration_future_birthday(self):
        """User registration should fail if the provided birth date is in the future."""
        new_user_data = self.new_user_data.copy()
        new_user_data["birth_date"] = self.tomorrow
        response = self.client.post(reverse('songs:user-register'), new_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(get_user_model().objects.count(), 2) # self.old_user and old_user_2
        self.assertRegex(response.json()["birth_date"][0], r'Ensure this value is less than or equal to \d{4}-\d{2}-\d{2}.')

    def test_fail_user_registration_invalid_country(self):
        """User registration should fail if the provided country doesn't exist."""
        new_user_data = self.new_user_data.copy()
        new_user_data["country"] = 'AA'
        response = self.client.post(reverse('songs:user-register'), new_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(get_user_model().objects.count(), 2) # self.old_user and old_user_2
        self.assertRegex(response.json()["country"][0], r'.* is not a valid choice.')

    def test_fail_user_registration_skip_username(self):
        """User registration should fail if username is not provided."""
        new_user_data = self.new_user_data.copy()
        new_user_data.pop("username")
        response = self.client.post(reverse('songs:user-register'), new_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(get_user_model().objects.count(), 2) # self.old_user and old_user_2
        self.assertEqual(response.json()["username"][0], 'This field is required.')

    def test_fail_user_registration_skip_password(self):
        """User registration should fail if password is not provided."""
        new_user_data = self.new_user_data.copy()
        new_user_data.pop("password")
        response = self.client.post(reverse('songs:user-register'), new_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(get_user_model().objects.count(), 2) # self.old_user and old_user_2
        self.assertEqual(response.json()["password"][0], 'This field is required.')

    def test_fail_user_registration_skip_password_confirmation(self):
        """User registration should fail if password confirmation is not provided."""
        new_user_data = self.new_user_data.copy()
        new_user_data.pop("password_confirmation")
        response = self.client.post(reverse('songs:user-register'), new_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(get_user_model().objects.count(), 2) # self.old_user and old_user_2
        self.assertEqual(response.json()["password_confirmation"][0], 'This field is required.')

    def test_fail_registration_forbidden_methods(self):
        #get
        response = self.client.get(reverse('songs:user-register'))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        #put
        response = self.client.put(reverse('songs:user-register'), self.new_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        #delete
        response = self.client.delete(reverse('songs:user-register'))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

class LoginAPITests(BaseAPITest):
    def test_user_login(self):
        """User login should be successful correct credentials."""
        response = self.client.post(reverse('songs:user-login'), self.old_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["user"]["username"], self.old_user.username)
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

    def test_fail_login_forbidden_methods(self):
        """Check that get, put and delete methods are not allowed for user login"""
        #get
        response = self.client.get(reverse('songs:user-login'))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        #put
        response = self.client.put(reverse('songs:user-login'), self.old_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        #delete
        response = self.client.delete(reverse('songs:user-login'))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class AuthenticatedAPITests(BaseAPITest):
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(user=self.old_user)

        # Prepare the song data
        self.song_data = {
            'title': 'Test Song',
            'audio_file': SimpleUploadedFile(name="test_audio_file.mp3", content=b'test audio file content', content_type='audio/mp3'),
            'release_date': self.yesterday,
            'artists': [self.old_user.id],  # Assuming you want to associate the current user with the song
            'genre': 'pop',
            'duration': 200,
            'track_number': 1
        }

        # create a song and then set artists to prevent TypeError 
        song_data = self.song_data.copy()
        artists = song_data.pop("artists")
        self.old_song = Song.objects.create(**song_data)
        self.old_song.artists.set(artists)

        self.tearDown()

    def tearDown(self):
        # Reset the position of the file-like object after each test
        self.song_data["audio_file"].seek(0)


class UserViewTest(AuthenticatedAPITests):
    def test_user_list(self):
        """Successfully list all users."""
        response = self.client.get(reverse('songs:users-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()["results"]), 2)  # list 2 users - old_user and old_user_2

    def test_fail_user_list_forbidden_methods(self):
        """Check that post, put and delete methods are not allowed for user list"""
        # post
        response = self.client.post(reverse('songs:users-list'), self.new_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        # put
        response = self.client.put(reverse('songs:users-list'))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        # delete
        response = self.client.delete(reverse('songs:users-list'))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_user_detail(self):
        """Successfully get old_user details"""
        response = self.client.get(reverse('songs:users-detail', args=[self.old_user.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["username"], self.old_user.username)

    def test_fail_user_detail_password_and_email(self):
        """Make sure that user password and email are not being sent"""
        response = self.client.get(reverse('songs:users-detail', args=[self.old_user.id]))
        with self.assertRaises(KeyError) as raises:
            response.json()["password"]
        with self.assertRaises(KeyError) as raises:
            response.json()["email"]
        
    def test_fail_user_detail_invalid_id(self):
        """Fail to get details about a user with an invallid id"""
        response = self.client.get(reverse('songs:users-detail', args=[get_user_model().objects.all().aggregate(Max("id"))["id__max"] + 1]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_detail_update(self):
        """Test user can update their details"""
        new_user_data = self.new_user_data.copy()
        new_user_data.update({"old_password": self.old_user_data["password"]})
        old_password_hash = self.old_user.password
        response = self.client.put(reverse('songs:users-detail', args=[self.old_user.id]), new_user_data, format='json')
        self.old_user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.old_user.username, self.new_user_data["username"])
        self.assertNotEqual(self.old_user.password, old_password_hash)

    def test_user_detail_change_username_taken(self):
        """change username"""
        new_username = "non_taken_user"
        response = self.client.put(reverse('songs:users-detail', args=[self.old_user.id]), {"username": new_username}, format='json')
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["username"][0], new_username)

    def test_fail_user_detail_change_username_taken(self):
        """Assert user can't change their username to a taken one"""
        response = self.client.put(reverse('songs:users-detail', args=[self.old_user.id]), {"username": self.old_user_2.username}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["username"][0], 'A user with that username already exists.')

    def test_fail_user_detail_change_password_incorrect_old_password(self):
        """Assert user cant change they password if the input incorrect old password"""
        old_password = self.old_user.password
        response = self.client.patch(
            reverse('songs:users-detail', 
                    args=[self.old_user.id]),
                    {"old_password": "incorrect password", "password": self.new_user_data["password"], "password_confirmation": self.new_user_data["password"]}, 
                    format='json')
        self.old_user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.old_user.password, old_password)
        self.assertEqual(response.json()["old_password"][0], 'Old password is incorrect')

    def test_fail_user_detail_change_password_short(self):
        """Assert user cant change they password if the input a short new password"""
        old_password = self.old_user.password
        response = self.client.patch(
            reverse('songs:users-detail', 
                    args=[self.old_user.id]),
                    {"old_password": self.old_user_data["password"], "password": "short", "password_confirmation": "short"}, 
                    format='json')
        self.old_user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.old_user.password, old_password)
        self.assertEqual(response.json()["non_field_errors"][0], 'This password is too short. It must contain at least 8 characters.')

    def test_fail_user_detail_post(self):
        """A user should be created only using register"""
        response = self.client.post(reverse('songs:users-detail', args=[self.old_user.id]))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_fail_user_detail_another_user(self):
        """
        Check that post, put and delete methods are not allowed for another user
        Authenticated as old_user and attempt to send those requests to old_user_2
        """
        # post
        response = self.client.post(reverse('songs:users-detail', args=[self.old_user_2.id]))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        # put
        response = self.client.put(reverse('songs:users-detail', args=[self.old_user_2.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # delete
        response = self.client.delete(reverse('songs:users-detail', args=[self.old_user_2.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SongTests(AuthenticatedAPITests):
    def test_create_song(self):
        response = self.client.post('/api/songs/', data=self.song_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Song.objects.count(), 2)
        self.assertEqual(response.json()["title"], self.song_data["title"])

    def test_fail_create_song_invalid_audio_file(self):
        song_data = self.song_data.copy()
        song_data.pop("audio_file")
        song_data["audio_file"] = SimpleUploadedFile(name="test_image_file.png", content=b'test image file content', content_type='image/png'),
        response = self.client.post('/api/songs/', data=song_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Song.objects.count(), 1)
        self.assertRegex(response.json()["audio_file"][0], r'File extension .* is not allowed. Allowed extensions are: mp3, wav, ogg.')
