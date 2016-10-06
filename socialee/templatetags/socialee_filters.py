from django import template
from django.template import Context, Template
from socialee.models import User
import re

register = template.Library()

@register.filter
def link_ats(value):
	c = Context()
	for user in re.finditer(r'@(?P<slug>[\w.@+-]+)', value):
		try:
			u = User.objects.get(username=user.group(1))
			c[user.group(1)] = u
		except:
			pass
	t = Template(re.sub(r'@(?P<slug>[\w.@+-]+)', 
		r'{% if \1 %}<a href="{% url "profile_view" \1 %}">@\1</a>{% else %}@\1{% endif %}', value))
	return t.render(c)


@register.filter
def long_name(object):
	return object.long_name()

@register.filter
def short_name(object):
	return object.short_name()