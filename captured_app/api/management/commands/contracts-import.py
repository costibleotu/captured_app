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


class Command(BaseCommand):
    help = 'Will try to import json file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--from-file',
            dest='from-file',
            required=True )

    def handle(self, *args, **options):
        self.do_bulk_import(
                file=options.get( 'from-file' )
            )



    def do_bulk_import(self, file):

        with open(file, encoding="ISO-8859-1") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            line = 0
            for row in reader:
                new_row = {}
                # print(unidecode(ftfy.fix_text(row['anb_name']).replace('?','o')))
                line += 1
                if line > 100:
                    pass
                print (row)
                try:
                    if row['rowid']:
                        contract = models.Contract.objects.get(rowid=row['rowid'])

                except:
                    try:
                        issuer = models.Issuer.objects.get(anb_id=row['Source'])
                    except:
                        issuer = models.Issuer.objects.create(
                            anb_id=row['Source'],
                            anb_name=unidecode(ftfy.fix_text(row['anb_name']).replace('?','o')),
                            anb_nuts=row.get('anb_nuts')
                            )
                    try:
                        winner = models.Winner.objects.get(w_id=row['Target'])
                    except:
                        winner = models.Winner.objects.create(
                            w_id=row['Target'],
                            w_name=unidecode(ftfy.fix_text(row['w_name']).replace('?','o')),
                            w_nuts=row.get('w_nuts'))

                    try:
                        category = models.CategoryCode.objects.get(code=row['ca_cpv'])
                    except:
                        category = None

                    cpv_div=row.get('cpv_div', '').strip()


                    if not cpv_div.replace(' ',''):
                        if file[:2] == 'PP':
                            cpv_div = 'petroleum products, fuel, electricity and other sources of energy'
                        elif file[:2] == 'BS':
                            cpv_div = 'business services: law, marketing, consulting, recruitment, printing and security'
                        elif file[:2] == 'AS':
                            cpv_div = 'architectural, construction, engineering and inspection services'
                        else:
                            cpv_div = 'construction work'
                    market = models.Market.objects.get(long_name=cpv_div)

                    for k,v in row.items():
                        print('{}-{}-{}'.format(k,v,len(v)))

                    if row.get('ca_scntr_sc').replace('NA','')=='':
                        ca_scntr_sc = None
                    else:
                        ca_scntr_sc = int(row.get('ca_scntr_sc'))

                    ca_contract_value = row.get('ca_contract_value').replace('.','').replace('NA', '') if row.get('ca_contract_value').count('.')>1 else row.get('ca_contract_value').replace(',','.').strip()
                    if ca_contract_value == '':
                        ca_contract_value = None

                    print('======')
                    if row.get('country', 'hungary'):
                        country_str = row.get('country', 'hungary')
                    else:
                        country_str = 'hungary'
                    print(country_str)
                    country = models.Country.objects.get(short=country_str)

                    # print('-----')
                    contract = models.Contract.objects.create(
                        issuer=issuer,
                        winner=winner,
                        category=category,
                        market=market,
                        country=country,
                        rowid=row.get('rowid'),
                        cri_comp=row.get('cri_comp', None).replace(',','.'),
                        icl_i=row.get('icl.i') if row.get('icl.i', '').replace('NA', '') else None,
                        ich_i=row.get('ich.i') if row.get('ich.i', '').replace('NA', '') else None,
                        icm_i=row.get('icm.i') if row.get('icm.i', '').replace('NA', '') else None,
                        scl_s=row.get('scl.s') if row.get('scl.s', '').replace('NA', '') else None,
                        sch_s=row.get('sch.s') if row.get('sch.s', '').replace('NA', '') else None,
                        scm_s=row.get('scm.s') if row.get('scm.s', '').replace('NA', '') else None,
                        ca_bids=row.get('ca_bids') if row.get('ca_bids', '').replace('NA', '') else None,
                        ca_cpv=row.get('ca_cpv'),
                        ca_criteria_count=row.get('ca_criteria_count') if row.get('ca_criteria_count','').replace('NA', '') else None,
                        ca_eufund=row.get('ca_eufund') if row.get('ca_eufund','').replace('NA', '') else None,
                        ca_nuts=row.get('ca_nuts'),
                        ca_scntr_sc=ca_scntr_sc,
                        ca_title=unidecode(ftfy.fix_text(row.get('ca_title','')).replace('?','o')),
                        ca_date=datetime.strptime(row.get('ca_date'),'%d-%b-%y') if row.get('ca_date') else None,
                        ca_year=datetime.strptime(row.get('ca_year'),'%Y') if row.get('ca_year') else None,
                        ca_contract_value=ca_contract_value,
                        nocft=row.get('nocft') if row.get('nocft') else None,
                        ca_procedure=row.get('ca_procedure'),
                        ca_criterion=row.get('ca_criterion'),
                        anb_type=row.get('anb_type'),
                        anb_sector=row.get('anb_sector'),
                        anb_empl_cat=row.get('anb_empl_cat'),
                        cpv_div=cpv_div,
                        # cpv_div=row.get('cpv_div', 'construction work')
                        )


