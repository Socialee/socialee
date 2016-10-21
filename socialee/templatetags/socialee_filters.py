from django import template
from django.template import Context, Template
from socialee.models import CommonGround, Profile
import re

register = template.Library()

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

@register.simple_tag
def profiles(user):
	return Profile.objects.filter(slug=user)