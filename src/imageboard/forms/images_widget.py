from django.forms import FileInput

from hexchan import config


class ImagesWidget(FileInput):
    template_name = 'imageboard/parts/images_widget.html'

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['accepted_file_types'] = ','.join(config.FILE_MIME_TYPES)
        context['widget']['max_file_size'] = config.FILE_MAX_SIZE
        context['widget']['max_file_num'] = config.FILE_MAX_NUM
        return context
