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
import numpy as np
import pandas as pd

class Command(BaseCommand):
    help = 'Will try to import json file'

    def handle(self, *args, **options):
        self.do_process()

    def do_process(self):
        countries = models.Country.objects.all()
        markets = models.Market.objects.all()

        for country in countries:
            for market in markets:
                print(country, market)
                contracts_values = models.Contract.objects.filter(country=country, market=market).exclude(ca_contract_value=None).values_list('ca_contract_value', flat=True)
                # print(contracts_values)
                s = pd.Series(contracts_values).describe()
                print(s)
                for contract in models.Contract.objects.filter(country=country, market=market).exclude(ca_contract_value=None):
                    # print (contract.ca_contract_value, std, mean)
                    if contract.ca_contract_value > s['75%'] :
                        contract.contract_value_category = 'high'
                    elif contract.ca_contract_value < s['25%'] :
                        contract.contract_value_category = 'low'
                    else:
                        contract.contract_value_category = 'medium'
                    contract.save()
                    print(contract.contract_value_category)
                print('========')