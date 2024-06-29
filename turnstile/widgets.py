from urllib.parse import urlencode
from django import forms
from django.utils.html import format_html
from django.template import loader
from django.utils.safestring import mark_safe
from turnstile.settings import JS_API_URL, SITEKEY


class TurnstileWidget(forms.Widget):
    template_name = 'turnstile/forms/widgets/turnstile_widget.html'
    cf_turnstile_response = 'cf-turnstile-response'

    def __init__(self, *args, **kwargs):
        self.extra_url = kwargs.pop('extra_url', {})
        super().__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        final_attrs = self.build_attrs(attrs)

        context = {
            'name': name,
            'value': value,
            'attrs': final_attrs,
            'api_url': JS_API_URL
        }
        if self.extra_url:
            context['api_url'] += '?' + urlencode(self.extra_url)

        template = loader.get_template(self.template_name).render(context)
        return mark_safe(template)

    def value_from_datadict(self, data, files, name):
        return data.get(self.cf_turnstile_response, None)

    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs)
        if extra_attrs:
            attrs.update(extra_attrs)
        attrs['data-sitekey'] = SITEKEY
        return attrs
