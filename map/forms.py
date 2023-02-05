from django import forms
from django.contrib.auth.models import User
from map.models import Map


class MapForm(forms.ModelForm):

    class Meta:
        model = Map
        fields = [
                "category",
                "name",
                "description",
                "image",
                "thumbnail",
                "pub_date",
                "maker",
                ]

    def clean_maker(self):
        if not self.cleaned_data['maker']:
            return User()
        return self.cleaned_data['maker']

    def clean_last_modified_by(self):
        if not self.cleaned_data['last_modified_by']:
            return User()
        return self.cleaned_data['last_modified_by']
