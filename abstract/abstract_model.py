from abc import abstractmethod

from django.db import models


class AbstractModel(models.Model):

    class Meta:
        abstract = True

    @classmethod
    def get_by_id(cls, pk: int):
        try:
            entity = cls.objects.get(pk=pk)
            return entity
        except cls.DoesNotExist:
            return None

    @classmethod
    def get_all(cls):
        try:
            task = cls.objects.all()
            return task
        except cls.DoesNotExist:
            return None

    @classmethod
    def remove(cls, pk):
        try:
            task = cls.objects.get(id=pk)
            task.delete()
        except cls.DoesNotExist:
            return False
        return True

    @abstractmethod
    def update(self, *args, **kwargs):
        raise NotImplemented

    @classmethod
    @abstractmethod
    def create(cls, *args, **kwargs):
        raise NotImplemented
