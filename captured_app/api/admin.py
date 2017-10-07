# -*- coding: utf-8 -*-
from api import models
from django.contrib import admin



@admin.register(models.Issuer)
class IssuerAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">fingerprint</i>'
    list_display = ('anb_id', 'anb_name', 'anb_nuts', 'influence')
    search_fields = ['anb_id', 'anb_name', 'anb_nuts']


@admin.register(models.Winner)
class WinnerAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">fingerprint</i>'
    list_display = ('w_id', 'w_name', 'w_nuts', 'influence')
    search_fields = ['w_id', 'w_name', 'w_nuts']


@admin.register(models.Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('issuer',  'winner','ich_i','category','market', 'cri_comp','ca_title','country','ca_date','ca_contract_value','cpv_div', 'contract_value_category')
    icon = '<i class="material-icons">settings_input_composite</i>'
    search_fields = ['anb_id']
    list_filter = ['country', 'market', 'contract_value_category', 'ca_nuts', 'anb_type']


@admin.register(models.CategoryCode)
class CategoryCodeAdmin(admin.ModelAdmin):
	list_display = ('code', 'title')
	search_fields = ['code', 'title']


@admin.register(models.Market)
class MarketAdmin(admin.ModelAdmin):
    list_display = ('name', 'long_name')
    search_fields = ['name', 'long_name']

@admin.register(models.StateCapture)
class StateCaptureAdmin(admin.ModelAdmin):
    list_display = ('market', 'values')

@admin.register(models.LevelStateCapture)
class LevelStateCaptureAdmin(admin.ModelAdmin):
    list_display = ('country', 'values')