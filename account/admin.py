from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from account.models import Account

class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'date_joined', 'last_login', 'is_admin', 'is_staff')
    search_fields = ('email', 'username', 'last_login')
    readonly_fields = ('id', 'date_joined', 'last_login')

    filter_horizontal = ()      #если не нужены фитры, можно пустым
    list_filter = ()            #если не нужены фитры, можно пустым
    fieldsets = ()              #если не нужены фитры, можно пустым

admin.site.register(Account, AccountAdmin)