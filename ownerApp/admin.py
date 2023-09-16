from django.contrib import admin
from django.contrib.auth import get_user_model

Owner = get_user_model()
admin.site.register(Owner)
