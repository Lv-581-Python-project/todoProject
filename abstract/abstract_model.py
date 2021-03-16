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

    def create(self, *args, **kwargs):
        raise NotImplemented

    def delete(self, *args, **kwargs):
        raise NotImplemented
