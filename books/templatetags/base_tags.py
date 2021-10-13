from django import template

# register library
register = template.Library()

# register a html file
@register.inclusion_tag('books/partials/link.html')
# send link function
def link(request, link_name, content, classes):
    # return a dictionary
    return {
        # request eq to request
        'request': request,
        # link name eq to link_name
        'link_name': link_name,
        # link eq to link_name
        'link': '{}'.format(link_name),
        # content eq to content
        'content': content,
        # classes eq to classess
        'classes': classes
    }