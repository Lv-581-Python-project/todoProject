from django.db import models, IntegrityError, DatabaseError

from utils.abstract_model import AbstractModel
from custom_user.models import CustomUser


class ToDoList(AbstractModel):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500, default='No description for now.')
    members = models.ManyToManyField(CustomUser, related_name='todo_lists')

    def __str__(self):
        return self.name

    def to_dict(self):
        return {'id': self.id,
                'name': self.name,
                'description': self.description,
                'members': sorted([member.id for member in self.members.all()])}

    def update(self, name=None, description=None):
        try:
            if name:
                self.name = name
            if description:
                self.description = description
            self.save()
            return self
        except (ValueError, IntegrityError, DatabaseError):
            return None

    def update_members(self, members_to_add=None, members_to_delete=None):
        try:
            if members_to_add:
                self.members.add(*members_to_add)
            if members_to_delete:
                self.members.remove(*members_to_delete)
            return self
        except (TypeError, ValueError):
            return None

    def get_list_members(self):
        members = self.members.all()
        return members

    @classmethod
    def create(cls, name, description='', members=None):
        try:
            todo_list = ToDoList(name=name, description=description)
            todo_list.save()
            if members:
                todo_list.members.add(*members)
            return todo_list
        except (ValueError, IntegrityError, DatabaseError):
            # log error
            return None
