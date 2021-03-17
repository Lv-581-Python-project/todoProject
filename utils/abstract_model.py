from abc import abstractmethod

from django.db import models


class AbstractModel(models.Model):
    objects = models.Manager()

    class Meta:
        abstract = True

    @classmethod
    def get_by_id(cls, pk: int):  # pylint: disable=C0103
        try:
            entity = cls.objects.get(pk=pk)
            return entity
        except cls.DoesNotExist:
            return None

    @classmethod
    def get_all(cls):
        task = cls.objects.all()
        return task

    @classmethod
    def remove(cls, pk):  # pylint: disable=C0103
        try:
            task = cls.objects.get(id=pk)
            task.delete()
        except cls.DoesNotExist:
            return False
        return True

    @abstractmethod
    def update(self, *args, **kwargs):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def create(cls, *args, **kwargs):
        raise NotImplementedError
