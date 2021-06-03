from django import template

register = template.Library()


@register.simple_tag
def custom_tag(bl_page):
    return bl_page.page.paginator.page_range[0:bl_page.number]

