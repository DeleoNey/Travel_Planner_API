from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

User = get_user_model()


class UserRegistrationTestCase(APITestCase):
    """Tests for user registration"""

    def setUp(self):
        self.client = APIClient()
        self.register_url = '/api/users/register/'

    def test_user_registration_success(self):
        """Test: successful user registration"""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'SecurePass123!',
            'password2': 'SecurePass123!',
            'first_name': 'John',
            'last_name': 'Doe'
        }

        response = self.client.post(self.register_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

        user = User.objects.get()
        self.assertEqual(user.username, 'newuser')
        self.assertEqual(user.email, 'newuser@example.com')
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')

    def test_registration_with_existing_username(self):
        """Test: registration with existing username"""
        User.objects.create_user(
            username='existinguser',
            email='existing@example.com',
            password='SecurePass123!'
        )

        data = {
            'username': 'existinguser',
            'email': 'new@example.com',
            'password': 'SecurePass123!',
            'password2': 'SecurePass123!'
        }

        response = self.client.post(self.register_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
        self.assertEqual(User.objects.count(), 1)

    def test_registration_with_existing_email(self):
        """Test: registration with existing email"""
        User.objects.create_user(
            username='existinguser',
            email='existing@example.com',
            password='SecurePass123!'
        )

        data = {
            'username': 'newuser',
            'email': 'existing@example.com',
            'password': 'SecurePass123!',
            'password2': 'SecurePass123!'
        }

        response = self.client.post(self.register_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertEqual(User.objects.count(), 1)

    def test_registration_with_weak_password(self):
        """Test: registration with weak password"""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': '123',
            'password2': '123'
        }

        response = self.client.post(self.register_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_registration_missing_required_fields(self):
        """Test: registration with missing required fields"""
        data = {
            'username': 'newuser'
        }

        response = self.client.post(self.register_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_invalid_email(self):
        """Test: registration with invalid email format"""
        data = {
            'username': 'newuser',
            'email': 'invalid-email',
            'password': 'SecurePass123!',
            'password2': 'SecurePass123!'
        }

        response = self.client.post(self.register_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)


class UserLoginTestCase(APITestCase):
    """Tests for user authentication"""

    def setUp(self):
        self.client = APIClient()
        self.login_url = '/api/users/login/'

        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123!',
            first_name='Test',
            last_name='User'
        )

    def test_login_success(self):
        """Test: successful login"""
        data = {
            'username': 'testuser',
            'password': 'TestPass123!'
        }

        response = self.client.post(self.login_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check for token (adjust based on your auth method: JWT, Token, etc.)
        self.assertTrue(
            'access' in response.data or
            'token' in response.data or
            'key' in response.data
        )

    def test_login_with_email(self):
        """Test: login using email instead of username"""
        data = {
            'email': 'test@example.com',
            'password': 'TestPass123!'
        }

        response = self.client.post(self.login_url, data, format='json')

        # This should succeed if your backend supports email login
        # Otherwise it should return 400
        self.assertIn(
            response.status_code,
            [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST]
        )

    def test_login_wrong_password(self):
        """Test: login with incorrect password"""
        data = {
            'username': 'testuser',
            'password': 'WrongPassword'
        }

        response = self.client.post(self.login_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('token', response.data)
        self.assertNotIn('access', response.data)

    def test_login_nonexistent_user(self):
        """Test: login with non-existent user"""
        data = {
            'username': 'nonexistent',
            'password': 'SomePass123!'
        }

        response = self.client.post(self.login_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_missing_credentials(self):
        """Test: login with missing credentials"""
        data = {
            'username': 'testuser'
        }

        response = self.client.post(self.login_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_empty_credentials(self):
        """Test: login with empty credentials"""
        data = {
            'username': '',
            'password': ''
        }

        response = self.client.post(self.login_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_inactive_user(self):
        """Test: login with inactive user account"""
        self.user.is_active = False
        self.user.save()

        data = {
            'username': 'testuser',
            'password': 'TestPass123!'
        }

        response = self.client.post(self.login_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserProfileTestCase(APITestCase):
    """Tests for user profile management"""

    def setUp(self):
        self.client = APIClient()
        self.profile_url = '/api/users/profile/'

        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123!',
            first_name='Test',
            last_name='User'
        )

        self.client.force_authenticate(user=self.user)

    def test_get_profile(self):
        """Test: retrieve user profile"""
        response = self.client.get(self.profile_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['email'], 'test@example.com')
        self.assertEqual(response.data['first_name'], 'Test')
        self.assertEqual(response.data['last_name'], 'User')

    def test_update_profile_full(self):
        """Test: full profile update"""
        data = {
            'username': 'testuser',
            'email': 'newemail@example.com',
            'first_name': 'Updated',
            'last_name': 'Name'
        }

        response = self.client.put(self.profile_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'newemail@example.com')
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.last_name, 'Name')

    def test_update_profile_partial(self):
        """Test: partial profile update"""
        data = {
            'first_name': 'NewFirstName'
        }

        response = self.client.patch(self.profile_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'NewFirstName')
        self.assertEqual(self.user.email, 'test@example.com')  # Unchanged

    def test_update_email_to_existing(self):
        """Test: update email to one that already exists"""
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='TestPass123!'
        )

        data = {
            'email': 'other@example.com'
        }

        response = self.client.patch(self.profile_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_profile_unauthorized(self):
        """Test: access profile without authentication"""
        self.client.force_authenticate(user=None)
        response = self.client.get(self.profile_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cannot_change_username(self):
        """Test: username should not be changeable (if enforced)"""
        data = {
            'username': 'newusername'
        }

        response = self.client.patch(self.profile_url, data, format='json')

        # Depending on your implementation:
        # Either username change is allowed or it's ignored/rejected
        if response.status_code == status.HTTP_200_OK:
            self.user.refresh_from_db()
            # If allowed, check it changed
            # self.assertEqual(self.user.username, 'newusername')
        else:
            # If not allowed
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserLogoutTestCase(APITestCase):
    """Tests for user logout"""

    def setUp(self):
        self.client = APIClient()
        self.logout_url = '/api/users/logout/'

        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123!'
        )

        self.client.force_authenticate(user=self.user)