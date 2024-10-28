from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import Quiz, Question, GameSession, Player
from django.shortcuts import get_object_or_404


class QuizConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.session_id = self.scope['url_route']['kwargs']['session_id']
        self.room_group_name = f'quiz_{self.session_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        await self.send(text_data=json.dumps({
            'message': 'player has joined'
        }))

    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        await self.send(text_data=json.dumps({
            'message': 'player has left'
        }))

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message_type = data.get('type')
        if message_type == 'start_quiz':
            await self.start_quiz()
        elif message_type == 'stop_quiz':
            await self.stop_quiz()
        elif message_type == 'create_session':
            await self.create_session(data)
        elif message_type == 'join_session':
            await self.join_session(data)

    async def create_session(self, data):
        quiz_id = data['quiz_id']
        quiz = await Quiz.objects.get(id=quiz_id)
        game_session = GameSession.objects.create(quiz=quiz)

        await self.send(text_data=json.dumps({
            'message': 'Game Session Created Successfully!',
            'Game Pin': game_session.pin
        }))

    async def join_session(self, data):
        username = data['username']
        pin = data['pin']

        game_session = get_object_or_404(GameSession, pin=pin)
        player, created = Player.objects.get_or_create(username=username)

        game_session.players.add(player)
        game_session.save()

        await self.send(text_data=json.dumps({
            'message': f'{username} has joined game'
        }))

    async def player_left(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def start_quiz(self):
        await self.channel_layer.group_send(
            self.room_group_name, {
                'type': 'quiz_message',
                'message': 'Quiz started'
            }
        )

    async def stop_quiz(self):
        await self.channel_layer.group_send(
            self.room_group_name, {
                'type': 'quiz_message',
                'message': 'Quiz stopped'
            }
        )

    async def quiz_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))
