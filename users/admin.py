from django.contrib import admin

from .models import ValidEmail, EmailPrivilege, UserPrivilege, PrivilegeLookup

admin.site.register(ValidEmail)
admin.site.register(EmailPrivilege)
admin.site.register(UserPrivilege)
admin.site.register(PrivilegeLookup)
