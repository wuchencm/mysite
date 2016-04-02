#coding: utf-8
from __future__ import unicode_literals
from django.contrib.auth.models import User, Group
from django.db import models

# Create your models here.

class Zones(models.Model):
	group = models.ForeignKey(Group, blank=True, null=True, verbose_name='部门')
	zone = models.CharField(max_length=250, unique=True, blank=True, verbose_name='域')
	desc = models.CharField(max_length=256, blank=True, verbose_name='描述')
	ctime = models.DateTimeField(auto_now=True,verbose_name='创建时间')
	active =  models.BooleanField(default=True,verbose_name='状态')

	def __str__(self):
		return self.zone

	class Meta:
		verbose_name = '域'
		verbose_name_plural = '域'


class Records(models.Model):

	type_choices = (
		('A', 'A'),
		('CNAME', 'CNAME'),
		('PTR', 'PTR'),
		('SOA', 'SOA'),
		('NS', 'NS'),
		)

	# group = models.ForeignKey(Group)
	host = models.CharField(max_length=256,  verbose_name='记录')
	zone = models.ForeignKey(Zones, db_column='zone', to_field='zone',  verbose_name='域')
	type = models.CharField(max_length=25, choices=type_choices , blank=True, verbose_name='类型')
	data = models.CharField(max_length=100, blank=True,null=True, verbose_name='默认')
	data_tel = models.CharField(max_length=100,  blank=True,null=True, verbose_name='电信')
	data_net = models.CharField(max_length=100,  blank=True,null=True, verbose_name='联通')
	ttl = models.IntegerField(blank=True,null=True, default=10)
	max_priority = models.IntegerField(blank=True,null=True)
	refresh = models.IntegerField(blank=True,null=True)
	retry = models.IntegerField(blank=True,null=True)
	expire = models.IntegerField(blank=True,null=True)
	minimum = models.IntegerField(blank=True,null=True)
	serial = models.IntegerField(blank=True,null=True)
	resp_contact = models.CharField(max_length=256)
	primary_ns = models.CharField(max_length=256)
	ctime = models.DateField(auto_now=True,verbose_name='创建时间')
	active =  models.BooleanField(default=True,verbose_name='状态')

	def __str__(self):
		return self.host

	class Meta:
		verbose_name = '记录'
		verbose_name_plural = '记录'