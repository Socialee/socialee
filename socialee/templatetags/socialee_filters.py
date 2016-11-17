from django import template
from django.template import Context, Template
from socialee.models import CommonGround, Profile
import re

register = template.Library()


@register.simple_tag
def profiles(user):
    '''
    Ich habe diesen tag schon in socialee_tags.py kopiert. 
    Kann hier raus, wenn klar ist, ob der nicht mehr über {{ load socialee_filters }} gedaden werden muss.
    '''
    return Profile.objects.filter(slug=user)


@register.filter
def url_target_blank(text):
    return text.replace('<a ', '<a target="_blank" ')


@register.filter
def link_ats(value):
	c = Context()
	for user in re.finditer(r'@(?P<slug>[\w.@+-]+)', value):
		try:
			u = CommonGround.objects.get(slug=user.group(1))
			c[user.group(1)] = u
		except:
			pass
	t = Template(re.sub(r'@(?P<slug>[\w.@+-]+)', 
		r'{% if \1.profile %}<a href="{% url "profile_view" slug=\1.slug %}">@\1</a>' +
		r'{% elif \1.project %}<a href="{% url "project_view" slug=\1.slug %}">@\1</a>{% else %}@\1{% endif %}', value))
	return t.render(c)


@register.filter
def truncatesmart(value, limit=80):
    """
    Truncates a string after a given number of chars keeping whole words.

    Usage:
        {{ string|truncatesmart }}
        {{ string|truncatesmart:50 }}
    """

    try:
        limit = int(limit)
    # invalid literal for int()
    except ValueError:
        # Fail silently.
        return value

    # Make sure it's unicode
    value = unicode(value)

    # Return the string itself if length is smaller or equal to the limit
    if len(value) <= limit:
        return value

    # Cut the string
    value = value[:limit]

    # Break into words and remove the last
    words = value.split(' ')[:-1]

    # Join the words and return
    return ' '.join(words) + '...'


@register.filter
def truncatelist(tlist, limit=8):
    """
    Truncates a list after a given number of elements.

    Usage:
        {{ list|truncatelist }}
        {{ list|truncatelist:5 }}
    """

    try:
        limit = int(limit)
    # invalid literal for int()
    except ValueError:
        # Fail silently.
        return tlist

    # Return the string itself if length is smaller or equal to the limit
    if len(tlist) <= limit:
        return tlist

    n = str(len(tlist)-limit)
    # Cut the string
    tlist = tlist[:limit]
    tlist.append(n+" Mehr...")

    # Join the words and return
    return tlist