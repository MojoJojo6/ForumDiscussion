"""This module consist of all the serializers.
"""

from rest_framework import serializers
from ForumComments.models import Forum


class ForumListSerializer(serializers.ModelSerializer):
    """Serializer for GET (List) API View
    
    Arguments:
        ModelSerializer {class} -- Base serializer class.
    """
    user_id             = serializers.IntegerField()
    user_first_name     = serializers.CharField(max_length=20)
    user_last_name      = serializers.CharField(max_length=20)
    course_id           = serializers.IntegerField()
    comment             = serializers.CharField(max_length=200)
    time_stamp          = serializers.DateTimeField(read_only=True)
    last_modified       = serializers.DateTimeField(read_only=True)

    class Meta:
        """Meta information of ForumListSerializer.
        """
        model = Forum
        fields = [
            'user_id',
            'user_first_name',
            'user_last_name',
            'course_id',
            'comment',
            'time_stamp',
            'last_modified',
            'parent_id'
        ]
    
    def get_fields(self):
        """Returns fields attribute
        """
        fields = super().get_fields()
        fields['parent_id'] = ForumListSerializer(many=True, read_only=True)
        return fields



