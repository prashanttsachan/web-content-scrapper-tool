from django.urls import path
from .views import WebsiteDownload
# from .views import HomeView, EntryView, CreateEntryView
urlpatterns = [
    path('download/', WebsiteDownload.as_view(success_url='/website/download/'), name='website-download'),
    path('download-website/', WebsiteDownload.as_view(), name='website-download-success'),
]
