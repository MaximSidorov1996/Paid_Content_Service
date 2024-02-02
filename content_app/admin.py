from django.contrib import admin

from content_app.models import Channel, Publication, Subscription


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ['title', ]


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ['title', ]


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'channel_id', 'subscription_status', ]
