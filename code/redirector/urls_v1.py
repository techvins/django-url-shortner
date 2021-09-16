from django.urls import path
from .views import CreateRedirectorView, OriginalUrlView

urlpatterns = [
    path('create/', CreateRedirectorView.as_view()),
    path('get_original_url/', OriginalUrlView.as_view()),

]
