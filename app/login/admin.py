from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, UserProfile, Ngo, Staff
from ngo.admin import NgoDetailInlineAdmin
from django.db.models import Q
from django.contrib.auth.models import Group
from .forms import RequiredInlineFormSet



class UserProfileInlineAdmin(admin.StackedInline):
    model = UserProfile
    formset = RequiredInlineFormSet
    can_delete = False
    

    

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Permissions'), {'fields': ('is_active',)}),
        (_('Important Info'), {'fields': ('last_login', 'date_joined', 'modified_by')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'last_login', 'is_active')
    list_filter = ( 'last_login', 'is_active')
    search_fields = ('email', 'is_active', 'date_joined')
    ordering = ('email','last_login','date_joined')
    readonly_fields = ('last_login', 'date_joined', 'modified_by')

    def save_model(self, request, obj, form, change): 
        obj.modified_by = request.user.email
        obj.save()

    def get_queryset(self, request):
        return self.model.objects.filter(Q(is_ngo=False) & Q(is_staff=False) & Q(is_superuser=False))

    inlines = [UserProfileInlineAdmin]




class NgoAdmin(CustomUserAdmin):

    inlines = [NgoDetailInlineAdmin]
    
    def save_model(self, request, obj, form, change):
        obj.modified_by = request.user.email
        obj.is_ngo = True
        obj.save()

    def get_queryset(self, request):
        return self.model.objects.filter(Q(is_ngo=True) & Q(is_staff=False) & Q(is_superuser=False))



class StaffAdmin(CustomUserAdmin):

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Permissions'), {'fields': ('is_active','is_superuser')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined', 'modified_by')}),
    )


    inlines = [UserProfileInlineAdmin]
    
    def save_model(self, request, obj, form, change): 
        obj.modified_by = request.user.email
        obj.is_staff = True
        obj.save()

    def get_queryset(self, request):
        return self.model.objects.filter(Q(is_staff=True) | Q(is_superuser=True))

admin.site.unregister(Group)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Ngo, NgoAdmin)
admin.site.register(Staff, StaffAdmin)

admin.site.site_header = 'Sharity administration'