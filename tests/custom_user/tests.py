import json

from django.test import TestCase

from custom_user.models import CustomUser


class CustomUserModelsTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.create(id=1,
                                      first_name='Test',
                                      last_name='User',
                                      email='testuser@gmail.com',
                                      password='test')

    def test_create_user(self):
        user = CustomUser.create(id=2,
                                 first_name='Test1',
                                 last_name='User1',
                                 email='testuser1@gmail.com',
                                 password='test1')
        self.assertIsInstance(user, CustomUser)

    def test_create_user_invalid_data(self):
        user = CustomUser.create(id='a',
                                 first_name='Test1',
                                 last_name='User1',
                                 email='testuser1@gmail.com',
                                 password='test1')
        self.assertEqual(user, False)

    def test_create_user_no_email(self):
        def create_user():
            res = CustomUser.create(id=2,
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
        result = self.user.update(first_name='User', last_name='Test', email='testuser@gmail.com')
        self.assertEqual(self.user.first_name, 'User')
        self.assertEqual(self.user.last_name, 'Test')
        self.assertEqual(self.user.email, 'testuser@gmail.com')
        self.assertTrue(result)

    def test_update_fail(self):
        result = self.user.update(first_name='123123123123123123123123123123123123123123123123123123123123123123123123',
                                  last_name='Test',
                                  email='testuser@gmail.com')
        self.assertEqual(result, None)

    def test_remove_user(self):
        user = CustomUser.objects.create(id=2,
                                         first_name='Test1',
                                         last_name='User1',
                                         email='testuser1@gmail.com',
                                         password='test1')
        user.remove(user.id)
        user = CustomUser.get_by_id(user.id)
        self.assertEqual(None, user)


class CustomUserViewsTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.create(id=2,
                                      first_name="Test",
                                      last_name="User",
                                      email="testuser@gmail.com",
                                      password="test")

        self.user = CustomUser.create(id=3,
                                      first_name="Test2",
                                      last_name="User2",
                                      email="testuser2@gmail.com",
                                      password="test2")

    def test_get_by_id(self):
        data = {'first_name': 'Test', 'last_name': 'User', 'email': 'testuser@gmail.com'}
        responce = self.client.get('/custom-user/profile/2/')
        self.assertEqual(responce.json(), data)

    def test_get_user_not_exist(self):
        responce = self.client.get('/custom-user/profile/10/')
        self.assertEqual(responce.status_code, 400)


    def test_create_user(self):
        data = {'first_name': 'Test3', 'last_name': 'User3', 'email': 'testuser3@gmail.com'}
        response = self.client.generic('POST', '/custom-user/create/', json.dumps({'first_name': 'Test3',
                                                                                   'last_name': 'User3',
                                                                                   'email': 'testuser3@gmail.com'}))
        self.assertEqual(response.json(), data)

    def test_create_user_empty_json(self):
        response = self.client.generic('POST', '/custom-user/create/', json.dumps({}))
        self.assertEqual(response.status_code, 400)


    def test_create_user_bad_save(self):
        response = self.client.generic('POST', '/custom-user/create/', json.dumps({
            'first_name': 'Test3Test3Test3Test3Test3Test3Test3Test3Test3Test3Test3Test3Test3Test3Test3Test3Test3Test3',
            'last_name': 'User3',
            'email': 'testuser3@gmail.com'}))
        self.assertEqual(response.status_code, 400)



    def test_put_all_input_data(self):
        data = {'first_name': 'NewName', 'last_name': 'User', 'email': 'testuser@gmail.com'}
        response = self.client.generic('PUT', '/custom-user/profile/2/', json.dumps({'first_name': 'NewName',
                                                                                     'last_name': 'User',
                                                                                     'email': 'testuser@gmail.com'}))
        self.assertEqual(response.json(), data)

    def test_put_not_all_input_data(self):
        data = {'first_name': 'Test', 'last_name': 'NewUser', 'email': 'testuser@gmail.com'}
        response = self.client.generic('PUT', '/custom-user/profile/2/', json.dumps({'last_name': 'NewUser',
                                                                                     'email': 'testuser@gmail.com'}))
        self.assertEqual(response.json(), data)

    def test_put_no_user(self):
        response = self.client.generic('PUT', '/custom-user/profile/100/', json.dumps({'first_name': 'NewName',
                                                                                     'last_name': 'User',
                                                                                     'email': 'testuser@gmail.com'}))
        self.assertEqual(response.status_code, 404)


    def test_put_empty_data(self):
        response = self.client.generic('PUT', '/custom-user/profile/2/', json.dumps({}))
        self.assertEqual(response.status_code, 400)

    def test_update_user_bad_save(self):
        response = self.client.generic('PUT', '/custom-user/profile/2/', json.dumps({
            'first_name': "123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890",
            'last_name': 'User',
            'email': 'testuser@gmail.com'})
            )
        self.assertEqual(response.status_code, 400)

    def test_delete(self):
        response = self.client.generic('DELETE', '/custom-user/profile/2/')
        self.assertEqual(response.status_code, 200)

    def test_delete_user_not_found(self):
        response = self.client.generic('DELETE', '/custom-user/profile/200/')
        self.assertEqual(response.status_code, 400)




