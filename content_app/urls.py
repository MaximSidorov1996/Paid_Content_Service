from django.conf.urls.static import static
from django.urls import path

from config import settings
from content_app.apps import ContentAppConfig
from content_app.views import ChannelView, ChannelList, home, ChannelCreate, \
    PublicationView, SubChannelList, PublicationCreate, PublicationEdit, PublicationDelete, ChannelEdit, sub_success

app_name = ContentAppConfig.name

urlpatterns = [
    path('', home, name='home'),
    path('channels/', ChannelList.as_view(template_name='content_app/channel_list.html'), name='channel_list'),
    path('channels/<int:pk>', ChannelView.as_view(), name='channel_view'),
    path('channels/create/', ChannelCreate.as_view(), name='channel_create'),
    path('publication/<int:pk>', PublicationView.as_view(), name='publication_detail'),
    path('subscriptions/', SubChannelList.as_view(template_name='content_app/sub_channels.html'), name='sub_channels'),
    path('publication/create/', PublicationCreate.as_view(), name='publication_create'),
    path('publication/edit/<int:pk>', PublicationEdit.as_view(), name='publication_edit'),
    path('publication/delete/<int:pk>', PublicationDelete.as_view(), name='publication_delete'),
    path('channels/edit/<int:pk>', ChannelEdit.as_view(), name='channel_edit'),
    path('channels/success/', sub_success, name='success'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
