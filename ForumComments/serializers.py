"""This module implements all the serializers.
"""

from rest_framework import serializers
from ForumComments.models import Forum

class ForumListSerializer(serializers.ModelSerializer):
    """Forum serializer for listing a json tree.
    
    Arguments:
        ModelSerializer {class} -- Base class for serializer.
    """
    
    id              = serializers.IntegerField(read_only=True)
    user_id         = serializers.IntegerField(read_only=True)
    user_first_name = serializers.CharField(max_length=20, read_only=True)
    user_last_name  = serializers.CharField(max_length=20, read_only=True)
    course_id       = serializers.IntegerField(read_only=True)
    comment         = serializers.CharField(max_length=200, read_only=True)
    time_stamp      = serializers.DateTimeField(read_only=True)
    last_modified   = serializers.DateTimeField(read_only=True)

    class Meta:
        """Meta information of ForumListSerializer.
        """
        model   = Forum
        fields  = [
            'id',
            'user_id',
            'user_first_name',
            'user_last_name',
            'course_id',
            'comment',
            'time_stamp',
            'last_modified',
            'children'
        ]
    
    def get_fields(self):
        """Returns fields of serializer.
        """
        fields = super().get_fields()
        fields['children'] = ForumListSerializer(read_only=True, many=True)
        return fields


class ForumSerializer(serializers.ModelSerializer):
    """Forum serializer for create, retrieve, Update a serializer forum instance.
    
    Arguments:
        ModelSerializer {class} -- Base class for serializer.
    """
    id              = serializers.IntegerField(required=False)
    user_id         = serializers.IntegerField()
    user_first_name = serializers.CharField(max_length=20)
    user_last_name  = serializers.CharField(max_length=20)
    course_id       = serializers.IntegerField()
    comment         = serializers.CharField(max_length=200, required=False)
    parent_id       = serializers.PrimaryKeyRelatedField(queryset=Forum.objects.all())
    time_stamp      = serializers.DateTimeField(read_only=True)
    last_modified   = serializers.DateTimeField(read_only=True)

    class Meta:
        """Meta information of ForumSerializer.
        """
        model   = Forum
        fields  = [
            'id',
            'user_id',
            'user_first_name',
            'user_last_name',
            'course_id',
            'comment',
            'parent_id',
            'time_stamp',
            'last_modified',
        ]
