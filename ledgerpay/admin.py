from django.contrib import admin
from django.contrib.admin import AdminSite
from ledger.accounts.models import EmailUser
from ledger.accounts import admin as ledger_admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from copy import deepcopy

from ledgerpay import forms
from ledgerpay.main_models import SystemMaintenance


class LedgerPayAdminSite(AdminSite):
    site_header = 'Ledger Pay Administration'
    site_title = 'Ledger Pay System'
    index_title = 'Ledger Pay System'


ledgerpay_admin_site = LedgerPayAdminSite(name='ledgerpayadmin')


admin.site.unregister(EmailUser) # because this base classAdmin alsready registered in ledger.accounts.admin


@admin.register(EmailUser)
class EmailUserAdmin(ledger_admin.EmailUserAdmin):
    """
    Overriding the EmailUserAdmin from ledger.accounts.admin, to remove is_superuser checkbox field on Admin page
    """

    def get_fieldsets(self, request, obj=None):
        """ Remove the is_superuser checkbox from the Admin page, if user is DisturbanceAdmin and NOT superuser """
        fieldsets = super(UserAdmin, self).get_fieldsets(request, obj)
        if not obj:
            return fieldsets

        if request.user.is_superuser:
            return fieldsets

        group = Group.objects.filter(name='Disturbance Admin')
        if group and group[0] in request.user.groups.all():
            fieldsets = deepcopy(fieldsets)
            for fieldset in fieldsets:
                if 'is_superuser' in fieldset[1]['fields']:
                    if type(fieldset[1]['fields']) == tuple :
                        fieldset[1]['fields'] = list(fieldset[1]['fields'])
                    fieldset[1]['fields'].remove('is_superuser')
                    break

        return fieldsets


@admin.register(SystemMaintenance)
class SystemMaintenanceAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'start_date', 'end_date', 'duration']
    ordering = ('start_date',)
    readonly_fields = ('duration',)
    form = forms.SystemMaintenanceAdminForm
