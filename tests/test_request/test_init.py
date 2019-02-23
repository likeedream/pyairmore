import ipaddress
import unittest
import urllib3.util.url

import pyairmore.request

from tests import HTTPrettyTestCase
from tests.test_request import AirmoreRequestTestCase


class TestAirmoreRequest:
    @classmethod
    def setup_class(cls):
        cls.session = pyairmore.request.AirmoreSession(
            ipaddress.IPv4Address("127.0.0.1")
        )

    def setup_method(self):
        self.request = pyairmore.request.AirmoreRequest(self.session)

    def test_method(self):
        self.request.prepare_method("get")
        assert self.request.method == "POST"

        self.request.prepare_method("whatever")
        assert self.request.method == "POST"

        self.request.prepare_method("post")
        assert self.request.method == "POST"

    def test_prepare_url_contains_base_url(self):
        self.request.prepare_url("/foo", {})
        assert (
            self.session.base_url
            == self.request.url[: len(self.session.base_url)]
        )

    def test_prepare_url_without_params(self):
        self.request.prepare_url("/foo", {})
        assert self.request.url == self.session.base_url + "/foo"

    def test_prepare_url_with_params(self):
        self.request.prepare_url("/", {"foo": "bar"})
        assert self.request.url == self.session.base_url + "/?foo=bar"


class TestApplicationOpenRequest(AirmoreRequestTestCase):
    request_class = pyairmore.request.ApplicationOpenRequest

    def test_url(self):
        assert self.request.url.endswith("/?Key=PhoneCheckAuthorization")


class AirmoreSessionTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.session = pyairmore.request.AirmoreSession(
            ipaddress.IPv4Address("127.0.0.1")
        )

    def test_is_server_running(self):
        setattr(self.session, "is_mocked", True)
        self.assertTrue(self.session.is_server_running)

    def test_is_application_open(self):
        self.assertTrue(self.session.is_application_open)

    def test_request_authorization(self):
        self.assertTrue(self.session.request_authorization())

    def test_base_url_scheme(self):
        parsed = urllib3.util.url.parse_url(self.session.base_url)
        self.assertEqual(parsed.scheme, "http")

    def test_base_url_hostname(self):
        parsed = urllib3.util.url.parse_url(self.session.base_url)
        self.assertEqual(parsed.hostname, "127.0.0.1")

    def test_base_url_port(self):
        parsed = urllib3.util.url.parse_url(self.session.base_url)
        self.assertEqual(parsed.port, 2333)
