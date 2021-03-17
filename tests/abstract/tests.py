from django.test import TestCase
from utils.abstract_model import AbstractModel


class TaskModelsTest(TestCase):
    def test_not_implemented_update(self):
        class TestModel(AbstractModel):
            class Meta:
                abstract = True

        self.assertRaises(NotImplementedError, TestModel.update, 'test')

    def test_not_implemented_create(self):
        class TestModel(AbstractModel):
            class Meta:
                abstract = True

        self.assertRaises(NotImplementedError, TestModel.create, 'test')
