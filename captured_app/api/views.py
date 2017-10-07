from django.shortcuts import render
from django.db.models import Count, Min, Sum, Avg
from api import models
from django.http import HttpResponse
import json
import pandas as pd
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


def chart_type_of_sc(request):
    charts = {
        "data": [],
        "axis": {
            "x": {
              "type": "category",
              "categories": ['2009', '2010', '2011', '2012']
            }
          }
    }
    data = []
    for i in models.StateCapture.objects.all():
        sc_data = []
        curr_list = ['Political Capture']
        for year in charts['axis']['x']['categories']:
            curr_list.append(i.values[year]['Political Capture'])
        sc_data.append(curr_list)
        curr_list = ['Bussiness Capture']
        for year in charts['axis']['x']['categories']:
            curr_list.append(i.values[year]['Bussiness Capture'])
        sc_data.append(curr_list)
        data.append(sc_data)
    charts['data'] = data
        # charts.append(i.values[x[0]])
    response = HttpResponse(
        json.dumps(charts, indent=4),
        content_type="application/json"
    )
    response['Access-Control-Allow-Origin'] = '*'
    return response


def chart_level_of_sc(request):
    charts = {
        "data": [
            ['Petroleum Products', 48, 29, 36, 36],
            ['Construction Work', 65, 29, 56, 57],
            ['Business Services', 6, 11, 34, 31],
            ['Architectural Services', 45, 37, 44, 37],
        ],
        "axis": {
            "x": {
              "type": "category",
              "categories": ['2009', '2010', '2011', '2012']
            }
          }
    }

    response = HttpResponse(
        json.dumps(charts, indent=4),
        content_type="application/json"
    )
    response['Access-Control-Allow-Origin'] = '*'
    return response


def estimated_money_spent_on_high_corruption_risk_contracts(request):
    country = models.Country.objects.get(name='Hungary')
    markets = models.Market.objects.all()
    data = []
    for market in markets:
        cri_values = models.Contract.objects.filter(market=market).values_list('cri_comp', flat=True)
        s = pd.Series(cri_values).describe()

        high_cri = s['75%']
        targeted_contracts = models.Contract.objects.filter(cri_comp__gte=high_cri).filter(market=market).aggregate(total_ca_value=Sum('ca_contract_value'))
        print(targeted_contracts)
        print('------')
        data.append([market.name, targeted_contracts['total_ca_value']])
    response = HttpResponse(
        json.dumps(data, indent=4),
        content_type="application/json"
    )
    response['Access-Control-Allow-Origin'] = '*'
    return response



def top10_high_corruption_risk_organizations(request):
    country = models.Country.objects.get(name='Hungary')
    markets = models.Market.objects.all()
    data = []
    for market in markets:
        contracts = models.Contract.objects.filter(country=country).filter(market=market).values('issuer__anb_name').annotate(avg_cri=Avg('cri_comp')).order_by('-avg_cri')[:10]
        # issuers = 
        for c in contracts:
            data.append([c['avg_cri'], c['issuer__anb_name'], market.name])
    response = HttpResponse(
        json.dumps(data, indent=4),
        content_type="application/json"
    )
    response['Access-Control-Allow-Origin'] = '*'
    return response


def top10_low_corruption_risk_organizations(request):
    country = models.Country.objects.get(name='Hungary')
    markets = models.Market.objects.all()
    data = []
    for market in markets:
        contracts = models.Contract.objects.filter(country=country).filter(market=market).values('issuer__anb_name').annotate(avg_cri=Avg('cri_comp')).order_by('avg_cri')[:10]
        # issuers = 
        for c in contracts:
            data.append([c['avg_cri'], c['issuer__anb_name'], market.name])
    response = HttpResponse(
        json.dumps(data, indent=4),
        content_type="application/json"
    )
    response['Access-Control-Allow-Origin'] = '*'
    return response


def estimated_money_spent_on_high_corruption_risk_contracts(request):
    country = models.Country.objects.get(name='Hungary')
    data = []

    political_capture = models.Contract.objects.exclude(ich_i=0).aggregate(total_ca_value=Sum('ca_contract_value'))
    bussiness_capture = models.Contract.objects.exclude(sch_s=0).aggregate(total_ca_value=Sum('ca_contract_value'))

    data.append(['Politcal Capture', political_capture['total_ca_value']])
    data.append(['Bussiness Capture', bussiness_capture['total_ca_value']])
    response = HttpResponse(
        json.dumps(data, indent=4),
        content_type="application/json"
    )
    response['Access-Control-Allow-Origin'] = '*'
    return response


def top_10_issuers_controlling_political_capture(request):
    country = models.Country.objects.get(name='Hungary')
    markets = models.Market.objects.all()
    data = []
    for market in markets:
        contracts = models.Contract.objects.filter(country=country).filter(market=market).values('issuer__anb_name').annotate(avg_ichi=Avg('ich_i')).order_by('-avg_ichi')[:10]
        # issuers = 
        for c in contracts:
            data.append([c['avg_ichi'], c['issuer__anb_name'], market.name])
    response = HttpResponse(
        json.dumps(data, indent=4),
        content_type="application/json"
    )
    response['Access-Control-Allow-Origin'] = '*'
    return response


