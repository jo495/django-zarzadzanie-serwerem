from django.contrib import admin
from .models import Button, Customer

admin.site.register(Customer)
@admin.register(Button)

class ButtonAdmin(admin.ModelAdmin):
    list_display = ('title', 'isOn', 'command', 'accessLevel')
    list_filter = list_display
    ordering = ('isOn',)