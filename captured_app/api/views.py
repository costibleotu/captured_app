from django.shortcuts import render
from api import models
from django.http import HttpResponse
import json
# Create your views here.



def winners_list(request):
    winners = []
    for w in models.Winner.objects.all():
        winners.append(dict(
            w_id=w.w_id,
            w_name=w.w_name,
            w_nuts=w.w_nuts,
            w_consortium=w.w_consortium
            ))
    response = HttpResponse(
        json.dumps(winners, indent=4),
        content_type="application/json"
    )
    response['Access-Control-Allow-Origin'] = '*'
    return response
