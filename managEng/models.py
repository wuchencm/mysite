# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.html import format_html
from django.db import models
from django.contrib.auth.models import User, Group

# Create your models here.

class Dept(models.Model):
	name = models.CharField(max_length=256,verbose_name='部门')
	desc = models.CharField(max_length=256,verbose_name='描述')

	def __unicode__(self):
		return self.name

class Allownet(models.Model):
	name = models.CharField(max_length=256,verbose_name='姓名')
	dept = models.ForeignKey(Dept, verbose_name='部门')
	num = models.CharField(max_length=256,verbose_name='工号')
	qq = models.IntegerField(blank=True,null=True,verbose_name='QQ')
	mac = models.CharField(max_length=25,verbose_name='MAC')
	ip = models.GenericIPAddressField(unique=True, verbose_name='IP Address')
	ctime = models.DateField(auto_now=True,verbose_name='创建时间')

	def  __unicode__(self):
		return self.name
	class Meta:
		verbose_name = '办公区入网信息'
		verbose_name_plural = '办公区入网信息'


class Wireless(models.Model):

	Terminal_choices = (
		(u'手机', u'手机'),
		(u'笔记本', u'笔记本'),
		(u'其他', u'其他'),
		)

	name = models.CharField(max_length=256,verbose_name='姓名')
	dept = models.ForeignKey(Dept, verbose_name='部门')
	Terminal = models.CharField(max_length=25, choices=Terminal_choices, verbose_name='终端类型')
	mac = models.CharField(unique=True,max_length=25,verbose_name='MAC')
	Checked = models.BooleanField(default=True,verbose_name='部门领导审核')
	fortime = models.DateField(blank=True, null=True, verbose_name='使用时限', help_text='默认为空时，表示不限期限')
	ctime = models.DateField(auto_now=True,verbose_name='开通时间')
	desc = models.CharField(max_length=256,verbose_name='申请原因')

	def  __unicode__(self):
		return self.name

	class Meta:
		verbose_name = '无线设备'
		verbose_name_plural = '无线设备'

class Print(models.Model):

	type_choices = (
		(u'彩色打印', u'彩色打印'),
		(u'本地打印', u'本地打印'),
		(u'网络打印', u'网络打印'),
		)
	offzone_choices = (
		(u'奥盛大厦', u'奥盛大厦'),
		(u'大陆机电', u'大陆机电'),
		(u'齐河', u'齐河'),
		(u'板房', u'板房'),		
	)

	offzone = models.CharField(max_length=256, choices=offzone_choices, verbose_name='办公区')
	dept = models.ForeignKey(Dept, verbose_name='部门')
	floor = models.CharField(max_length=25,verbose_name='楼层')
	version = models.CharField(max_length=200, verbose_name='打印机型号')
	ip = models.GenericIPAddressField(unique=True, verbose_name='IP Address')
	printype = models.CharField(max_length=200, choices=type_choices, verbose_name='打印类型')
	ctime = models.DateField(auto_now=True,verbose_name='开通时间')

	# def  __unicode__(self):
	# 	return self.dept

	class Meta:
		verbose_name = '打印机'
		verbose_name_plural = '打印机'
	


class  Projects(models.Model):
	name  =  models.CharField(max_length=256,verbose_name='项目名称')
	dept = models.ForeignKey(Group, blank=True, null=True, verbose_name='部门')
	officer = models.CharField(max_length=256, blank=True, verbose_name='负责人')
	num = models.CharField(max_length=256,verbose_name='项目名称')
	email = models.EmailField(verbose_name='邮箱地址', help_text='这是一个必填项，以便当添加新主机时通知到负责人')
	desc = models.TextField(blank=True,verbose_name='项目描述')

	def  __unicode__(self):
		return self.name
	class Meta:
		verbose_name = '项目'
		verbose_name_plural = '项目'


class Ipsub(models.Model):
	startip = models.GenericIPAddressField(unique=True)
	endip = models.GenericIPAddressField(unique=True)
	count = models.IntegerField(blank=True,null=True)
	desc = models.CharField(max_length=40,blank=True)
	ctime = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.startip
	class Meta:
		verbose_name = 'IP 段'
		verbose_name_plural = 'IP 段'




