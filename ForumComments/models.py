"""This module consist of all the database tables.
"""

from django.db import models

# Create your models here.

class Forum(models.Model):
    """Forum Model for each course.
    
    Arguments:
        Model {class} -- Base Model class. 
    """

    user_id         = models.BigIntegerField()
    user_first_name = models.CharField(max_length=20)
    user_last_name  = models.CharField(max_length=20)
    course_id       = models.BigIntegerField()
    comment         = models.CharField(max_length=200)
    parent_id       = models.ForeignKey('self', on_delete=models.CASCADE)
    time_stamp      = models.DateTimeField(auto_now_add=True)
    last_modified   = models.DateTimeField(auto_now=True)

    class Meta:
        """Defines meta information of Forum Model.
        """
        ordering = ['time_stamp']