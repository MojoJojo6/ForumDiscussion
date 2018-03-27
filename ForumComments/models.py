from django.db import models

# Create your models here.

class Comments(models.Model):
    id = models.BigAutoField(primary_key=True)
    comment = models.CharField(max_length= 255)
    replies = models.ForeignKey('self',on_delete=models.CASCADE)

    