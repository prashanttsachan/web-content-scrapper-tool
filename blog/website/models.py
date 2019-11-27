from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Website (models.Model):
	website_url = models.CharField(max_length=255)

	class Meta:
		verbose_name_plural = "websites"

	def __str__(self):
		return f'{self.website_url}'