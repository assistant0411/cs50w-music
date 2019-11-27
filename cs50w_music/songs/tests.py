from django.test import Client, TestCase
from rest_framework import status


class IndexTest(TestCase):
    def test_index(self):

        # Set up client to make requests
        c = Client()

        # Send get request to index page and store response
        response = c.get("/")

        # Make sure status code is 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Make sure three flights are returned in the context
        #self.assertEqual(response.context["flights"].count(), 3)