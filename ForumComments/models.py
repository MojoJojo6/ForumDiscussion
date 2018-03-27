from django.db import models

# Create your models here.

class Comments(models.Model):

    id = models.BigAutoField(primary_key=True)
    comment = models.CharField(max_length= 255)
    parent_comment = models.ForeignKey('self',on_delete=models.CASCADE)
    timestamp = models.DateField(auto_now_add=True)
    last_updated = models.DateField(auto_now=True)