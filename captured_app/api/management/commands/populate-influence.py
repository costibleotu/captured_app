# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.core import exceptions
from api import models
import csv
from unidecode import unidecode
from bs4 import UnicodeDammit
from pprint import pprint 
from datetime import datetime
import codecs

import ftfy
from unidecode import unidecode
from glob import glob


class Command(BaseCommand):
    help = 'Will try to import json file'

    def handle(self, *args, **options):
        self.populate_influence()



    def populate_influence(self):
        for i in models.Influence.objects.all():
            try:
                issuer = models.Issuer.objects.get(anb_id=i.obj_id)
                if not issuer.influence:
                    issuer.influence = {}
                issuer.influence.setdefault(i.year.strftime('%Y'), {})
                issuer.influence[i.year.strftime('%Y')][i.market.name]={
                    "contracts_no": i.contracts_no,
                    "bridging_capacity": i.bridging_capacity,
                    "influence": i.influence,
                    "infl_norm": i.infl_norm
                }
                print(issuer.influence)
                issuer.save()
            except Exception as ee:
                try:
                    winner = models.Winner.objects.get(w_id=i.obj_id)
                    if not winner.influence:
                        winner.influence = {}
                    winner.influence.setdefault(i.year.strftime('%Y'), {})
                    winner.influence[i.year.strftime('%Y')][i.market.name]={
                        "contracts_no": i.contracts_no,
                        "bridging_capacity": i.bridging_capacity,
                        "influence": i.influence,
                        "infl_norm": i.infl_norm
                    }
                    winner.save()
                    print(winner.influence)
                except Exception as e:
                    # print(e)
                    print(i.obj_id)
                    i.delete()
