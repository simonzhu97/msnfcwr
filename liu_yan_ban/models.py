#coding=utf-8 
from django.db import models
import datetime
# Create your models here.
class AUser(models.Model):
	name = models.CharField(default="匿名",max_length=10)
	def __unicode__(self):
		return self.name

class Comment(models.Model):
	content = models.CharField(max_length = 1000)
	pub_date = models.DateTimeField(default = datetime.datetime.now)
	likes = models.IntegerField(default=0)
	is_sensored = models.BooleanField(default = False)
	is_top = models.BooleanField(default = False)
	is_handled = models.BooleanField(default = False)
	user = models.ForeignKey(AUser)
	is_viewed = models.BooleanField(default=False)

	def __unicode__(self):
		return "["+self.user.name+"]"+self.content

	def like(self):
		self.likes += 1
		self.save()

	def short(self):
		content = self.content
		if len(content)>10:
			return content[:10]+"..."
		else:
			return content[:10]


class Transaction(models.Model):
	name = models.CharField(max_length=100)
	quantity = models.IntegerField()
	money = models.IntegerField()
	location = models.CharField(max_length=200)
	shown_name = models.CharField(max_length=100)
	liuyan = models.CharField(max_length=1000)
	is_self = models.BooleanField(default=False)
	user = models.ForeignKey(AUser)
	is_confirmed = models.BooleanField(default=False)
	recipient = models.CharField(max_length=100, default="")
	is_processed = models.BooleanField(default=False)
	is_delivered = models.BooleanField(default=False)

	def __unicode__(self):
		return str(self.id) + ": " + self.name+" bought " + str(self.quantity) + " roses for $"+str(self.money)

class DM(models.Model):
	user = models.ForeignKey(AUser)
	content = models.CharField(max_length=200)
	is_viewed = models.BooleanField(default=False)

	# def __unicode__(self):
	# 	return "To " + str(self.user)
