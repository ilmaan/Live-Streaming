import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Stream


class StreamConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for handling WebRTC signaling."""
    
    async def connect(self):
        self.stream_id = self.scope['url_route']['kwargs']['stream_id']
        self.room_group_name = f'stream_{self.stream_id}'
        self.is_host = self.scope['url_route']['kwargs'].get('is_host', False)
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # If viewer joins, increment viewer count
        if not self.is_host:
            await self.increment_viewer_count()
            # Notify host that a viewer joined
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'viewer_joined',
                    'viewer_id': self.channel_name
                }
            )
    
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
        # If viewer leaves, decrement viewer count
        if not self.is_host:
            await self.decrement_viewer_count()
    
    async def receive(self, text_data):
        """Receive message from WebSocket and broadcast to room."""
        data = json.loads(text_data)
        message_type = data.get('type')
        target = data.get('target')
        
        # Broadcast the signaling message to all peers in the room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'signal_message',
                'message_type': message_type,
                'data': data,
                'sender': self.channel_name,
                'target': target,
                'is_host': self.is_host
            }
        )
    
    async def signal_message(self, event):
        """Send signaling message to WebSocket."""
        # Don't send back to sender
        if event['sender'] == self.channel_name:
            return

        # If target is specified, only send to that specific channel
        if event['target'] and event['target'] != self.channel_name:
            return

        # Send message with sender info included
        await self.send(text_data=json.dumps({
            'type': event['message_type'],
            'sender': event['sender'],
            **event['data']
        }))
    
    async def viewer_joined(self, event):
        """Notify when a new viewer joins."""
        if self.is_host:
            await self.send(text_data=json.dumps({
                'type': 'viewer_joined',
                'viewer_id': event['viewer_id']
            }))
    
    @database_sync_to_async
    def increment_viewer_count(self):
        """Increment viewer count in database."""
        try:
            stream = Stream.objects.get(stream_id=self.stream_id)
            stream.viewer_count += 1
            stream.save()
        except Stream.DoesNotExist:
            pass
    
    @database_sync_to_async
    def decrement_viewer_count(self):
        """Decrement viewer count in database."""
        try:
            stream = Stream.objects.get(stream_id=self.stream_id)
            if stream.viewer_count > 0:
                stream.viewer_count -= 1
                stream.save()
        except Stream.DoesNotExist:
            pass
