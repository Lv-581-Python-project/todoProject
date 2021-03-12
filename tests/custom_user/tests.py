from django.test import TestCase
from custom_user.models import CustomUser


class CustomUserModelsTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(id=1,
                                              first_name='Test',
                                              last_name='User',
                                              email='testuser@gmail.com',
                                              password='test')

    def test_create_user(self):
        user = CustomUser.objects.create(id=2,
                                         first_name='Test1',
                                         last_name='User1',
                                         email='testuser1@gmail.com',
                                         password='test1')
        self.assertIsInstance(user, CustomUser)

    def test_create_user_no_email(self):
        def create_user():
            res = CustomUser.objects.create(id=2,
                                            first_name='Test1',
                                            last_name='User1',
                                            email='',
                                            password='test1')
            return res
        self.assertRaises(ValueError, create_user)

    def test_str(self):
        result = self.user.__str__()
        self.assertEqual(result, 'Test User')

    def test_to_dict(self):
        result = self.user.to_dict()
        self.assertTrue(type(result) == dict)

    def test_find_by_id(self):
        user = CustomUser.get_by_id(1)
        self.assertIsInstance(user, CustomUser)

    def test_find_by_id_not_found(self):
        user = CustomUser.get_by_id(3)
        self.assertTrue(user is None)

    def test_update(self):
        data = {
            'first_name': 'User',
            'last_name': 'Test',
            'email': 'testuser@gmail.com'
        }
        result = self.user.update(data)
        self.assertEqual(self.user.first_name, 'User')
        self.assertEqual(self.user.last_name, 'Test')
        self.assertEqual(self.user.email, 'testuser@gmail.com')
        self.assertTrue(result)

    def test_remove_user(self):
        CustomUser.objects.create(id=2,
                                  first_name='Test1',
                                  last_name='User1',
                                  email='testuser1@gmail.com',
                                  password='test1')
        res = CustomUser.remove(2)
        self.assertIn(b'User removed', res.content)