class  Devices(models.Model):
	#项目类型 
	projectype_choices  = (
		(u'test', u'测试'),
		(u'prod', u'生产'),
	)
	#操作系统
	operate_choices = (
		('linux 6.5', 'linux 6.5'),
		('linux 7.0', 'linux 7.0'),
		('windows 2008', 'windows 2008'),
		('kvm', 'kvm'),
		('esxi', 'esxi'),		
	)
	#cpu数
	cpu_choices = (
		('2', '2'),
		('4', '4'),
		('8', '8'),
		('12', '12'),
		('16', '16'),
		('24', '24'),
		('64z`', '64'),		
	)
	# 内存大小
	memory_choises = (
		('8', '8'),
		('16', '16'),
		('32', '32'),
		('64', '64'),
		('128', '128'),
		('more', 'more'),
	)
	# disk
	disk_choises = (
		('500', '500'),
		('600', '600'),
		('1000', '1000'),
		('2000', '2000'),
		('4000', '4000'),
	)

	backup_choises = (
		('整机备份', '整机备份'),
		('配置文件', '配置文件'),
		('应用数据', '应用数据'),
		('无需备份', '无需备份'),
	)


	hostname = models.CharField(max_length=64, unique=True, verbose_name='主机名')
	usergroup = models.ForeignKey(Group, blank=True, null=True, verbose_name='所有者')
	project = models.ForeignKey(Projects, blank=True, null=True, verbose_name='项目名称')
	projectype = models.CharField(max_length=256, choices=projectype_choices, verbose_name='项目类型')
	operate = models.CharField(max_length=256, choices=operate_choices, default='linux 6.5', verbose_name='操作系统')
	cpu = models.CharField(choices=cpu_choices,max_length=256, default=8)
	memory = models.CharField(choices=memory_choises, default=8, max_length=256, verbose_name='内存(G)')
	diskspace = models.CharField(choices=disk_choises, max_length=256, default=500, verbose_name='磁盘容量(GB)')
	ctime = models.DateTimeField(auto_now=True, verbose_name='创建时间')
	uptime = models.DateTimeField(auto_now_add=True)
	active = models.BooleanField(default=True,verbose_name='Online')
	zt = models.BooleanField(default=True,verbose_name='审核')
	note = models.TextField(blank=True, verbose_name='应用及系统概述', help_text='或填写应用安装、数据、配置文件目录以及注意事项等')
	authorization = models.CharField(max_length=256,blank=True,verbose_name='访问权限')
	backup = models.CharField(choices=backup_choises, default='无需备份', max_length=256, verbose_name='备份')


	def __unicode__(self):
		return self.hostname

	def get_ip(self):
		return '<br>'.join([a.ip for a in self.ip_set.all()])
	get_ip.short_description = 'IP address'	
	get_ip.allow_tags = True
	
	# def get_group(self):
	# 	g = list(self.user.groups.all())
	# 	for e in g:
	# 		return e
	# get_group.short_description =  u'部门'
	# get_group.allow_tags = True

	class Meta:
		verbose_name = '主机'
		verbose_name_plural = '主机'
		ordering = ['ctime',]



	

class Hosts(models.Model):
	#项目类型 
	projectype_choices  = (
		(u'test', u'测试'),
		(u'prod', u'生产'),
	)
	#操作系统
	operate_choices = (
		('linux 6.5', 'linux 6.5'),
		('linux 7.0', 'linux 7.0'),
		('windows 2008', 'windows 2008'),
		('kvm', 'kvm'),
		('esxi', 'esxi'),		
	)
	#cpu数
	cpu_choices = (
		('2', '2'),
		('4', '4'),
		('8', '8'),
		('16', '16'),		
	)
	# 内存大小
	memory_choises = (
		('2', '2'),
		('4', '4'),
		('6', '6'),
		('8', '8'),
		('12', '12'),
		('more', 'more'),
	)
	# disk
	disk_choises = (
		('100', '100'),
		('150', '150'),
		('200', '200'),
		('300', '300'),
		('more', 'more'),
	)

	backup_choises = (
		('整机备份', '整机备份'),
		('配置文件', '配置文件'),
		('应用数据', '应用数据'),
		('无需备份', '无需备份'),
	)
	usergroup  =  models.ForeignKey(Group, verbose_name='所有者')
	hostname = models.CharField(max_length=64, unique=True,verbose_name='主机名')
	project = models.ForeignKey(Projects, blank=True, null=True, verbose_name='项目名称')
	projectype = models.CharField(max_length=256,choices=projectype_choices, verbose_name='项目类型')
	operate = models.CharField(max_length=256, choices=operate_choices, default='linux 6.5', verbose_name='操作系统')
	cpu = models.CharField(max_length=256, choices=cpu_choices, default=4)
	memory = models.CharField(max_length=256, choices=memory_choises, default=4, verbose_name='内存(G)')
	diskspace = models.CharField(max_length=256, choices=disk_choises, default=200, verbose_name='磁盘容量(GB)')
	backup = models.CharField(choices=backup_choises, default='无需备份', max_length=256)
	authorization = models.CharField(max_length=256,blank=True,verbose_name='访问权限')
	note = models.TextField(blank=True, verbose_name='应用及系统概述', help_text='或填写应用安装、数据、配置文件目录以及注意事项等')	
	ctime = models.DateTimeField(auto_now=True,verbose_name='创建时间')
	utime = models.DateTimeField(auto_now=True)
	zt = models.BooleanField(default=True,verbose_name='审核')
	active = models.BooleanField(default=True,verbose_name='Online')
	device = models.ForeignKey(Devices,blank=True,null=True,verbose_name='物理机')

	def __str__(self):
		return self.hostname

	def get_ip(self):
		return '<br>'.join([a.ip for a in self.ip_set.all()])
	get_ip.short_description = 'IP address'	
	get_ip.allow_tags = True


	def get_group(self):
		g = list(self.user.groups.all())
		for e in g:
			return e
	get_group.short_description = u'部门'

	class Meta:
		verbose_name = '虚拟机'
		verbose_name_plural = '虚拟机'





class  Ip(models.Model):
	ip = models.GenericIPAddressField(unique=True,verbose_name='IP address')
	hostname = models.ForeignKey(Hosts,null=True,blank=True,verbose_name='虚拟机')
	device = models.ForeignKey(Devices,null=True,blank=True,verbose_name='主机')
	

	def __str__(self):
		return self.ip	

	class Meta:
		verbose_name = 'IP 地址'
		verbose_name_plural = 'IP 地址'