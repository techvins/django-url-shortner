from django.db import models
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
# Create your models here.
class URLRedirect(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    url=models.CharField(max_length=255,unique=True)
    short_url=models.CharField(max_length=255,db_index=True)
    hit_count=models.IntegerField(default=0)
    created_by = models.ForeignKey(User,null=True,on_delete=models.CASCADE) 

    def hit(self):
        self.hit_count +=1
        self.save()
    

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