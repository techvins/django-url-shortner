from django.urls import path
from .views import CreateRedirectorView

urlpatterns = [
    path('create/', CreateRedirectorView.as_view()),
]
