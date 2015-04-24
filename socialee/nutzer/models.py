from django.db import models

# Create your models here.
class User(models.Model):
	user = models.CharField(max_length=120, default='nickname')
	firstname = models.CharField(max_length=120, null=True, blank=True)
	lastname = models.CharField(max_length=120, null=True,blank=True)
	email = models.EmailField()
	#newsletter = models.BooleanField(default=False)
	permission = models.BooleanField(default=False)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __unicode__(self):
		return self.email


class Digiinput(models.Model):
	user = models.OneToOneField('User', null=True, related_name="input", unique=True)
	bietet = models.TextField(null=True, blank=True)
	image = models.ImageField(upload_to='zettels/images/input/', null=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

 	def __unicode__(self):
 		return ' Xs Zettel Nr. y input'

class Digioutput(models.Model):
	user = models.OneToOneField('User', null=True, related_name="output", unique=True)
	braucht = models.TextField(null=True, blank=True)
	image = models.ImageField(upload_to='zettels/images/output/', null=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

 	def __unicode__(self):
 		return ' Xs Zettel Nr. y output'

class Tag(models.Model):
	tag = models.TextField(null=True, blank=True)
	