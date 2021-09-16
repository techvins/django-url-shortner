from rest_framework import authentication, generics, permissions

from .models import URLRedirect
from .serializers import URLRedirectSerializer
from rest_framework.response import Response
from rest_framework import status



class CreateRedirectorView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]
    queryset = URLRedirect.objects.none()
    serializer_class = URLRedirectSerializer
    
    def perform_create(self,serializer):
        serializer.save(created_by=self.request.user)

    def create(self, request, *args, **kwargs):
        url=request.data['url']
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=False)
        url_redirect=URLRedirect.objects.filter(url=url)
        if url_redirect.exists():
            short_url=url_redirect.last().short_url
            return Response({'url':url,'short_url':short_url,'created':'false'}, status=status.HTTP_202_ACCEPTED)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        result= serializer.data
        result['created']='true'
        return Response(result, status=status.HTTP_201_CREATED, headers=headers)