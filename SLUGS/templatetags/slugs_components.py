from django import template


register = template.Library()


@register.inclusion_tag("SLUGS/components/nav.html")
def nav(request):
    return locals()
