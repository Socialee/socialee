from django import template
from django.contrib.auth.models import User
from socialee.models import CommonGround, Profile, Project
from ideas.models import Idea


register = template.Library()


@register.simple_tag
def user_count():
	user_count = User.objects.all().count()
	return user_count

@register.simple_tag
def project_idea_count():
	project_count = Project.objects.all().count()
	idea_count = Idea.objects.all().count()
	project_idea_count = project_count + idea_count
	return project_idea_count