def top_10_suppliers_controlling_business_capture(request):
    country = models.Country.objects.get(name='Hungary')
    markets = models.Market.objects.all()
    data = []
    for market in markets:
        contracts = models.Contract.objects.filter(country=country).filter(market=market).values('winner__w_name').annotate(avg_schs=Avg('sch_s')).order_by('-avg_schs')[:10]
        # issuers = 
        for c in contracts:
            data.append([c['avg_schs'], c['winner__w_name'], market.name])
    response = HttpResponse(
        json.dumps(data, indent=4),
        content_type="application/json"
    )
    response['Access-Control-Allow-Origin'] = '*'
    return response


def geographical_patterns(request):
    country = models.Country.objects.get(name='Hungary')
    markets = models.Market.objects.all()
    data = []
    # for market in markets:
    cri_values = models.Contract.objects.filter( country=country).values_list('cri_comp', flat=True)
    s = pd.Series(cri_values).describe()

    high_cri = s['75%']
    targeted_contracts = models.Contract.objects.filter(cri_comp__gte=high_cri).filter( country=country).values('ca_nuts').annotate(total_ca_value=Sum('ca_contract_value')).order_by('-total_ca_value')
    for c in targeted_contracts:
        print(c)
        data.append([c['ca_nuts'], c['total_ca_value']])
    response = HttpResponse(
        json.dumps(data, indent=4),
        content_type="application/json"
    )
    response['Access-Control-Allow-Origin'] = '*'
    return response

    # Line plots, number of high corruption risk contracts (above 75% - cri_cmp) signed by national and regional/local issuers over time (for each issuer type, aggregate number of contracts across markets)


def corruption_risks_by_issuer_type1(request):
    country = models.Country.objects.get(name='Hungary')
    markets = models.Market.objects.all()
    markets_values = markets.values_list('name', flat=True)
    data = []
    anb_types = ['national ', 'regional/local ']
    final_data = {}
    cri_values = models.Contract.objects.filter(country=country, market__in=markets, anb_type__in=anb_types).values_list('cri_comp', flat=True)

    s = pd.Series(cri_values).describe()

    high_cri = s['75%']
    targeted_contracts = models.Contract.objects.filter(cri_comp__gte=high_cri).filter( country=country, market__in=markets, anb_type__in=anb_types).values('issuer__influence', 'anb_type')

    for c in targeted_contracts:
        final_data.setdefault(c['anb_type'],0)
        if c['issuer__influence']:
            for k,v in c['issuer__influence'].items():
                if list(v)[0] in markets_values:
                    final_data[c['anb_type']] += v[list(v)[0]]['contracts_no']
    for k,v in final_data.items():
        data.append([k,v])
    response = HttpResponse(
        json.dumps(data, indent=4),
        content_type="application/json"
    )
    response['Access-Control-Allow-Origin'] = '*'
    return response

def corruption_risks_by_issuer_type2(request):
    country = models.Country.objects.get(name='Hungary')
    markets = models.Market.objects.all()
    markets_values = markets.values_list('name', flat=True)
    data = []
    anb_types = ['established by public law', 'other/private ', 'supported body/soe ']
    final_data = {}
    cri_values = models.Contract.objects.filter(country=country, market__in=markets, anb_type__in=anb_types).values_list('cri_comp', flat=True)

    s = pd.Series(cri_values).describe()

    high_cri = s['75%']
    targeted_contracts = models.Contract.objects.filter(cri_comp__gte=high_cri).filter( country=country, market__in=markets, anb_type__in=anb_types).values('issuer__influence', 'anb_type')

    for c in targeted_contracts:
        final_data.setdefault(c['anb_type'],0)
        if c['issuer__influence']:
            for k,v in c['issuer__influence'].items():
                if list(v)[0] in markets_values:
                    final_data[c['anb_type']] += v[list(v)[0]]['contracts_no']
    for k,v in final_data.items():
        data.append([k,v])
    response = HttpResponse(
        json.dumps(data, indent=4),
        content_type="application/json"
    )
    response['Access-Control-Allow-Origin'] = '*'
    return response


def top_10_high_corruption_risk_issuers(request):
    country = models.Country.objects.get(name='Hungary')
    markets = models.Market.objects.all()

    data = []
    for market in markets:
        contracts = models.Contract.objects.filter(country=country, market=market, anb_type='national ').values('issuer__anb_name').annotate(avg_cri=Avg('cri_comp')).order_by('-avg_cri')[:10]
        # issuers = 
        for c in contracts:
            data.append([c['avg_cri'], c['issuer__anb_name'], market.name])
    response = HttpResponse(
        json.dumps(data, indent=4),
        content_type="application/json"
    )
    response['Access-Control-Allow-Origin'] = '*'
    return response


def top_10_high_corruption_risk_winners(request):
    country = models.Country.objects.get(name='Hungary')
    markets = models.Market.objects.all()

    data = []
    for market in markets:
        contracts = models.Contract.objects.filter(country=country, market=market, anb_type='national ').values('winner__w_name').annotate(avg_cri=Avg('cri_comp')).order_by('-avg_cri')[:10]
        # issuers = 
        for c in contracts:
            data.append([c['avg_cri'], c['winner__w_name'], market.name])
    response = HttpResponse(
        json.dumps(data, indent=4),
        content_type="application/json"
    )
    response['Access-Control-Allow-Origin'] = '*'
    return response