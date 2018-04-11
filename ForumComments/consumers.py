"""This modules consist all the consumers.
"""

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from ForumComments.serializers import ForumListSerializer, ForumSerializer
from rest_framework.exceptions import ValidationError
from .models import Forum
import json


class ForumConsumer(AsyncWebsocketConsumer):
    """Real time websocket for Forum discussion
    
    Arguments:
        AsyncWebsocketConsumer {class} -- Base class for asynchronous websocket
    """
    
    async def connect(self):
        """Called on connection.
        """
        self.course_room_id = self.scope['url_route']['kwargs']['course_room_id']
        self.room_group_name = 'forum_%s' % self.course_room_id
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Accept connection
        await self.accept()

        serialized_data = await self.serialize_forum()
        # Send a Forum
        await self.send(
            text_data=serialized_data
        )


    async def disconnect(self, close_code):
        """Called on disconnection.
        """
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    async def receive(self, text_data=None):
        """Runs when a new comment is received in a forum.
        """
        packet = json.loads(text_data)
        # print('Receive:', packet)
        await self.deserialize_comment(packet['data'], packet['event_type']) # 0: Create / Update; 1: Delete
        
        try:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'forum_message'
                }
            )
        except Exception as except_obj:
            print('Error in receive', except_obj)
            await self.close()


    async def forum_message(self, event):
        """Runs when updating the room about new comment.
        """
        # Send message to WebSocket
        serialized_data = await self.serialize_forum()
        await self.send(
            text_data=serialized_data
        )


    #############################################
    # Serializer Methods
    #############################################


    async def serialize_forum(self):
        """Serializes the forum tree.
        
        Returns:
            string -- serialized json tree.
        """
        try:
            queryset = await self.get_forum()
            serializer_data = ForumListSerializer(queryset, many=True).data
            return json.dumps(serializer_data)

        except Exception as excep_obj:
            print('Error in serialize_forum: ', excep_obj)
            await self.close()
    

    async def deserialize_comment(self, serialized_data, event_type):
        """Deserializes a comment
        
        Arguments:
            serialized_data {json} -- serialized data of a comment.
        
        Raises:
            ValidationError -- Raise when a Validation Error.
        
        Returns:
            object -- Validation Errors.
        """

        try:
            serializer = ForumSerializer(data=serialized_data)
            if serializer.is_valid(raise_exception=True):
                if event_type == 1: # 0: Create/Update: Delete
                    # import ipdb
                    # ipdb.set_trace()
                    await self.delete_instance(serializer.validated_data['id'])
                else:
                    del serializer.validated_data['id']
                    serializer.save()

        except ValidationError as except_obj:
            print('Validation Error in deserialize comment: ', except_obj)
        except Exception as except_obj:
            print('Error in deserialize_comment: ', except_obj)
            await self.close()


    #############################################
    # Database Methods
    #############################################
    
    
    @database_sync_to_async
    def get_forum(self):
        """Returns a queryset of all the threads in a forum.
        """
        try:
            return Forum.objects.filter(course_id=self.scope['url_route']['kwargs']['course_room_id'], parent_id=None)
        except Exception as excep_obj:
            print('Error in get_forum: ', excep_obj)   

    @database_sync_to_async
    def delete_instance(self, id):
        """Deletes a forum model instance.
        
        Arguments:
            id {int} -- id of a forum model instance.
        """
        # import ipdb
        # ipdb.set_trace()
        Forum.objects.get(id=id).delete()
















