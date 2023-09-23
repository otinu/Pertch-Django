import datetime

from django.db import models
from django.core.validators import MinLengthValidator

from petApp.models import PetModel


class PetCommentModel(models.Model):
    class Meta:
        db_table = "pet_comment"

    event_time = models.CharField(validators=[MinLengthValidator(16)], max_length=18)
    event_place = models.CharField(max_length=80)
    event_information = models.CharField(max_length=200)

    now = datetime.datetime.now()
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(default=now)

    # Pet:PetComment で 1:N の関係
    pet = models.ForeignKey(PetModel, on_delete=models.CASCADE)
