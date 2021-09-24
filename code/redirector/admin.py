from django.contrib import admin
from .models import URLRedirect
# Register your models here.


class URLRedirectAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at','id','created_by')
    fields = ['created_at','id','created_by','short_url','url','hit_count']
    date_hierarchy = 'created_at'
    list_display = ['id', 'short_url','url','hit_count','created_by']
    sortable_by=['id', 'short_url','created_at']
    ordering = ['id']
    list_filter = ['created_at']
    search_fields=['url','short_url','id']
    list_display_links=['id','short_url']


admin.site.register(URLRedirect,URLRedirectAdmin)
