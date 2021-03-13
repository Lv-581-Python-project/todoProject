from django.db import models, IntegrityError

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
                'members': self.members.all()}

    def update(self, data):
        if data.name:
            self.name = data.name
        if data.description:
            self.description = data.description
        self.save()

    def update_members(self, members_to_add=None, members_to_delete=None):
        if members_to_add:
            self.members.add(*members_to_add)
        if members_to_delete:
            self.members.remove(*members_to_delete)

    def get_list_members(self):
        members = self.members.all()
        return members

    @classmethod
    def get_by_id(cls, todo_list_pk):
        try:
            todo_list = ToDoList.objects.get(pk=todo_list_pk)
            return todo_list
        except ToDoList.DoesNotExist:
            # log error
            return None

    @classmethod
    def get_all(cls):
        todo_lists = ToDoList.objects.all()
        return todo_lists

    @classmethod
    def create(cls, name, description='', members=None):
        todo_list = ToDoList(name=name, description=description)
        try:
            todo_list.save()
            if members:
                todo_list.members.add(*members)
            return todo_list
        except (ValueError, IntegrityError):
            # log error
            return None

    @classmethod
    def remove(cls, todo_list_pk):
        todo_list = ToDoList.objects.get(pk=todo_list_pk)
        todo_list.delete()
