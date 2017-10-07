# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from api import models


class Command(BaseCommand):
    help = 'Will try to import json file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--from-file',
            dest='from-file',
            required=True)

    def handle(self, *args, **options):
        self.do_bulk_import(
                file=options.get('from-file')
            )

    def do_bulk_import(self, file):
        create_markets()
        with open(file) as txtfile:
            for line in txtfile:
                code = line.strip().split('\t')[0]
                title = line.strip().split('\t')[1]
                try:
                    category = models.CategoryCode.objects.get(code=code)
                except Exception as e:
                    category = models.CategoryCode.objects.create(
                        code=code,
                        title=title)
                print(category)


def create_markets():
    markets = {
        "Construction": "construction work",
        "Petroleum": "petroleum products, fuel, electricity and other sources of energy",
        "Bussiness": "business services: law, marketing, consulting, recruitment, printing and security",
        "Architectural": "architectural, construction, engineering and inspection services"
    }

    countries = {
        "Czech Republic": 'czechr',
        "Hungary": 'hungary',
        "Slovakia": 'slovakia'
    }

    for k,v in markets.items():
        try:
            market = models.Market.objects.get(name=k)
        except:
            market = models.Market.objects.create(
                name=k,
                long_name=v)
            print(market)

    for k,v in countries.items():
        try:
            country = models.Country.objects.get(name=k)
        except:
            country = models.Country.objects.create(
                name=k,
                short=v)
            print(country)
