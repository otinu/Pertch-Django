from datetime import datetime

from django import forms
from .models import PetModel, PetCommentModel
from django.utils import timezone


class PetCommentForm(forms.ModelForm):
    reuqired_message = "入力が必要です"

    event_time = forms.DateTimeField(
        label="時間",
        widget=forms.DateTimeInput(
            attrs={
                "type": "datetime-local",
                "class": "event-text",
            }
        ),
        input_formats=["%Y-%m-%dT%H:%M"],
    )

    event_place = forms.CharField(
        label="場所",
        max_length=80,  # max_lengthを超過した入力は受け付けなくなる
        required=True,
        error_messages={"required": reuqired_message},
        widget=forms.TextInput(attrs={"class": "event-text"}),  # HTML側でのclass属性を追加
    )

    event_information = forms.CharField(
        label="情報",
        widget=forms.Textarea(attrs={"class": "event-textarea"}),
        max_length=200,
        required=True,
        error_messages={"required": reuqired_message},
    )

    class Meta:
        model = PetCommentModel
        fields = ("event_time", "event_place", "event_information")
        labels = {"event_time": "日時", "event_place": "場所", "event_information": "情報"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["event_time"].required = True
        self.fields["event_place"].required = True
        self.fields["event_information"].required = True
