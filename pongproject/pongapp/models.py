from django.db import models

class GameResult(models.Model):
    player1_name = models.CharField(max_length=30)
    player2_name = models.CharField(max_length=30)
    player1_score = models.IntegerField()
    player2_score = models.IntegerField()
    played_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.player1_name} {self.player1_score} - {self.player2_score} {self.player2_name}"