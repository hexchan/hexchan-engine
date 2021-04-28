from django import forms


class CaptchaWidget(forms.TextInput):
    template_name = 'imageboard/captcha_widget.html'

    def __init__(self, attrs=None):
        self.board_id = None
        self.thread_id = None

        super().__init__(attrs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['board_id'] = self.board_id
        context['widget']['thread_id'] = self.thread_id
        return context
