from django.http import JsonResponse
from .models import GameResult
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render

def home(request):
    return render(request, "pongapp/home.html")

@csrf_exempt  # Protip: na produkcję lepiej zabezpieczyć inaczej ;)
def save_result(request):
    if request.method == "POST":
        data = json.loads(request.body)
        GameResult.objects.create(
            player1_name=data.get('player1'),
            player2_name=data.get('player2'),
            player1_score=data.get('score1'),
            player2_score=data.get('score2'),
        )
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "fail"}, status=400)