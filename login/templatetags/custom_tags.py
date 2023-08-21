from django import template
register=template.Library()
@register.simple_tag
def half_content(Description):
    total=len(Description)
    half=total/2
    half=int(half)
    content=Description[:half]
    return content
