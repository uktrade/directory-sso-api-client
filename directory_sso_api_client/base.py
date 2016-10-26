from hashlib import sha256
import json
import logging
import urllib.parse as urlparse

from monotonic import monotonic
import requests

from directory_sso_api_client.version import __version__


logger = logging.getLogger(__name__)


class BaseAPIClient:
    def __init__(self, base_url=None, api_key=None):

        assert base_url, "Missing base url"
        assert api_key, "Missing API key"
        self.base_url = base_url
        self.api_key = api_key

    def put(self, url, data, headers=None):
        return self.request(
            url=url,
            method="PUT",
            content_type="application/json",
            data=json.dumps(data)
        )

    def patch(self, url, data, files=None, headers=None):
        if files:
            response = self.request(
                url=url,
                method="PATCH",
                content_type="multipart/form-data",
                data=data,
                files=files,
            )
        else:
            response = self.request(
                url=url,
                method="PATCH",
                content_type="application/json",
                data=json.dumps(data),
            )
        return response

    def get(self, url, params=None, headers=None):
        return self.request(url=url, method="GET", params=params)

    def post(self, url, data):
        return self.request(
            url=url,
            method="POST",
            content_type="application/json",
            data=json.dumps(data),
        )

    def delete(self, url, data=None, headers=None):
        return self.request(url=url, method="DELETE")

    def request(
        self, method, url, content_type=None, data=None, params=None,
        files=None, headers=None
    ):
        if not headers:
            headers = {}

        logger.debug("API request {} {}".format(method, url))

        headers["User-agent"] = "EXPORT-DIRECTORY-SSO-API-CLIENT/{}".format(
            __version__
        )
        if content_type:
            headers["Content-type"] = content_type

        url = urlparse.urljoin(self.base_url, url)

        start_time = monotonic()

        try:
            return self.send(
                api_key=self.api_key,
                method=method,
                url=url,
                headers=headers,
                data=data,
                params=params,
                files=files,
            )
        finally:
            elapsed_time = monotonic() - start_time
            logger.debug(
                "API {} request on {} finished in {}".format(
                    method, url, elapsed_time
                )
            )

    def sign_request(self, api_key, url, prepared_request):
        url = urlparse.urlsplit(url)
        path = bytes(url.path, "utf-8")

        if url.query:
            path += bytes("?{}".format(url.query), "utf-8")

        salt = bytes(api_key, "utf-8")
        body = prepared_request.body or b""

        if isinstance(body, str):
            body = bytes(body, "utf-8")

        signature = sha256(path + body + salt).hexdigest()
        prepared_request.headers["X-Signature"] = signature

        return prepared_request

    def send(self, api_key, method, url, request=None, *args, **kwargs):

        prepared_request = requests.Request(
            method, url, *args, **kwargs
        ).prepare()

        signed_request = self.sign_request(
            api_key=api_key,
            url=url,
            prepared_request=prepared_request,
        )
        return requests.Session().send(signed_request)
