from django.contrib import admin
from .models import MainPayed, Payments, SearchWords, User, Home, AppTokens


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'username', 'created_date', 'update_date', 'active']
    list_display_links = ['username']
    sortable_by = ['username']
    list_filter = [ 'active']
    list_editable = ['active']
    search_fields = ['full_name', 'username']
    fieldsets = (
        ('General Info', {
            'fields': ('full_name', 'username', 'password', 'email', 'phone_number')
        }),
        ('Details', {
            'classes': ('collapse',),
            'fields': ('active',)
        }),
        ('AdminDetail', {
            'classes': ('collapse',),
            'fields': ('superuser', 'staff',)
        })
    )
    actions = ['make_active', 'make_inactive']

    def make_active(self, request, queryset):
        active = queryset.update(active=True)

    def make_inactive(self, request, queryset):
        active = queryset.update(active=False)


@admin.register(Home)
class HomeAdmin(admin.ModelAdmin):
    list_display = ['title', 'address', 'created_date', 'update_date']
    list_display_links = ['title']


# register AppTokens
@admin.register(AppTokens)
class AppTokensAdmin(admin.ModelAdmin):
    list_display = ['title', 'token']
 

@admin.register(SearchWords)
class SearchWordsAdmin(admin.ModelAdmin):
    list_display = ['word']
  

@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    list_display = ['amount']


@admin.register(MainPayed)
class MainPayedAdmin(admin.ModelAdmin):
    list_display = ['amount']
