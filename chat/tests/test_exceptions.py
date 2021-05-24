from django.test import TestCase
from rest_framework.exceptions import NotFound, APIException, server_error, ParseError

from chat.exceptions import get_response, get_error_message, exception_handler, handle_exception
from rest_framework.views import exception_handler


class ExceptionsTest(TestCase):
    def test_get_response(self):
        message = "error"
        status_code = 400
        status = False

        error_response = {
            "message": message,
            "status_code": status_code,
            "status": status
        }

        self.assertEqual(error_response, get_response(message, status, status_code))

    def test_exception_handler(self):
        response_404 = exception_handler(NotFound(), None)
        response_400 = exception_handler(ParseError(), None)

        self.assertEqual(404, response_404.status_code)
        self.assertEqual(400, response_400.status_code)

