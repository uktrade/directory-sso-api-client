from django.conf.urls import url
from django.http import HttpResponse
from django.views import View


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
