from django import forms
from .models import PetModel


class PetForm(forms.ModelForm):
    name = forms.CharField(
        label="名前",
        min_length=2,
        max_length=20,
        widget=forms.TextInput(attrs={"id": "name"}),
    )

    age = forms.IntegerField(
        label="年齢",
        min_value=0,
        max_value=99,
        widget=forms.NumberInput(attrs={"id": "age"}),
    )

    sex_list = [(True, "♂"), (False, "♀")]
    sex = forms.BooleanField(
        label="性別",
        initial=[True],
        # choices=sex_list,
        widget=forms.RadioSelect(
            attrs={"class": "radio-button"},
            choices=[
                (True, "♂"),
                (False, "♀"),
            ],
        ),
    )

    image = forms.ImageField(
        label="写真",
        required=False,
    )

    charm_point = forms.CharField(
        label="特徴", widget=forms.Textarea(), max_length=1000, required=False
    )

    post_cord = forms.IntegerField(
        label="郵便番号",
        widget=forms.NumberInput(
            attrs={"id": "post-cord", "placeholder": "7桁でご入力ください"}
        ),
    )

    address = forms.CharField(
        label="住所",
        max_length=50,
        widget=forms.TextInput(attrs={"id": "address"}),
        required=False,
    )

    class Meta:
        model = PetModel
        fields = ("name", "age", "sex", "charm_point", "post_cord", "address", "image")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_post_cord(self):
        post_cord = self.cleaned_data["post_cord"]
        if len(str(post_cord)) != 7:
            raise forms.ValidationError("エラーが発生しました。郵便番号は7桁でご入力ください")
        return post_cord
