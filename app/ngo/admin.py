from django.contrib import admin
from .models import NgoDetail, Needs, Images, City, CharityHomeType
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html
from .forms import RequiredInlineFormSet
from django.db.models import Q

class NeedsInlineAdmin(admin.TabularInline):
    model = Needs
    extra = 0


class NgoDetailInlineAdmin(admin.StackedInline):
    model = NgoDetail
    formset = RequiredInlineFormSet
    can_delete = False

    fields = ('name',)
        
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["name"]
        else:
            return []


class TaxCertificateListFilter(admin.SimpleListFilter):

    title = _('Has tax certificate')

    parameter_name = 'Tax Certificate'

    def lookups(self, request, model_admin):

        return (
            ('yes', _('Yes')),
            ('no',  _('No')),
        )

    def queryset(self, request, queryset):

        if self.value() == 'yes':
            return queryset.filter(taxCertificate__isnull=False).exclude(taxCertificate='')

        if self.value() == 'no':
            return queryset.filter(Q(taxCertificate__isnull=True) | Q(taxCertificate__exact=''))


class NgoDetailAdmin(admin.ModelAdmin):

    def has_add_permission(self, request, obj=None):
        return False
    
    model = NgoDetail
    inlines = [NeedsInlineAdmin]

    fieldsets = (
        (None, {'fields': ('user', 'name','contactNumber')}),
        (_('Location'), {'fields': ('address','city','mapLocation')}),
        (_('Others'), {'fields': ('description', 'charityHomeType', 'amountRaised','taxCertificate')}),
    )

    readonly_fields = ('name','user')
    list_display = ('name', 'city', 'needs_unverified_count')
    list_filter = ( 'city', 'charityHomeType', TaxCertificateListFilter)
    search_fields = ('name', 'city','needs_unverified_count')
    ordering = ('name','city')

    def needs_unverified_count(self, obj):
        return obj.needs.filter(status='unverified').count()

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class NgoImage(NgoDetail):
    class Meta:
        proxy = True


class ImagesInlineAdmin(admin.TabularInline):
    model = Images
    extra = 0
    
    fields = ('image_tag','image')
    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
       return format_html('<img src="{}"  width="150" height="150" />'.format(obj.image.url))


    image_tag.short_description = 'Image'

class NgoImageAdmin(admin.ModelAdmin):

    def has_add_permission(self, request, obj=None):
        return False

    model = NgoImage
    inlines = [ImagesInlineAdmin]

    fields = ('name','user')
    readonly_fields = ('name','user')
    list_display = ('name', 'city') 
    list_filter = ( 'city', 'charityHomeType')
    search_fields = ('name', 'city')
    ordering = ('name',)
    
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class CityAdmin(admin.ModelAdmin):
    model = City
    list_display = ('city',) 

class CharityHomeTypeAdmin(admin.ModelAdmin):
    model = CharityHomeType
    list_display = ('charityHomeType',) 

admin.site.register(NgoDetail, NgoDetailAdmin)
admin.site.register(NgoImage, NgoImageAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(CharityHomeType, CharityHomeTypeAdmin)