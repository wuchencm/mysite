# -*- coding: utf-8 -*-
from django.core.mail import send_mail
from import_export import resources
from import_export.admin import ImportExportMixin, ExportMixin, ImportMixin, ExportActionModelAdmin
import threading
from django.contrib import admin
from managEng.models import *
from django.forms import TextInput, ModelForm, Textarea, Select
from suit.admin import SortableTabularInline, SortableModelAdmin, SortableStackedInline
from suit.widgets import SuitDateWidget, SuitSplitDateTimeWidget, \
    EnclosedInput, LinkedSelect, AutosizedTextarea



# import_export
class HostsResource(resources.ModelResource):

	class Meta:
		model = Hosts
		fields = ('hostname','project__name','ip__ip', 'device__hostname',)
		export_order = ('hostname','project__name','ip__ip', 'device__hostname',)



# Register your models here.
#发送邮件
def  sendmail(Subject, desc, to):
	send_mail('虚拟机申请',  desc, '通知 <wuchencm@126.com>', ['2062853450@qq.com', to], auth_user='wuchencm@126.com', auth_password='wudalong2016,./', fail_silently=False)
	try:
		# thread.start_new_thread( sendmail, ("Thread-1", 2, ) )
		t = threading.Thread(target = sendmail,args=(1,))
		t.start()
	except BadHeaderError:
		return HttpResponse('Invaild header fount.')



class IpInline(admin.TabularInline):
	model = Ip
	fields = ('ip',)
	extra = 1
	raw_id_fields = ("hostname",)

class IpdInline(admin.TabularInline):
	model = Ip
	fields = ('ip',)
	extra = 1




class IpsubAdmin(admin.ModelAdmin):
	list_display = ('foo_link', 'endip', 'count','desc','ctime',)
	search_fields = ('startip',)
	fields = ('startip', 'endip', 'desc')
	list_display_links = ('endip',)

	def  foo_link(self, obj):
		ip = obj.startip.split('.')[0:3]
		find = '.'.join(ip)

		return u'<a href="/admin/managEng/ip/?q=%s">%s</a>' % (find, obj.startip)
	foo_link.allow_tags = True
	foo_link.short_description = "startip"


class HostsAdmin(ExportMixin, admin.ModelAdmin):
	list_display = ('hostname', 'project', 'projectype','note','device', 'get_ip', 'usergroup','ctime', 'zt','active')
	search_fields = ('hostname','project__name','ip__ip', 'device__hostname',)
	list_filter = ('usergroup','projectype','project','zt')
	radio_fields = {'projectype': admin.VERTICAL, 'operate':admin.HORIZONTAL, 'cpu':admin.HORIZONTAL, 'memory':admin.HORIZONTAL, 'diskspace':admin.HORIZONTAL, 'backup':admin.VERTICAL}
	list_editable = ('active',)
	ordering = ('-ctime',)
	list_per_page = 15
	# 分组表单
	fieldsets = (
		('基本信息', {'fields': ('hostname', 'project', 'projectype','authorization','note','operate')}),
		('硬件参数', {'fields': ('cpu','memory','diskspace','backup')}),
		('拥有者', {'fields': ('device','usergroup')}),
	)

	#inlines
	inlines = [IpInline,]

	#获取自己的数据
	def get_queryset(self, request):
		qs = super(HostsAdmin, self).get_queryset(request)
		if request.user.is_superuser:
			return qs
		else:
			return qs.filter(usergroup_id=Group.objects.get(user=request.user).id)

	#隐藏字段
	def get_readonly_fields(self,request,change):
		 if not request.user.is_superuser :
		 	if change:
		 		fields = ['projectype','cpu','memory','diskspace','backup','device','operate','usergroup']
		 		return fields
		 	else:
		 		fields = ['usergroup','device']
		 		return fields
		 else:
		 	pass
   		 return self.readonly_fields

	def save_model(self, request, obj, form, change):
		usermail =request.user.email
	#---如果修改		
		if change:
			if request.user.is_superuser:
				obj.zt = 1
				
	#---如果新建		
		else:	
			if request.user.is_superuser:
				obj.zt = 1
			else:
				obj.zt = 0
				obj.usergroup_id =  Group.objects.get(user=request.user).id
				#发送邮件
				Subject = obj.hostname
				to = obj.project.email+','+usermail
				if obj.projectype == 'prod':
					l = u"生产"
				else:
					l = u"测试"
				desc = obj.hostname + " " + " " + l + " " + " " + obj.note
				sendmail(Subject, desc, to)


		obj.save()	


