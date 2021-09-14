from django.db import models
from django.utils.crypto import get_random_string

# Create your models here.
class URLRedirect(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    url=models.CharField(max_length=255)
    short_url=models.CharField(max_length=255,db_index=True)
    hit_count=models.IntegerField(default=0)


    def hit(self):
        self.hit_count +=1
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