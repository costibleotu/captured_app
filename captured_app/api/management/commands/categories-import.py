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
        with open(file) as txtfile:
            for line in txtfile:
                code = line.strip().split('\t')[0]
                title = line.strip().split('\t')[1]
                try:
                    category = models.CategoryCode.objects.get(code=code)
                except Exception as e:
                    print(e)
                    category = models.CategoryCode.objects.create(
                        code=code,
                        title=title)
                print(category)
