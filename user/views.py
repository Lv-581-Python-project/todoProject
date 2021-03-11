from django.views.generic import DetailView
from django.http import JsonResponse

from .models import CustomUser
from lists.models import List


class ProfileView(DetailView):
    model = CustomUser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        lists = List.objects.filter(user_id=user.pk)
        context['lists'] = lists
        context['user'] = user
        return context

    def get(self, request, *args, **kwargs):
        data = self.get_context_data()
        if self.request.GET:
            return JsonResponse(data)
