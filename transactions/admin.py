from django.contrib import admin
from.models import AccountDetails, User, UserBalance

admin.site.register(User)
admin.site.register(AccountDetails)
admin.site.register(UserBalance)
