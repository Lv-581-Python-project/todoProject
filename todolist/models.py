from django.db import models

from custom_user.models import CustomUser


class ToDoList(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500, default='No description for now.')

    members = models.ManyToManyField(CustomUser, related_name='todo_lists')

    def __str__(self):
        return self.name

    def to_dict(self):
        return {'name': self.name,
                'description': self.description,
                #'members': self.members
               }

    @classmethod
    def get_by_id(cls, todo_list_pk: int):
        try:
            todo_list = ToDoList.objects.get(pk=todo_list_pk)
            return todo_list
        except ToDoList.DoesNotExist:
            return None

    @classmethod
    def get_all(cls):
        try:
            todo_lists = ToDoList.objects.all()
            return todo_lists
        except ToDoList.DoesNotExist:
            return None

    @classmethod
    def create(cls, name: str, description: str, member_pk):
        todo_list = ToDoList(name=name, description=description)
        todo_list.save()
        member_to_add = CustomUser.find_by_id(user_id=member_pk)
        todo_list.members.add(member_to_add)
        todo_list.save()
        return todo_list

    @classmethod
    def update(cls, todo_list_pk: int, data: dict):
        todo_list = cls.get_by_id(todo_list_pk)
        if todo_list:
            for field, value in data.items():
                if hasattr(todo_list, field):
                    setattr(todo_list, field, value)
                else:
                    raise KeyError("Failed to update non existing attribute {}.{}".format(
                        todo_list.__class__.__name__, field))
            todo_list.save()
            return cls.get_by_id(todo_list_pk=todo_list_pk)
        return None

    @classmethod
    def remove(cls, todo_list_pk: int):
        todo_list = cls.get_by_id(todo_list_pk=todo_list_pk)
        if todo_list:
            todo_list.delete()
        return not cls.get_by_id(todo_list_pk=todo_list_pk)
