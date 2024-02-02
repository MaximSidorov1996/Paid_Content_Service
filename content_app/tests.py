from django.test import TestCase

from content_app.management.commands.fill import Command
from content_app.models import Channel, Subscription
from users.models import User


class ChannelTestCase(TestCase):
    def setUp(self):
        self.auth_user = User.objects.create(phone_number='8904567464', password='test', is_active=True)
        self.channel = Channel.objects.create(
                                              owner=self.auth_user,
                                              title='test_channel',
                                              description='test_description')

    def test_auth_get(self):
        response = self.client.get('/channels/')
        response2 = self.client.get(f'/channels/{self.channel.id}')
        response3 = self.client.get(f'/channels/5')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['object_list']) == 1)
        self.assertFalse(len(response.context['object_list']) == 0)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response3.status_code, 404)


class SubscriptionTestCase(TestCase):
    def setUp(self):
        self.auth_user = User.objects.create(phone_number='8904567464', password='test', is_active=True)
        self.channel = Channel.objects.create(
            title='test_channel',
            description='test_description')
        self.subscription = Subscription.objects.create(user_id=self.auth_user.id,
                                                        channel_id=self.channel.id,
                                                        subscription_status=True)

    def test_subscription(self):
        self.assertTrue(Subscription.objects.get(id=self.subscription.id).subscription_status == True)


class FillTestCase(TestCase):

    def setUp(self):
        args = {'fill'}
        Command.handle(*args)

    def test_command(self):
        self.assertTrue(User.objects.get(phone_number=89771234567))
        self.assertTrue(Channel.objects.get(title='ФлористикаChannel'))



