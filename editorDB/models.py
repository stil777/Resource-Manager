#coding: utf-8

from django.db import models

class Task(models.Model):
	Title = models.CharField(max_length=30)
	class Meta():
		db_table = "Task"
	def __unicode__(self):
		return self.Title

class Machine(models.Model):
	NumOfCores = models.IntegerField(default=0)
	class Meta():
		db_table = "Machine"

class Option(models.Model):
	Title = models.CharField(max_length=20)
	Task = models.ForeignKey(Task)
	class Meta():
		db_table = "Option"

class Launch(models.Model):
	Date = models.DateField(auto_now_add=False)
	Machine = models.ForeignKey(Machine)
	Task = models.ForeignKey(Task)
	RunTime = models.IntegerField(default=0)
	DataSize = models.IntegerField(default=0)
	class Meta():
		db_table = "Launch"

class LaunchOption(models.Model):
	Value = models.IntegerField(default=0)
	Launch = models.ForeignKey(Launch)
	Option = models.ForeignKey(Option)
	class Meta():
		db_table = "LaunchOption"