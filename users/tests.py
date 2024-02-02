from django.test import TestCase

from users.management.commands.createadmin import Command
from users.models import User


class CreateUserTestCase(TestCase):

    def setUp(self):
        args = {'createadmin'}
        Command.handle(*args)

    def test_command(self):
        self.assertTrue(User.objects.get(phone_number=1234))


class RegisterTestCase(TestCase):
    def test_register_page(self):
        response = self.client.get(f'/users/')
        self.assertEqual(response.status_code, 200)