class DevicesAdmin(admin.ModelAdmin):
	list_display = ('hostname', 'project', 'projectype','note', 'get_ip', 'usergroup', 'ctime', 'zt','active')
	search_fields = ('hostname','project__name','ip__ip',)
	list_filter = ('usergroup','projectype','project','zt')
	radio_fields = {'projectype': admin.VERTICAL, 'operate':admin.HORIZONTAL, 'cpu':admin.HORIZONTAL, 'memory':admin.HORIZONTAL, 'diskspace':admin.HORIZONTAL, 'backup':admin.VERTICAL}
	list_editable = ('active',)
	ordering = ('-ctime',)
	list_per_page = 15
	inlines = [IpdInline,]
	
	# 分组表单
	fieldsets = (
		('基本信息', {'fields': ('hostname', 'project', 'projectype','authorization','note', 'operate',)}),
		('硬件参数', {'fields': ('cpu','memory','diskspace','backup')}),
		('拥有者', {'fields': ('usergroup',)}),
	)

	#获取自己的数据
	def get_queryset(self, request):
		qs = super(DevicesAdmin, self).get_queryset(request)
		# group_id = Group.objects.get(user=request.user).id
		
		if request.user.is_superuser:
			return qs
		else:
			return qs.filter(usergroup_id=Group.objects.get(user=request.user).id)
	#隐藏字段	
	def get_readonly_fields(self,request,change):
		 if not request.user.is_superuser :
		 	if change:
		 		fields = ['usergroup', 'cpu','memory','diskspace','backup','operate']
		 		return fields
		 	else:
		 		fields = ['usergroup']
		 		return fields
		 else:
		 	pass
   		 return self.readonly_fields

	#重写slave_model方法
	def save_model(self, request, obj, form, change):
		usermail =request.user.email
	#---如果修改	
		if change:
			if request.user.is_superuser:
				obj.zt = 1

	#---如果新建		
		else:	
			if request.user.is_superuser:
				obj.zt = 1
			else:
				obj.zt = 0
				obj.usergroup_id =  Group.objects.get(user=request.user).id
				#发送邮件
				Subject = obj.hostname
				to = obj.project.email+','+usermail
				if obj.projectype == 'prod':
					l = u"生产"
				else:
					l = u"测试"
				desc = obj.hostname + " " + " " + l + " " + " " + obj.note
				sendmail(Subject, desc, to)

		obj.save()


class IpAdmin(admin.ModelAdmin):
	list_display = ('ip','hd',)
	search_fields = ('ip','hostname__hostname','device__hostname')
	

	def save_model(self, request, obj, form, change):
		obj.active = True
		obj.save()

	def get_fieldsets(self, request, obj):
		if not obj.hostname and obj.device:
			fieldsets = (
			('', {'fields': (('ip', 'device',), )}),
			)
		else:
			fieldsets = (
			('', {'fields': (('ip', 'hostname',), )}),
			)			
		return fieldsets

	def hd(self, obj):
		if not obj.hostname:
			return u'<strong>%s</strong>'  %obj.device
		elif not obj.device:
			return obj.hostname
	hd.allow_tags = True
	hd.short_description = "hostname"
				



class ProjectsAdmin(admin.ModelAdmin):
	list_display = ('name', 'dept', 'officer', 'num', 'email', 'desc')
	fieldsets = (
		('', {'fields': ('name', 'dept',)}),
		('', {'fields': ('officer','num','email')}),
		('', {'fields': ('desc',)}),
	)

###办公区入网信息
class AllownetForm(ModelForm):
	class Meta:
		model = Allownet
		fields = '__all__'
		widgets = {
		'name': EnclosedInput(prepend='icon-user',attrs={'class': 'input-medium'}),
		'dept': LinkedSelect,
		'num': EnclosedInput(prepend='icon-list-alt',attrs={'class': 'input-medium'}),	
		'qq': EnclosedInput(prepend='icon-comment',attrs={'class': 'input-medium'}),
		}

class AllownetAdmin(admin.ModelAdmin):
	form = AllownetForm
	list_display = ('name', 'num', 'dept', 'qq', 'mac', 'ip','ctime')
	search_fields = ('name','num','ip')
	list_filter = ('dept', )
	fieldsets = (
		('基本信息', {'fields': ('name', 'num', 'dept', 'qq',)}),
		('网络参数', {'fields': ('mac','ip',)}),
	)

#无线上网设备
class WirelessForm(ModelForm):
	class Meta:
		model = Wireless
		fields = '__all__'
		widgets = {
		'fortime': SuitDateWidget,
		'desc': AutosizedTextarea(attrs={'class': 'input-medium', 'rows': 2, 'style': 'width:35%'}),
		'name': EnclosedInput(prepend='icon-user',attrs={'class': 'input-medium'}),
		'dept': LinkedSelect,	
		}

class WirelessAdmin(admin.ModelAdmin):
	form = WirelessForm
	list_display = ('name', 'dept', 'Terminal', 'mac', 'Checked', 'fortime','desc',)
	search_fields = ('name','dept',)
	list_filter = ('dept', )
	radio_fields = {'Terminal': admin.VERTICAL,}
	fieldsets = (
		('基本信息', {'fields': ('name', 'dept',)}),
		('硬件参数', {'fields': ('Terminal','mac','fortime',)}),
		('', {'fields': ('desc',)}),
	)

class DeptAdmin(admin.ModelAdmin):
	list_display = ('name', 'desc')

class PrintAdmin(admin.ModelAdmin):
	list_display = ('offzone', 'dept', 'floor', 'version', 'ip',)
	search_fields = ('name','dept',)
	list_filter = ('offzone', 'floor', 'dept' )
	radio_fields = {'offzone': admin.HORIZONTAL,}

	fieldsets = (
		('基本信息', {'fields': ('offzone', 'dept', 'floor',)}),
		('网络参数', {'fields': ('version','ip',)}),
	)




admin.site.register(Hosts,HostsAdmin)
admin.site.register(Devices,DevicesAdmin)
admin.site.register(Ipsub,IpsubAdmin)
admin.site.register(Ip,IpAdmin)
admin.site.register(Projects,ProjectsAdmin)
admin.site.register(Allownet,AllownetAdmin)
admin.site.register(Wireless,WirelessAdmin)
admin.site.register(Dept,DeptAdmin)
admin.site.register(Print, PrintAdmin)

