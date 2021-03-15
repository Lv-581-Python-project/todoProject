import json
from django.test import TestCase
from todolist.models import ToDoList
from custom_user.models import CustomUser


class ToDoListViewTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(id=1,
                                              first_name="TestUser",
                                              last_name="UserLastName",
                                              email="test@gmail.com",
                                              password="adminpassword")
        self.user2 = CustomUser.objects.create(id=2,
                                               first_name="TestUser2",
                                               last_name="UserLastName2",
                                               email="test2@gmail.com",
                                               password="adminpassword2")
        self.todo_list = ToDoList.objects.create(id=10,
                                                 name="TestList",
                                                 description="Test description")
        self.todo_list.members.add(self.user.id)

    # Testing GET method

    def test_get_one_list(self):
        response = self.client.get('/todolist/10/')
        self.assertEqual(response.status_code, 200)

    def test_get_not_existing_list(self):
        response = self.client.get('/todolist/28/')
        self.assertEqual(response.status_code, 404)

    def test_get_one_wrong_list_pk(self):
        response = self.client.get('/todolist/w/')
        self.assertEqual(response.status_code, 404)

    def test_get_all_lists(self):
        response = self.client.get('/todolist/')
        self.assertEqual(response.status_code, 200)

    # Testing Post method

    def test_post_data_valid_data(self):
        response = self.client.generic('POST', '/todolist/', json.dumps({
            "name": "name1",
            "description": "LIST1", "members": [self.user.id]
        }))
        self.assertEqual(response.status_code, 201)

    def test_post_data_no_data(self):
        response = self.client.generic('POST', '/todolist/')
        self.assertEqual(response.status_code, 400)

    def test_post_data_name_missing_fail(self):
        response = self.client.generic('POST', '/todolist/', json.dumps({
            "description": "LIST1",
            "members": [self.user.id]
        }))
        self.assertEqual(response.status_code, 400)

    def test_post_data_description_missing_pass(self):
        response = self.client.generic('POST', '/todolist/', json.dumps({
            "name": "name1",
            "members": [self.user.id]
        }))
        self.assertEqual(response.status_code, 201)

    def test_post_data_members_missing_pass(self):
        response = self.client.generic('POST', '/todolist/', json.dumps({
            "name": "name1",
            "description": "LIST1"
        }))
        self.assertEqual(response.status_code, 201)

    def test_post_too_long_data_field(self):
        name = "f"*60
        response = self.client.generic('POST', '/todolist/', json.dumps({
            "name": name, "description": "LIST1", "members": [self.user.id]
        }))
        self.assertEqual(response.status_code, 400)

    def test_post_wrong_json(self):
        response = self.client.generic('POST', '/todolist/', '{"name": instance1, ')
        self.assertEqual(response.status_code, 400)

    # Testing PUT method

    def test_put_missing_todo_list_pk(self):
        response = self.client.generic('PUT', '/todolist/', json.dumps({
            "name": "namePUT",
            "description": "LIST1PUT",
            "members": [self.user.id]
        }))
        self.assertEqual(response.status_code, 404)

    def test_put_not_existing_todo_list_pk(self):
        response = self.client.generic('PUT', '/todolist/42/', json.dumps({
            "name": "namePUT",
            "description": "LIST1PUT",
            "members": [self.user.id]
        }))
        self.assertEqual(response.status_code, 404)

    def test_put_wrong_todo_list_pk(self):
        response = self.client.generic('PUT', '/todolist/w/', json.dumps({
            "name": "namePUT",
            "description": "LIST1PUT",
            "members": [self.user.id]
        }))
        self.assertEqual(response.status_code, 404)

    def test_put_no_data(self):
        response = self.client.generic('PUT', '/todolist/10/')
        self.assertEqual(response.status_code, 400)

    def test_put_valid_data(self):
        response = self.client.generic('PUT', '/todolist/10/', json.dumps({
            "name": "namePUT",
            "description": "LIST1PUT",
            "members_to_add": [self.user2.id]
        }))
        self.assertEqual(response.status_code, 200)

    def test_put_wrong_json(self):
        response = self.client.generic('PUT', '/todolist/10/', '{"name": instance1, ')
        self.assertEqual(response.status_code, 400)

    def test_put_too_long_data_field(self):
        name = "f" * 60
        response = self.client.generic('PUT', '/todolist/10/', json.dumps({
            "name": name, "description": "LIST1"
        }))
        self.assertEqual(response.status_code, 400)

    def test_put_members_to_add_pass(self):
        response = self.client.generic('PUT', '/todolist/10/', json.dumps({
            "members_to_add": [2]
        }))
        self.assertEqual(response.status_code, 200)

    def test_put_members_to_delete_pass(self):
        response = self.client.generic('PUT', '/todolist/10/', json.dumps({
            "members_to_delete": [1]
        }))
        self.assertEqual(response.status_code, 200)

    def test_put_members_to_add_fail(self):
        response = self.client.generic('PUT', '/todolist/10/', json.dumps({
            "members_to_delete": 1
        }))
        self.assertEqual(response.status_code, 400)

    def test_put_members_to_delete_fail(self):
        response = self.client.generic('PUT', '/todolist/10/', json.dumps({
            "members_to_delete": "1a"
        }))
        self.assertEqual(response.status_code, 400)

    # Testing DELETE method

    def test_delete_missing_todo_list_pk(self):
        response = self.client.generic('DELETE', '/todolist/')
        self.assertEqual(response.status_code, 404)

    def test_delete_not_existing_todo_list_pk(self):
        response = self.client.generic('DELETE', '/todolist/23/')
        self.assertEqual(response.status_code, 404)

    def test_delete_wrong_todo_list_pk(self):
        response = self.client.generic('DELETE', '/todolist/w/')
        self.assertEqual(response.status_code, 404)

    def test_delete_pass(self):
        response = self.client.generic('DELETE', '/todolist/10/')
        self.assertEqual(response.status_code, 200)
