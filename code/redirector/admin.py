from django.contrib import admin
from .models import URLRedirect, URLRedirectInfo
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


class URLRedirectInfoAdmin(admin.ModelAdmin):
    readonly_fields = ('visited_at','id')
    fields = ['visited_at','id','url_redirect','user_ip_address','http_referer','user_agent']
    date_hierarchy = 'visited_at'
    list_display = ['id','url_redirect','user_ip_address','http_referer','user_agent']
    sortable_by=['id','url_redirect','visited_at']
    ordering = ['id']
    list_filter = ['visited_at']
    search_fields=['url_redirect']
    list_display_links=['id']

admin.site.register(URLRedirect,URLRedirectAdmin)
admin.site.register(URLRedirectInfo,URLRedirectInfoAdmin)

