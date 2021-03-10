from django.shortcuts import render
from django.views.generic import DetailView, FormView, DeleteView, ListView
from django.http import JsonResponse

from .models import User
from lists.models import ToDoList


class ProfileView(DetailView):
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        lists = ToDoList.objects.filter(user_id=user.pk)
        context['lists'] = lists
        context['user'] = user
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        data = self.get_context_data(object=self.object)
        if self.request.GET:
            return JsonResponse(data)
