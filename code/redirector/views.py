from rest_framework import authentication, generics, permissions

from .models import URLRedirect
from .serializers import URLRedirectSerializer


class CreateRedirectorView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]
    queryset = URLRedirect.objects.none()
    serializer_class = URLRedirectSerializer
