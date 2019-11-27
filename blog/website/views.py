from django.shortcuts import render
import cgi

# from .forms import RegistrationForm
from django.contrib.auth.mixins import LoginRequiredMixin
# from .models import Website
# Create your views here.

class WebsiteDownload(LoginRequiredMixin, CreateView):
	template_name= "website/download.html"

class DownloadingStart(LoginRequiredMixin):
	form = cgi.FieldStorage()
	web_url =  form.getvalue('website_url')