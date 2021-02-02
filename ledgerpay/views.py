from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from ledgerpay.forms import LoginForm
from ledgerpay.helpers import is_internal


class LedgerPayRoutingView(TemplateView):
    template_name = 'ledgerpay/index.html'

    def get(self, *args, **kwargs):
        web_url = self.request.META.get('HTTP_HOST', None)
        # only send internal users to login page
        # if self.request.user.is_authenticated():
        #     if is_internal(self.request):
        if self.request.user.is_authenticated() and is_internal(self.request):
            return redirect('internal')
        elif web_url and '-internal' in web_url:
            kwargs['form'] = LoginForm
            return super(LedgerPayRoutingView, self).get(*args, **kwargs)
        else:
            return redirect('external')


class InternalView(UserPassesTestMixin, TemplateView):
    template_name = 'ledgerpay/dash/index.html'

    def test_func(self):
        return is_internal(self.request)

    def get_context_data(self, **kwargs):
        context = super(InternalView, self).get_context_data(**kwargs)
        context['dev'] = settings.DEV_STATIC
        context['dev_url'] = settings.DEV_STATIC_URL
        context['build_tag'] = settings.BUILD_TAG
        if hasattr(settings, 'DEV_APP_BUILD_URL') and settings.DEV_APP_BUILD_URL:
            context['app_build_url'] = settings.DEV_APP_BUILD_URL
        return context


class ExternalView(TemplateView):
    template_name = 'ledgerpay/dash/index.html'

    def get_context_data(self, **kwargs):
        context = super(ExternalView, self).get_context_data(**kwargs)
        context['dev'] = settings.DEV_STATIC
        context['dev_url'] = settings.DEV_STATIC_URL
        context['build_tag'] = settings.BUILD_TAG
        if hasattr(settings, 'DEV_APP_BUILD_URL') and settings.DEV_APP_BUILD_URL:
            context['app_build_url'] = settings.DEV_APP_BUILD_URL
        return context
