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

class CreateRedirectorView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]
    queryset = URLRedirect.objects.none()
    serializer_class = URLRedirectSerializer
    
    def perform_create(self,serializer):
        serializer.save(created_by=self.request.user)

    def create(self, request, *args, **kwargs):
        base_url=settings.BASE_URL
        url=request.data.get('url')
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=False):
            return Response(serializer.errors.values(),status=status.HTTP_401_UNAUTHORIZED)
        url_redirect=URLRedirect.objects.filter(url=url)
        if url_redirect.exists() and not request.data.get('short_url'):
            short_url=url_redirect.last().short_url
            return Response({'url':url,'short_url':"{}{}".format(base_url,short_url),'created':'false'}, status=status.HTTP_202_ACCEPTED)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        result= serializer.data
        result['created']='true'
        URLRedirect.add_in_cache(result['short_url'],url)
        result['short_url']="{}/{}".format(base_url,result['short_url'])
        return Response(result, status=status.HTTP_201_CREATED, headers=headers)


class OriginalUrlView(APIView):
    permission_classes = [permissions.AllowAny]

    def get_client_ip(self,request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def get(self, request,unique_key):
        if unique_key:
            if URLRedirect.get_from_cache(unique_key):
                redirect_url = URLRedirect.get_from_cache(unique_key)
            else:
                url_redirect_obj=get_object_or_404(URLRedirect,short_url=unique_key)
                redirect_url = url_redirect_obj.url
                URLRedirect.add_in_cache(unique_key,redirect_url)
            info = { 'user_ip_address':self.get_client_ip(request),'user_agent':request.META.get('HTTP_USER_AGENT'),'http_referer':request.META.get('HTTP_REFERER')}
            URLRedirect.hit(unique_key,info)
            return HttpResponseRedirect(redirect_to=redirect_url)
        return Response({'message':'please enter short url'},status=status.HTTP_400_BAD_REQUEST)


        