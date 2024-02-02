from django import forms

from content_app.models import Channel, Publication, Subscription


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ChannelForm(StyleFormMixin, forms.ModelForm):
    # image = forms.ImageField(attrs={'enctype="multipart/form-data"'}
    class Meta:
        model = Channel
        fields = ('title', 'description', 'image',)


class PublicationForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = ('title', 'content', 'image', 'is_free')


