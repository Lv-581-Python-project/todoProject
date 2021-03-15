from django.test import TestCase, Client
from custom_user.models import CustomUser
import json



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

class CustomUserViewsTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(id=2,
                                              first_name="Test",
                                              last_name="User",
                                              email="testuser@gmail.com",
                                              password="test")

        self.user = CustomUser.objects.create(id=3,
                                              first_name="Test2",
                                              last_name="User2",
                                              email="testuser2@gmail.com",
                                              password="test2")



    def test_get_by_id(self):
        data = {'first_name': 'Test', 'last_name': 'User', 'email': 'testuser@gmail.com'}
        responce = self.client.get('/custom_user/profile/2/')
        self.assertEqual(responce.json() , data)

    def test_create_user(self):
        data = {'first_name': 'Test3', 'last_name': 'User3', 'email': 'testuser3@gmail.com'}
        response = self.client.generic('POST', '/custom_user/create/', json.dumps({'first_name': 'Test3',
                                                                                   'last_name': 'User3',
                                                                                   'email': 'testuser3@gmail.com'}))
        self.assertEqual(response.json(),data)

    def test_put_all_input_data(self):
        data = {'first_name': 'NewName', 'last_name': 'User', 'email': 'testuser@gmail.com'}
        response = self.client.generic('PUT', '/custom_user/profile/2/', json.dumps({'first_name': 'NewName',
                                                                                   'last_name': 'User',
                                                                                   'email': 'testuser@gmail.com'}))
        self.assertEqual(response.json(), data)

    def test_put_not_all_input_data(self):
        data = {'first_name': 'Test', 'last_name': 'NewUser', 'email': 'testuser@gmail.com'}
        response = self.client.generic('PUT', '/custom_user/profile/2/', json.dumps({'last_name': 'NewUser',
                                                                                   'email': 'testuser@gmail.com'}))
        self.assertEqual(response.json(), data)

    def test_delete(self):
        response = self.client.generic('DELETE', '/custom_user/profile/2/')
        self.assertEqual(response.status_code, 200)




