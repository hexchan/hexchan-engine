from django import template
from django.utils.safestring import mark_safe


register = template.Library()

TEMPLATE = '''
<svg class="svg-icon" viewBox="0 0 {size} {size}" width="{size}" height="{size}">
    <use href="#icon-{name}"/></svg>
'''.strip()


@register.simple_tag
def icon(name, size=24):
    rendered_text = TEMPLATE.format(name=name, size=size)
    return mark_safe(rendered_text)
