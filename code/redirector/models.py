from django.db import models
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
from pymemcache.client import base
from django.core.cache import cache

# Create your models here.

class URLRedirect(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    url=models.CharField(max_length=255)
    short_url=models.CharField(max_length=255,db_index=True)
    hit_count=models.IntegerField(default=0)
    created_by = models.ForeignKey(User,null=True,on_delete=models.CASCADE) 
    
    @classmethod
    def hit(cls,unique_key,info):
        obj = URLRedirect.objects.get(short_url=unique_key)
        URLRedirectInfo.objects.create(url_redirect=obj,user_agent=info['user_agent'],user_ip_address=info['user_ip_address'],http_referer=info['http_referer'])
        obj.hit_count += 1
        obj.save()
        
        
    @classmethod
    def add_in_cache(cls,key,value,time_period=48*60*60):
        cache.set(key,value,time_period)
    
    @classmethod
    def get_from_cache(cls,key):
        return cache.get(key)
    

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.short_url:
            self.short_url=self.get_unique_key()
            self.save()


    @classmethod
    def get_unique_key(cls):
        k= get_random_string(length=5)
        #TODO handle multiple duplicate checks
        if URLRedirect.objects.filter(short_url=k).exists():
            k= get_random_string(length=5)
        return k
  



    @classmethod
    def make_entry(cls,url):
        urlr=URLRedirect(url=url)
        urlr.short_url=cls.get_unique_key()
        urlr.save()


class URLRedirectInfo(models.Model):
    visited_at = models.DateTimeField(auto_now_add=True)
    url_redirect = models.ForeignKey(URLRedirect,on_delete=models.CASCADE)
    user_ip_address=models.CharField(max_length=255,blank=True,null=True)
    http_referer = models.CharField(max_length=255,blank=True,null=True)
    user_agent = models.CharField(max_length=255,blank=True,null=True)


    