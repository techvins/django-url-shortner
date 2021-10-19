from rest_framework import serializers
from .models import URLRedirect

class URLRedirectSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = URLRedirect
        fields = ['url', 'short_url']
        extra_kwargs = {
        'short_url': {'required': False},
        'url': {
                'error_messages':{"blank":"Please enter the URL."}
            }
         }
        

    def validate_short_url(self, value):
        if len(value) < 3:
            raise serializers.ValidationError({'message':'Minimum length of must url should be 3.'})
        if URLRedirect.objects.filter(short_url=value).exists():
            raise serializers.ValidationError({'message':'This short url is not available.'})
        return value