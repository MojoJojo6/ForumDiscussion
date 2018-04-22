"""This module consist of all the database tables.
"""

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,BaseUserManager,
)


class UserManager(BaseUserManager):

    def create_user(self, **validated_data):

        if not validated_data["email_id"]:
            raise ValueError("Email Id is required")
        if not validated_data["password"]:
            raise ValueError("Password is required")
        if not validated_data["first_name"]:
            raise ValueError("First Name is required")
        if not validated_data["last_name"]:
            raise ValueError("Last Name is required")
        if validated_data["role"] is None:
            raise ValueError("Role is required")

        user_obj = self.model( email_id=self.normalize_email(validated_data["email_id"]))
        user_obj.first_name = validated_data["first_name"]
        user_obj.last_name = validated_data["last_name"]
        user_obj.role = validated_data["role"]
        user_obj.mobile_number = validated_data["mobile_number"]
        user_obj.staff = validated_data["staff"]
        user_obj.admin = validated_data["admin"]
        user_obj.active = validated_data["active"]
        user_obj.set_password(validated_data["password"])
        user_obj.save(using=self.db)
        return user_obj
    
    def create_superuser(self, **validated_data):
        validated_data['staff'] = True
        validated_data['admin'] = True
        validated_data['active'] = True
        return self.create_user(**validated_data)

    def create_staffuser(self, **validated_data):
        validated_data['staff'] = True
        validated_data['admin'] = False
        validated_data['active'] = True
        return self.create_user(**validated_data)

    
class User(AbstractBaseUser):
    """ User Table for User Service"""
    roles = [(0, "Admin"), (1, "Faculty"), (2, "Student")]

    u_id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email_id = models.EmailField(max_length=255, unique=True)
    mobile_number = models.CharField(max_length=20)
    role = models.IntegerField(choices=roles)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email_id'
    REQUIRED_FIELDS = ['first_name','last_name','role', 'mobile_number']

    objects = UserManager()

    def get_full_name(self):
        return "{0} {1}".format(self.first_name,self.last_name)

    def get_short_name(self):
        return self.first_name

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    """String Function for All CharField in User Model"""
    def __str__(self):
        return self.email_id


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
    parent_id       = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    time_stamp      = models.DateTimeField(auto_now_add=True)
    last_modified   = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    
    class Meta:
        """Defines meta information of Forum model.
        """
        ordering = ['time_stamp']

    def __str__(self):
        """string overide method
        
        Returns:
            string -- Returns a comment text.
        """
        return self.comment