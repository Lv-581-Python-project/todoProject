from django.http import HttpResponse

import json


class JSONMiddleware:
    """
    Process application/json requests data from GET and POST requests.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST' or request.method == 'PUT':
            try:
                request._body = json.loads(request.body)
                return self.get_response(request)
            except json.JSONDecodeError:
                return HttpResponse("Invalid JSON", status=400)
        else:
            response = self.get_response(request)
            return response
