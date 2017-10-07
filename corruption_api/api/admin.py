# -*- coding: utf-8 -*-
from api import models
from django.contrib import admin



@admin.register(models.Issuer)
class IssuerAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">fingerprint</i>'
    list_display = ('anb_id', 'anb_name', 'anb_nuts')
    search_fields = ['anb_id', 'anb_name', 'anb_nuts']


@admin.register(models.Winner)
class WinnerAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">fingerprint</i>'
    list_display = ('w_id', 'w_name', 'w_nuts')
    search_fields = ['w_id', 'w_name', 'w_nuts']


@admin.register(models.Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('issuer', 'winner','category','rowid','ca_bids','ca_cpv','ca_nuts','ca_scntr_sc','ca_title','country','ca_date','ca_contract_value','ca_procedure','ca_criterion')
    icon = '<i class="material-icons">settings_input_composite</i>'
    search_fields = ['country']

@admin.register(models.CategoryCode)
class CategoryCodeAdmin(admin.ModelAdmin):
	list_display = ('code', 'title')
	search_fields = ['code', 'title']