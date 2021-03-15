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


class ToDoListCRUDTest(TestCase):
    def setUp(self) -> None:
        self.user = CustomUser.objects.create(id=1, first_name="TestUser1",
                                              last_name="UserLastName1", email="test1@gmail.com",
                                              password="adminpassword1")
        self.user2 = CustomUser.objects.create(id=2, first_name="TestUser2",
                                               last_name="UserLastName2", email="test2@gmail.com",
                                               password="adminpassword2")

        self.todo_list = ToDoList.objects.create(name="TestList", description="Test description")
        self.todo_list.members.add(self.user.id)

    def test_create(self):
        todo_list1 = ToDoList.create('test list name 1')
        todo_list2 = ToDoList.create(name='test list name 2', description='test list description 2')
        todo_list3 = ToDoList.create(name='test list name 3', description='test list description 3',
                                     members=[self.user, self.user2])

        first_to_dict_expected = {'id': 2, 'name': 'test list name 1', 'description': '', 'members': []}
        second_to_dict_expected = {'id': 3, 'name': 'test list name 2',
                                   'description': 'test list description 2', 'members': []}
        third_to_dict_expected = {'id': 4, 'name': 'test list name 3',
                                  'description': 'test list description 3', 'members': [1, 2]}

        self.assertEqual(first_to_dict_expected, todo_list1.to_dict())
        self.assertEqual(second_to_dict_expected, todo_list2.to_dict())
        self.assertEqual(third_to_dict_expected, todo_list3.to_dict())

    def test_update(self):
        new_name = 'new list name'
        self.todo_list.update(name=new_name)
        self.assertEqual(new_name, self.todo_list.name)

        new_description = 'new list description'
        self.todo_list.update(description=new_description)
        self.assertEqual(new_description, self.todo_list.description)

        new_name, new_description = 'absolutely new list name', 'absolutely new list description'
        self.todo_list.update(name=new_name, description=new_description)
        self.assertEqual(new_name, self.todo_list.name)
        self.assertEqual(new_description, self.todo_list.description)

    def test_get_by_id(self):
        todo_list = ToDoList.get_by_id(self.todo_list.id)
        expected_to_dict = {'id': self.todo_list.id, 'name': 'TestList',
                            'description': 'Test description', 'members': [1]}
        self.assertEqual(expected_to_dict, todo_list.to_dict())

    def test_delete_by_id(self):
        todo_list = ToDoList.get_by_id(self.todo_list.id)
        todo_list.remove()
        todo_list = ToDoList.get_by_id(self.todo_list.id)
        self.assertEqual(None, todo_list)
