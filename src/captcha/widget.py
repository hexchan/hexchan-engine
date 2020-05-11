from django import forms
from django.forms import Widget, MultiWidget, MultiValueField, HiddenInput


class CaptchaWidget(MultiWidget):
    template_name = 'captcha/captcha_widget.html'

    def __init__(self, attrs=None):
        widgets = (
            forms.TextInput(attrs={
                'maxlength': 128,
                'data-key': 'solution',
                'class': 'captcha-widget__input',
                'placeholder': 'CAPTCHA',
            }),
            forms.HiddenInput(attrs={
                'maxlength': 8,
                'data-key': 'public_id',
                'class': 'captcha-widget__hidden js-captcha-id'
            }),
        )

        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value['solution'], value['public_id']]
        else:
            return [None, None]


class CaptchaField(MultiValueField):
    widget = CaptchaWidget

    def __init__(self, **kwargs):
        fields = (
            forms.CharField(),  # Captcha solution
            forms.CharField(),  # Captcha public_id
        )

        super().__init__(fields, **kwargs)

    def compress(self, data_list):
        return {
            'solution': data_list[0],
            'public_id': data_list[1],
        }
