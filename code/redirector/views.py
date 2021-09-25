from rest_framework import authentication, generics, permissions

from .models import URLRedirect
from .serializers import URLRedirectSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.http import HttpResponse, HttpResponseRedirect 
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from pymemcache.client import base
from django.core.cache import cache

class CreateRedirectorView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]
    queryset = URLRedirect.objects.none()
    serializer_class = URLRedirectSerializer
    
    def perform_create(self,serializer):
        serializer.save(created_by=self.request.user)

    def create(self, request, *args, **kwargs):
        base_url=settings.BASE_URL
        url=request.data['url']
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=False)
        url_redirect=URLRedirect.objects.filter(url=url)
        if url_redirect.exists():
            short_url=url_redirect.last().short_url
            return Response({'url':url,'short_url':"{}/{}".format(base_url,short_url),'created':'false'}, status=status.HTTP_202_ACCEPTED)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        result= serializer.data
        result['created']='true'
        cache.set(result['short_url'],url,48*60*60)
        result['short_url']="{}/{}".format(base_url,result['short_url'])
        return Response(result, status=status.HTTP_201_CREATED, headers=headers)


class OriginalUrlView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request,unique_key):
        if unique_key:
            if cache.get(unique_key):
                redirect_url = cache.get(unique_key)
            else:
                url_redirect_obj=get_object_or_404(URLRedirect,short_url=unique_key)
                redirect_url = url_redirect_obj.url
                cache.set(unique_key,redirect_url)
            URLRedirect.hit(unique_key)
            return HttpResponseRedirect(redirect_to=redirect_url)
        return Response({'message':'please enter short url'},status=status.HTTP_400_BAD_REQUEST)


        