from io import StringIO
import http
from unittest import TestCase

import requests

from tests import stub_request
from directory_sso_api_client.base import BaseAPIClient


class BaseAPIClientTest(TestCase):

    def setUp(self):
        self.client = BaseAPIClient(
            base_url='https://example.com', api_key='test'
        )

    @stub_request('https://example.com/test', 'post')
    def test_request(self, stub):
        self.client.request("POST", 'test', data='data')

    @stub_request('https://example.com/test', 'post')
    def test_post_encodes_json(self, stub):
        data = {'key': 'value'}
        self.client.post('test', data=data)
        request = stub.request_history[0]
        assert request.headers['Content-type'] == 'application/json'
        assert request.text == '{"key": "value"}'

    @stub_request('https://example.com/test', 'put')
    def test_put_encodes_json(self, stub):
        data = {'key': 'value'}
        self.client.put('test', data=data)
        request = stub.request_history[0]
        assert request.headers['Content-type'] == 'application/json'
        assert request.text == '{"key": "value"}'

    @stub_request('https://example.com/test', 'patch')
    def test_patch_encodes_json_without_file(self, stub):
        data = {'key': 'value'}
        self.client.patch('test', data=data)
        request = stub.request_history[0]
        assert request.headers['Content-type'] == 'application/json'
        assert request.text == '{"key": "value"}'

    @stub_request('https://example.com/thing/', 'patch')
    def test_patch_encodes_form_with_file(self, stub):
        data = {'key': 'value'}
        files = {'logo': StringIO('hello')}
        self.client.patch(url='thing/', data=data, files=files)
        request = stub.request_history[0]
        assert request.headers['Content-type'] == 'multipart/form-data'

    def test_sign_request(self):
        url = 'https://example.com'
        prepared_request = requests.Request(
            "POST", url, data='data'
        ).prepare()

        self.client.sign_request(
            api_key='test',
            prepared_request=prepared_request,
        ),

    @stub_request('https://example.com', 'post')
    def test_send_response_ok(self, stub):
        response = self.client.send(
            api_key="test", method="POST", url="https://example.com",
        )
        assert response.status_code == http.client.OK

    @stub_request('https://example.com', 'post', http.client.BAD_REQUEST)
    def test_send_response_not_ok(self, stub):
        response = self.client.send(
            api_key="test", method="POST", url="https://example.com",
        )
        assert response.status_code == http.client.BAD_REQUEST
