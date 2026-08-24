from typing import ClassVar

from django.http import HttpResponse
from django.urls import re_path
from django.views import View


class TestView(View):
    http_method_names: ClassVar[list[str]] = ["get"]

    def get(self, request):
        return HttpResponse()


urlpatterns = [
    re_path(
        r"^$",
        TestView.as_view(),
    ),
]
