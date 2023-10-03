from datetime import datetime

from django import forms
from .models import PetModel, PetCommentModel


class PetCommentForm(forms.ModelForm):
    reuqired_message = "入力が必要です"

    event_time = forms.DateTimeInput(
        format="%d/%m/%Y %H:%M", attrs={"type": "datetime-local", "class": "event-text"}
    )

    event_place = forms.CharField(
        max_length=80,  # max_lengthを超過した入力は受け付けなくなる
        required=True,
        error_messages={"required": reuqired_message},
        label="場所",
        widget=forms.TextInput(attrs={"class": "event-text"}),  # class属性を追加
    )

    event_information = forms.CharField(
        widget=forms.Textarea(attrs={"class": "event-textarea"}),
        max_length=200,
        required=True,
        error_messages={"required": reuqired_message},
    )

    # 登録日時
    created_at = forms.DateTimeField()
    # 更新日時
    updated_at = forms.DateTimeField()

    class Meta:
        model = PetCommentModel
        fields = "__all__"
        labels = {"event_time": "日時", "event_place": "場所", "event_information": "情報"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["event_time"].required = True
        self.fields["event_place"].required = True
        self.fields["event_information"].required = True
        self.fields["pet"] = forms.ModelChoiceField(queryset=PetModel.objects.none())


"""
    def clean_event_time(self):
        value = self.cleaned_data["event_time"]
        return value

    def clean_event_place(self):
        value = self.cleaned_data["event_place"]
        
        if len(value) > 81:
            raise forms.ValidationError(
                "",
            )
"""
