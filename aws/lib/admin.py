from django.contrib import admin
from lib import models


class AWSCommandResponseAdmin(admin.ModelAdmin):
    list_display = ['id', 'date', 'command', ]
    search_fields = ['id', 'date', 'command', ]


admin.site.register(models.AWSCommandResponse, AWSCommandResponseAdmin)


