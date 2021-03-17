from abc import abstractmethod
from datetime import date
from django.db import models, IntegrityError, DataError
from custom_user.models import CustomUser
from todolist.models import ToDoList
from utils.abstract_model import AbstractModel


class Task(AbstractModel):
    title = models.CharField(max_length=30)
    description = models.TextField(max_length=256, default="")
    is_completed = models.BooleanField(default=False)
    deadline = models.DateField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    todolist = models.ForeignKey(ToDoList, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    @classmethod
    def get_by_list_id(cls,todolist: ToDoList):
        tasks = Task.objects.filter(todolist_id=todolist.pk)
        return tasks

    @classmethod
    def create(cls,
               title: str,
               description: str,
               deadline: date,
               user: CustomUser,
               todolist: ToDoList):  # pylint disable=W0221
        task = Task(title=title, description=description, deadline=deadline)
        task.user = user
        task.todolist = todolist
        try:
            task.save()
            return task
        except (ValueError, DataError, IntegrityError):
            return None

    @abstractmethod
    def update(self,
               title: str,
               description: str,
               is_completed: bool,
               deadline: date,
               user: CustomUser,
               todolist: ToDoList):  # pylint disable=W0221
        try:
            if title:
                self.title = title
            if description:
                self.description = description
            if deadline:
                self.deadline = deadline
            if is_completed:
                self.is_completed = is_completed
            if user:
                self.user = user
            if todolist:
                self.todolist = todolist
            self.save()
            return True
        except (ValueError, DataError, TypeError, IntegrityError):
            return None
