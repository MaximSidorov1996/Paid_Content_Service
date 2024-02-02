import os
from datetime import datetime

from django.core.management import BaseCommand
from dotenv import load_dotenv

from config.settings import BASE_DIR
from content_app.models import Publication, Channel, Subscription, Payment
from users.models import User

dot_env = os.path.join(BASE_DIR, '.env')
load_dotenv(dotenv_path=dot_env)


class Command(BaseCommand):

    def handle(self, *args, **options):
        Publication.objects.all().delete()
        Channel.objects.all().delete()
        Subscription.objects.all().delete()
        User.objects.all().delete()
        Payment.objects.all().delete()
        users_list = [
            {'phone_number': '89771234567', 'is_active': True},
            {'phone_number': '89254956395', 'is_active': True},
            {'phone_number': '89253343444', 'is_active': True},
            {'phone_number': '89478906390', 'is_active': True},
            {'phone_number': '89051232345', 'is_active': True},
        ]
        user_ids = []
        for user in users_list:
            new_user = User.objects.create(**user)
            new_user.set_password('qwerty')
            new_user.save()
            user_ids.append(new_user.id)

        channels_list = [
            {'owner': user_ids[0], 'title': 'ФлористикаChannel',
             'description': 'Этот канал посвящен флористике и интересным '
                            'исследованиям на тему жизненного цикла цветов.'
             },
            {'owner': user_ids[1], 'title': 'MrPilsner',
             'description': 'Канал о пиве'
             },
            {'owner': user_ids[2], 'title': 'MsPainter',
             'description': 'Творчество'
             },
            {'owner': user_ids[3], 'title': 'Singer',
             'description': 'Профессиональные каверы на популярные шлягеры',
             },
            {'owner': user_ids[4], 'title': 'OlegCat',
             'description': 'Канал посвящен моему коту Олегу и его жизни'
             },
        ]
        channels_ids = []
        for channel in channels_list:
            new_channel = Channel.objects.create(
                                    owner=User.objects.get(pk=channel['owner']),
                                    title=channel['title'],
                                    description=channel['description'])
            channels_ids.append(new_channel.id)

        publications_list = [
            {'owner': user_ids[0], 'channel': channels_ids[0], 'title': 'Тюльпаны',
             'content': 'Так люблю тюльпаны', 'image': 'fill/flower.jpeg',
             'is_free': True
             },
            {'owner': user_ids[1], 'channel': channels_ids[1], 'title': 'Лагер',
             'content': 'Так люблю пиво', 'image': 'fill/beer.jpg',
             'is_free': True
             },
            {'owner': user_ids[4], 'channel': channels_ids[4], 'title': 'Знакомьтесь, мой кот Олег',
             'content': '', 'image': 'fill/cat.jpeg',
             'is_free': True
             },
            {'owner': user_ids[2], 'channel': channels_ids[2], 'title': 'Рисунки только в платном разделе <3',
             'content': '', 'image': '', 'is_free': True
             },

        ]
        for publication in publications_list:
            new_publication = Publication.objects.create(
                owner=User.objects.get(pk=publication['owner']),
                channel=Channel.objects.get(pk=publication['channel']),
                title=publication['title'],
                content=publication['content'],
                is_free=publication['is_free'],
                image=publication['image']
            )
