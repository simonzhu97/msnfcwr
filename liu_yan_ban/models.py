#coding=utf-8 
from django.db import models
import datetime
# Create your models here.
class Comment(models.Model):
	content = models.CharField(max_length = 1000)
	author = models.CharField(max_length = 100, default = 'Anonymous')
	pub_date = models.DateTimeField(default = datetime.datetime.now)
	is_sensored = models.BooleanField(default = False)
	is_top = models.BooleanField(default = False)
	is_handled = models.BooleanField(default = False)
	user_id = models.IntegerField(default= -1)
	is_viewed = models.BooleanField(default=False)

	def __unicode__(self):
		return "["+self.author+"]"+self.content

	def short(self):
		content = self.content
		if len(content)>10:
			return content[:10]+"..."
		else:
			return content[:10]

class UserID(models.Model):
	name = models.CharField(default="z",max_length=10)
	def __unicode__(self):
		return "User"+str(self.id)

class Transaction(models.Model):
	name = models.CharField(max_length=100)
	quantity = models.IntegerField()
	money = models.IntegerField()
	location = models.CharField(max_length=200)
	shown_name = models.CharField(max_length=100)
	liuyan = models.CharField(max_length=1000)
	is_self = models.BooleanField(default=False)
	user_id = models.IntegerField()
	is_confirmed = models.BooleanField(default=False)
	recipient = models.CharField(max_length=100, default="")
	is_processed = models.BooleanField(default=False)
	is_delivered = models.BooleanField(default=False)

	def __unicode__(self):
		return str(self.id) + ": " + self.name+" bought " + str(self.quantity) + " roses for $"+str(self.money)