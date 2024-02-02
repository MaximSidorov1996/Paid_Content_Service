from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, request
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from content_app.forms import ChannelForm, PublicationForm
from content_app.models import Publication, Channel, Subscription


class PublicationView(DetailView):
    model = Publication

    def get_context_data(self, **kwargs):
        context = super(PublicationView, self).get_context_data(**kwargs)
        self.object = self.get_object()
        context['channel'] = Channel.objects.get(id=self.object.channel_id)
        return context

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class ChannelEdit(LoginRequiredMixin, UpdateView):
    model = Channel
    form_class = ChannelForm
    success_url = reverse_lazy('content_app:channel_list')


class PublicationCreate(LoginRequiredMixin, CreateView):
    model = Publication
    form_class = PublicationForm

    def form_valid(self, form):
        if form.is_valid:
            self.object = form.save()
            self.object.owner_id = self.request.user.id
            self.object.channel_id = Channel.objects.get(owner_id=self.object.owner_id).id
            self.object.save()
            return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('content_app:channel_list')


class PublicationEdit(LoginRequiredMixin, UpdateView):
    model = Publication
    form_class = PublicationForm
    success_url = reverse_lazy('content_app:channel_list')


class PublicationDelete(LoginRequiredMixin, DeleteView):
    model = Publication
    success_url = reverse_lazy('content_app:channel_list')


class ChannelList(ListView):
    model = Channel

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        try:
            context['owner'] = Channel.objects.get(owner_id=request.user.id)
            return self.render_to_response(context)
        except Channel.DoesNotExist:
            return self.render_to_response(context)


class SubChannelList(LoginRequiredMixin, ListView):
    model = Channel

    def get_queryset(self):
        user = self.request.user
        channels_ids = [i['channel_id'] for i in list(Subscription.objects.filter(
                                                                                  user_id=user.id,
                                                                                  subscription_status=True
                                                                                 ).values('channel_id'))]
        queryset = Channel.objects.filter(id__in=channels_ids)
        return queryset


class ChannelCreate(LoginRequiredMixin, CreateView):
    model = Channel
    form_class = ChannelForm
    success_url = reverse_lazy('content_app:channel_list')

    def form_valid(self, form):
        if form.is_valid:
            self.object = form.save()
            self.object.owner = self.request.user
            self.object.save()
            Subscription.objects.create(user_id=self.request.user.id, channel_id=self.object.id, subscription_status=True)
            return super().form_valid(form)


class ChannelView(DetailView):
    model = Channel

    def get_context_data(self, **kwargs):
        context = super(ChannelView, self).get_context_data(**kwargs)
        context['followers'] = Subscription.objects.filter(
                                                        channel_id=self.get_object().id).filter(
                                                        subscription_status=True).count()
        context['publications_count'] = Publication.objects.filter(
                                                        channel_id=self.get_object().id).count()
        if self.request.user.is_active or self.request.user.is_staff:
            context['publications'] = Publication.objects.filter(channel_id=self.get_object().id)
        else:
            context['publications'] = Publication.objects.filter(
                                                                channel_id=self.get_object().id).filter(
                                                                is_free=True)
        try:
            context['subscription'] = Subscription.objects.get(
                                                            user_id=self.request.user.id,
                                                            channel_id=self.get_object().id).__dict__[
                                                                'subscription_status'
                                                            ]
            return context
        except Exception:
            return context

    def post(self, request, **kwargs):
        self.object = self.get_object()
        if request.POST.get('button'):
            user = request.user
            try:
                subscription = Subscription.objects.get(user_id=user.id, channel_id=self.object.id)
                if subscription.__dict__['subscription_status']:
                    subscription.subscription_status = False
                    subscription.save()
                else:
                    subscription.subscription_status = True
                    subscription.save()
                return redirect('content_app:success')
            except Exception:
                Subscription.objects.create(user_id=user.id, channel_id=self.object.id, subscription_status=True)
                return redirect('content_app:success')
        context = self.get_context_data(object=self.object)
        return render(request, context)


def home(request):
    channels = Channel.objects.order_by('?')[:3]
    publications = Publication.objects.filter(is_free=True).order_by('?')[:3]
    context = {
        'channels': channels,
        'publications': publications
    }
    return render(request, 'content_app/home.html', context)


def sub_success(request):
    if request.method == 'GET':
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
