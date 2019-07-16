from django.conf.urls import url
from django.views import View
from django.http import HttpResponse


class TestView(View):
    http_method_names = ['get']

    def get(self, request):
        return HttpResponse()


urlpatterns = [
    url(
        r'^$',
        TestView.as_view(),
    ),
]
