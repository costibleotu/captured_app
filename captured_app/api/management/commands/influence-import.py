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

    def add_arguments(self, parser):
        parser.add_argument(
            '--from-dir',
            dest='from-dir',
            required=True )

    def handle(self, *args, **options):
        self.do_bulk_import(
                s_dir=options.get( 'from-dir' )
            )



    def do_bulk_import(self, s_dir):
        markets_map = {
            "AS": "Architectural",
            "PP": "Petroleum",
            "BS": "Bussiness",
            "CW": "Construction",
        }

        country_map = {
            "HU": "Hungary",
            "SK": "Slovakia",
            "CZ": "Czech Republic"
        }
        for file in glob(s_dir + '/*'):
            print(file)
            with open(file, encoding="ISO-8859-1") as csvfile:
                filename = file.split('/')[-1].split('.')[0]
                year_str = filename.split('_')[-1]
                if filename[:2] in markets_map.keys():
                    market = models.Market.objects.get(name=markets_map[filename[:2]])
                    country = models.Country.objects.get(name='Hungary')
                else:
                    market = models.Market.objects.get(name='Construction')
                    country = models.Country.objects.get(name=country_map[filename[:2]])
                # print(country)
                reader = csv.DictReader(csvfile, delimiter=',')
                for row in reader:
                    print(row)
                    try:
                        year = datetime.strptime(year_str,'%Y')
                        influence = models.Influence.objects.get(obj_id=row['id'], year=year)
                    except Exception as e:
                        influence = models.Influence.objects.create(
                            obj_id=row['id'],
                            year=year,
                            contracts_no=row['Contracts'],
                            bridging_capacity=row['Bridging Capacity'],
                            influence=row['Influence'],
                            market=market)
