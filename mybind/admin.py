#coding: utf-8
from django.contrib import admin
from mybind.models import *
from mybind.models import Records
from django.forms import TextInput, ModelForm, Textarea, Select
from suit.admin import SortableTabularInline, SortableModelAdmin, SortableStackedInline
from suit.widgets import SuitDateWidget, SuitSplitDateTimeWidget, EnclosedInput, LinkedSelect, AutosizedTextarea

# Register your models here.


#form
class RecordsInlineForm(ModelForm):
	class Meta:
		model = Records
		fields = '__all__'
		widgets = {
		'host': TextInput(attrs={'class': 'input-small'}),
		'type': Select(attrs={'class': 'input-small'}),
		'data': TextInput(attrs={'class': 'input-small', 'style': 'width:75%'}),
		'data_tel': TextInput(attrs={'class': 'input-small', 'style': 'width:75%'}),
		'data_net': TextInput(attrs={'class': 'input-small', 'style': 'width:75%'}),
		}

class ZonesForm(ModelForm):
	class Meta:
		model = Zones
		fields = '__all__'
		widgets = {
		'zone': EnclosedInput(prepend='icon-globe',attrs={'class': 'input-medium', 'style': 'width: 180px'}),
		'desc': AutosizedTextarea(attrs={'class': 'input-medium', 'rows': 2, 'style': 'width:35%'}),
		}


###inline
class RecordsInline(admin.TabularInline):
	model = Records
	form = RecordsInlineForm

	fieldsets = (
		(
			'adadda', {		
   				'fields': ('host', 'type', 'data', 'data_tel', 'data_net' ,'zone', 'ctime', 'active', )
			}),
	)
	extra = 0
	readonly_fields =('ctime', )
	###
	def get_queryset(self, request):
		qs =  super(RecordsInline, self).get_queryset(request)
		if request.user.is_superuser:
			return qs
		else:
			return qs.exclude(type = 'SOA' ).exclude(type = 'NS')



class ZonesAdmin(admin.ModelAdmin):
	list_display = ('zone', 'desc', 'count', 'ctime', 'active', )
	search_fields = ('zone',)
	form = ZonesForm

	inlines = [RecordsInline,]
   
	def get_fieldsets(self, request, obj=None):
		if request.user.is_superuser:
			fieldsets = (
				(
				'域信息', {
				'description': u'非管理员，不可修改已添加的域',
				'fields': ('group','zone', 'desc', 'active', ),
				}
				),
			)
		else:
			fieldsets = (
				(
				'域信息', {
				'description': u'非管理员，不可修改已添加的域',
				'fields': ('zone', 'desc', 'active', ),
				}
				),
			)			
		return fieldsets	


	##count
	def  count(self, obj):
		c = Records.objects.filter( zone = obj.zone).count() -2 
		return c

	count.allow_tags = True
	count.short_description = u"记录数"

	#隐藏字段
	def get_readonly_fields(self,request,change):
		 if not request.user.is_superuser :
		 	if change:
		 		fields = ['zone',]
		 		return fields
		 else:
		 	pass
   		 return self.readonly_fields

	#获取自己的数据
	def get_queryset(self, request):
		qs = super(ZonesAdmin, self).get_queryset(request)
		if request.user.is_superuser:
			return qs
		else:
			return qs.filter(group_id=Group.objects.get(user=request.user).id)


	def save_model(self, request, obj, form, change):
		if change:
			pass
		else:
			if request.user.is_superuser:
				pass
			else:
				obj.group_id =  Group.objects.get(user=request.user).id
		obj.save()


		if not change:
			Records.objects.create(
				host = '@',
				zone_id = obj.zone,
				type = 'SOA',
				ttl = 10,
				refresh = 600,
				retry = 3600,
				expire = 86400,
				minimum = 10,
				serial = 2016032300,
				resp_contact = 'root',
				primary_ns = 'dns1.handu.com'
				)

			Records.objects.create(
				host = '@',
				zone_id = obj.zone,
				type = 'NS',
				data = 'dns1.handu.com.',
				data_tel = 'dns1.handu.com.',
				data_net = 'dns1.handu.com.',
				)




class RecordsAdmin(admin.ModelAdmin):
	list_display = ('host', 'type', 'data', )
	search_fields = ('host', 'data', 'zone')
	list_filter = ('type','zone',)
	list_editable = ('host', 'type', 'data', )
	



admin.site.register(Zones,ZonesAdmin)
admin.site.register(Records, RecordsAdmin)
