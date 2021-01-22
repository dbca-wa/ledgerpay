from django.contrib.admin import AdminSite


class LedgerPayAdminSite(AdminSite):
    site_header = 'Ledgerpay Administration'
    site_title = 'Ledgerpay Licensing'

ledgerpay_admin_site = LedgerPayAdminSite(name='ledgerpayadmin')
