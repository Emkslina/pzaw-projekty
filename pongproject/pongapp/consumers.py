import json
from channels.generic.websocket import AsyncWebsocketConsumer
import asyncio
import random

class PongConsumer(AsyncWebsocketConsumer):
    players = set()
    left_paddle_y = 160
    right_paddle_y = 160
    ball_x = 300
    ball_y = 200
    ball_dx = random.choice([-3, 3])
    ball_dy = random.choice([-2, 2])
    score_left = 0
    score_right = 0
    game_task = None

    async def connect(self):
        self.room_group_name = 'pong_game'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        self.players.add(self.channel_name)

        if len(self.players) == 2 and self.game_task is None:
            self.game_task = asyncio.create_task(self.game_loop())

    async def disconnect(self, close_code):
        self.players.discard(self.channel_name)
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        if len(self.players) < 2 and self.game_task:
            self.game_task.cancel()
            self.game_task = None

    async def receive(self, text_data):
        data = json.loads(text_data)
        msg = data.get("message", {})

        # Aktualizacja pozycji paletek
        if 'leftPaddleY' in msg:
            self.left_paddle_y = msg['leftPaddleY']
        if 'rightPaddleY' in msg:
            self.right_paddle_y = msg['rightPaddleY']

    async def game_loop(self):
        while True:
            self.ball_x += self.ball_dx
            self.ball_y += self.ball_dy

            # Odbicia od góry i dołu
            if self.ball_y <= 0 or self.ball_y >= 400:
                self.ball_dy *= -1

            # Odbicia od paletek
            if (self.ball_x <= 10 and self.left_paddle_y <= self.ball_y <= self.left_paddle_y + 80):
                self.ball_dx *= -1
            elif (self.ball_x >= 590 and self.right_paddle_y <= self.ball_y <= self.right_paddle_y + 80):
                self.ball_dx *= -1

            # Punktacja i reset po punkcie
            if self.ball_x < 0:
                self.score_right += 1
                self.reset_ball()
            elif self.ball_x > 600:
                self.score_left += 1
                self.reset_ball()

            # Rozsyłanie stanu gry
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'pong_update',
                    'message': {
                        'leftPaddleY': self.left_paddle_y,
                        'rightPaddleY': self.right_paddle_y,
                        'ballX': self.ball_x,
                        'ballY': self.ball_y,
                        'scoreLeft': self.score_left,
                        'scoreRight': self.score_right,
                    }
                }
            )

            await asyncio.sleep(0.016)  # ~60 FPS

    def reset_ball(self):
        self.ball_x = 300
        self.ball_y = 200
        self.ball_dx = random.choice([-3, 3])
        self.ball_dy = random.choice([-2, 2])