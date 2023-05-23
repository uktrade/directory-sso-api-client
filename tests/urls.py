from django.urls import re_path
from django.http import HttpResponse
from django.views import View


class TestView(View):
    http_method_names = ['get']

    def get(self, request):
        return HttpResponse()


urlpatterns = [
    re_path(
        r'^$',
        TestView.as_view(),
    ),
]
