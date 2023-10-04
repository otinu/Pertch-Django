from django import forms
from .models import PetCommentModel


class PetCommentForm(forms.ModelForm):
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
        # required=True, # fields指定をしていれば、requiredは不要?
        widget=forms.TextInput(attrs={"class": "event-text"}),  # HTML側でのclass属性を追加
    )

    event_information = forms.CharField(
        label="情報",
        widget=forms.Textarea(attrs={"class": "event-textarea"}),
        max_length=200,
    )

    class Meta:
        model = PetCommentModel
        fields = ("event_time", "event_place", "event_information")
