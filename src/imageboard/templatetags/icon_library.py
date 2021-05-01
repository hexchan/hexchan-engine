import os.path

from django import template
from django.utils.safestring import mark_safe


register = template.Library()

# Read icon data on module import
icon_data = []
icons_dir = os.path.join(
    os.path.dirname(__file__),
    '../static/imageboard/images/icons'
)
for root, dirs, files in os.walk(icons_dir):
    for name in files:
        file_path = os.path.join(root, name)
        print(file_path)
        base_name, ext = os.path.splitext(name)
        with open(file_path, 'r') as f:
            icon_content = f.read()
            icon_content_with_id = icon_content\
                .replace(
                    '<svg',
                    '<svg id="icon-{}"'.format(base_name)
                )\
                .replace('width="512"', '')\
                .replace('height="512"', '')\
                .replace('#000', 'currentColor')
            icon_data.append(icon_content_with_id)


@register.simple_tag
def icon_library():
    rendered_text = '\n'.join(icon_data)
    return mark_safe(rendered_text)
