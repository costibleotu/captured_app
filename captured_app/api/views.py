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



# ________________START SECTION 1__________________

def chart_level_of_sc(request):
    charts = {
        "data":{
            "type": 'line',
            "columns": [
                ['Petroleum Products', 48, 29, 36, 36],
                ['Construction Work', 65, 29, 56, 57],
                ['Business Services', 6, 11, 34, 31],
                ['Architectural Services', 45, 37, 44, 37],
            ]
        },
        "axis": {
            "x": {
              "type": "category",
              "categories": ['2009', '2010', '2011', '2012']
            }
          },
          "title": {
            "text":  "Level of State Capture"
          }
    }

    return charts


def estimated_money_spent_on_high_corruption_risk_contracts_by_market(request):
    country = models.Country.objects.get(name=request.GET.get('country', 'Hungary'))
    markets = models.Market.objects.filter(name__in= request.GET.get('markets', 'Construction').split(','))
    years = request.GET.get('years', '2012').split(',')
    data = []

    for market in markets:
        cri_values = models.Contract.objects.filter(market=market, country=country).values_list('cri_comp', flat=True)
        s = pd.Series(cri_values).describe()

        high_cri = s['75%']

        targeted_contracts_political = models.Contract.objects.filter(cri_comp__gte=high_cri).filter(market=market, country=country).filter(ich_i__gt=0).filter(ca_year__year__in=years).aggregate(total_ca_value=Sum('ca_contract_value'))

        data.append([market.name + ' [PC]', targeted_contracts_political['total_ca_value']])
        targeted_contracts_bussiness = models.Contract.objects.filter(cri_comp__gte=high_cri).filter(market=market).filter(sch_s__gt=0).filter(ca_year__year__in=years).aggregate(total_ca_value=Sum('ca_contract_value'))

        data.append([market.name + ' [BC]', targeted_contracts_bussiness['total_ca_value']])

    return {
        "data": {
            'type': 'bar',
            'columns': data
        },
        "title": {"text": "Estimated money spent on high corruption risk contracts by market"}
    }



def top10_high_corruption_risk_organizations(request):
    country = models.Country.objects.get(name=request.GET.get('country', 'Hungary'))
    markets = models.Market.objects.filter(name__in= request.GET.get('markets', 'Construction').split(','))
    years = request.GET.get('years', '2012').split(',')
    data = []
    columns = [
            { 'title': "Issuer" },
            { 'title': "Average CRI" },
        ]
    contracts = models.Contract.objects.filter(country=country).filter(market__in=markets, ca_year__year__in=years).values('issuer__anb_name').annotate(avg_cri=Avg('cri_comp')).order_by('-avg_cri')[:10]
    # issuers = 
    for c in contracts:
        data.append([c['issuer__anb_name'], c['avg_cri']])

    return {
        "columns": columns,
        "paging": 0,
        "searching": 0,
        "info": 0,
        "data": data
    }


def top10_low_corruption_risk_organizations(request):
    country = models.Country.objects.get(name=request.GET.get('country', 'Hungary'))
    markets = models.Market.objects.filter(name__in= request.GET.get('markets', 'Construction').split(','))
    years = request.GET.get('years', '2012').split(',')
    data = []

    columns = [
            { 'title': "Issuer" },
            { 'title': "Average CRI" },
        ]

    contracts = models.Contract.objects.filter(country=country).filter(market__in=markets, ca_year__year__in=years).values('issuer__anb_name').annotate(avg_cri=Avg('cri_comp')).order_by('avg_cri')[:10]

    for c in contracts:
        data.append([c['issuer__anb_name'], c['avg_cri']])

    return {
        "columns": columns,
        "paging": 0,
        "searching": 0,
        "info": 0,
        "data": data
    }



def section_1(request):
    section_data ={ 
        "charts": [
        chart_level_of_sc(request),
        estimated_money_spent_on_high_corruption_risk_contracts_by_market(request),
    ],
        "tables":[
        top10_high_corruption_risk_organizations(request),
        top10_low_corruption_risk_organizations(request),
    ]}

    response = HttpResponse(
        json.dumps(section_data, indent=4),
        content_type="application/json"
    )
    response['Access-Control-Allow-Origin'] = '*'
    return response

# ________________END SECTION 1__________________





# ________________START SECTION 2__________________

def chart_type_of_sc(request):
    charts = {
        "data":{
            "type": 'line',
            "columns": [],
        },
        "axis": {
            "x": {
              "type": "category",
              "categories": ['2009', '2010', '2011', '2012']
            }
          },
          "title": {"text": "Type of State Capture"}
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
    charts['data']['columns'] = data

    return charts



def top10_high_corruption_risk_issuers(request):
    country = models.Country.objects.get(name=request.GET.get('country', 'Hungary'))
    markets = models.Market.objects.filter(name__in= request.GET.get('markets', 'Construction').split(','))
    years = request.GET.get('years', '2012').split(',')
    data = []

    contracts = models.Contract.objects.filter(country=country).filter(market__in=markets).filter(ca_year__year__in=years).values('issuer__anb_name').annotate(avg_cri=Avg('cri_comp')).order_by('-avg_cri')[:10]
    # issuers = 
    for c in contracts:
        data.append([ c['issuer__anb_name'], c['avg_cri']])
    
    columns = [
            { 'title': "Issuer" },
            { 'title': "Average CRI" },
        ]
    return {
        "columns": columns,
        "paging": 0,
        "searching": 0,
        "info": 0,
        "data": data
    }


def top10_high_corruption_risk_winners(request):
    country = models.Country.objects.get(name=request.GET.get('country', 'Hungary'))
    markets = models.Market.objects.filter(name__in= request.GET.get('markets', 'Construction').split(','))
    years = request.GET.get('years', '2012').split(',')
    data = []

    contracts = models.Contract.objects.filter(country=country).filter(market__in=markets, ca_year__year__in=years).values('winner__w_name').annotate(avg_cri=Avg('cri_comp')).order_by('-avg_cri')[:10]
    # issuers = 
    for c in contracts:
        data.append([c['winner__w_name'], c['avg_cri']])

    columns = [
            { 'title': "Winner" },
            { 'title': "Average CRI" },
        ]
    return {
        "columns": columns,
        "paging": 0,
        "searching": 0,
        "info": 0,
        "data": data
    }


def estimated_money_spent_on_high_corruption_risk_contracts(request):
    country = models.Country.objects.get(name=request.GET.get('country', 'Hungary'))
    markets = models.Market.objects.filter(name__in= request.GET.get('markets', 'Construction').split(','))
    years = request.GET.get('years', '2012').split(',')
    data = []
    political_capture = models.Contract.objects.exclude(ich_i=0).filter(market__in=markets).filter(ca_year__year__in=years).aggregate(total_ca_value=Sum('ca_contract_value'))
    bussiness_capture = models.Contract.objects.exclude(sch_s=0).filter(market__in=markets).filter(ca_year__year__in=years).aggregate(total_ca_value=Sum('ca_contract_value'))

    data.append(['Politcal Capture', political_capture['total_ca_value']])
    data.append(['Bussiness Capture', bussiness_capture['total_ca_value']])


    return {
        "data": {
            'type': 'bar',
            'columns': data 
        },
        "title": {"text": "Estimated money spent on high corruption risk contracts"}
    }



def section_2(request):
    section_data ={ 
        "charts": [
        chart_type_of_sc(request),
        estimated_money_spent_on_high_corruption_risk_contracts(request),
    ],
        "tables":[
        top10_high_corruption_risk_issuers(request),
        top10_high_corruption_risk_winners(request),
    ]}

    response = HttpResponse(
        json.dumps(section_data, indent=4),
        content_type="application/json"
    )
    response['Access-Control-Allow-Origin'] = '*'
    return response

# ________________ END SECTION 2__________________



# ________________ START SECTION 3__________________


def geographical_patterns(request):
    country = models.Country.objects.get(name=request.GET.get('country', 'Hungary'))
    markets = models.Market.objects.filter(name__in= request.GET.get('markets', 'Construction').split(','))
    years = request.GET.get('years', '2012').split(',')
    data = []
    # for market in markets:
    cri_values = models.Contract.objects.filter(country=country).filter(market__in=markets).filter(ca_year__year__in=years).values_list('cri_comp', flat=True)
    s = pd.Series(cri_values).describe()

    high_cri = s['75%']
    targeted_contracts = models.Contract.objects.filter(cri_comp__gte=high_cri).filter( country=country).filter(market__in=markets).filter(ca_year__year__in=years).exclude(ca_nuts=None).values('ca_nuts').annotate(total_ca_value=Sum('ca_contract_value')).order_by('-total_ca_value')
    for c in targeted_contracts:
        print(c)
        data.append([c['ca_nuts'], c['total_ca_value']])

    return {
        "data": {
            'type': 'bar',
            'columns': data,
        },
        "axis": {
            "rotated": 1,
        },
        "title": {"text": "Geographical patterns"}
    }


def section_3(request):
    section_data ={ 
        "charts": [
        geographical_patterns(request),
    ]}

    response = HttpResponse(
        json.dumps(section_data, indent=4),
        content_type="application/json"
    )
    response['Access-Control-Allow-Origin'] = '*'
    return response

# ________________ END SECTION 3__________________








def top_10_issuers_controlling_political_capture(request):
    country = models.Country.objects.get(name='Hungary')
    markets = models.Market.objects.filter(name="Construction")
    years = ['2009']
    data = []

    contracts = models.Contract.objects.filter(country=country).filter(market__in=markets).filter(ca_year__year__in=years).values('issuer__anb_name').annotate(avg_ichi=Avg('ich_i')).order_by('-avg_ichi')[:10]
    # issuers = 
    for c in contracts:
        data.append([c['avg_ichi'], c['issuer__anb_name']])
    response = HttpResponse(
        json.dumps(data, indent=4),
        content_type="application/json"
    )
    response['Access-Control-Allow-Origin'] = '*'
    return response


def top_10_suppliers_controlling_business_capture(request):
    country = models.Country.objects.get(name='Hungary')
    markets = models.Market.objects.filter(name="Construction")
    years = ['2009']
    data = []

    contracts = models.Contract.objects.filter(country=country).filter(market__in=markets).filter(ca_year__year__in=years).values('winner__w_name').annotate(avg_schs=Avg('sch_s')).order_by('-avg_schs')[:10]
    # issuers = 
    for c in contracts:
        data.append([c['avg_schs'], c['winner__w_name']])
    response = HttpResponse(
        json.dumps(data, indent=4),
        content_type="application/json"
    )
    response['Access-Control-Allow-Origin'] = '*'
    return response






# ________________ START SECTION 4__________________

def corruption_risks_by_issuer_type_national_regional(request):
    country = models.Country.objects.get(name=request.GET.get('country', 'Hungary'))
    markets = models.Market.objects.filter(name__in= request.GET.get('markets', 'Construction').split(','))
    years = request.GET.get('years', '2012').split(',')
    markets_values = markets.values_list('name', flat=True)
    data = []
    map_types = {
        "national ": "National",
        "regional/local ": "Regional/Local",
    }
    anb_types = ['national ', 'regional/local ']
    final_data = {}
    cri_values = models.Contract.objects.filter(country=country, market__in=markets, anb_type__in=anb_types).filter(ca_year__year__in=years).values_list('cri_comp', flat=True)

    s = pd.Series(cri_values).describe()

    high_cri = s['75%']
    targeted_contracts = models.Contract.objects.filter(cri_comp__gte=high_cri).filter( country=country, market__in=markets, anb_type__in=anb_types).filter(ca_year__year__in=years).values('issuer__influence', 'anb_type')

    for c in targeted_contracts:
        final_data.setdefault(c['anb_type'],0)
        if c['issuer__influence']:
            for k,v in c['issuer__influence'].items():
                if list(v)[0] in markets_values:
                    final_data[c['anb_type']] += v[list(v)[0]]['contracts_no']
    for k,v in final_data.items():
        data.append([map_types[k],v])

    return {
        "data": {
            'type': 'bar',
            'columns': data,
        },
        "title": {"text": "Corruption risks by issuer type (national/regional)"}
    }

def corruption_risks_by_issuer_type_public_private(request):
    country = models.Country.objects.get(name=request.GET.get('country', 'Hungary'))
    markets = models.Market.objects.filter(name__in= request.GET.get('markets', 'Construction').split(','))
    years = request.GET.get('years', '2012').split(',')
    markets_values = markets.values_list('name', flat=True)
    data = []
    map_types = {
        "established by public law": "Public",
        "supported body/soe ": "State Owned Enterprise",
        "other/private ": "Private"
    }

    anb_types = ['established by public law', 'other/private ', 'supported body/soe ']
    final_data = {}
    cri_values = models.Contract.objects.filter(country=country, market__in=markets, anb_type__in=anb_types).filter(ca_year__year__in=years).values_list('cri_comp', flat=True)

    s = pd.Series(cri_values).describe()

    high_cri = s['75%']
    targeted_contracts = models.Contract.objects.filter(cri_comp__gte=high_cri).filter( country=country, market__in=markets, anb_type__in=anb_types).filter(ca_year__year__in=years).values('issuer__influence', 'anb_type')

    for c in targeted_contracts:
        final_data.setdefault(c['anb_type'],0)
        if c['issuer__influence']:
            for k,v in c['issuer__influence'].items():
                if list(v)[0] in markets_values:
                    final_data[c['anb_type']] += v[list(v)[0]]['contracts_no']
    for k,v in final_data.items():
        data.append([map_types[k],v])
    return {
        "data": {
            'type': 'bar',
            'columns': data,
        },
        "title": {"text": "Corruption risks by issuer type (public/private)"}
    }



def top_10_high_corruption_risk_issuers_national(request):
    country = models.Country.objects.get(name=request.GET.get('country', 'Hungary'))
    markets = models.Market.objects.filter(name__in= request.GET.get('markets', 'Construction').split(','))
    years = request.GET.get('years', '2012').split(',')
    data = []

    contracts = models.Contract.objects.filter(country=country, market__in=markets, anb_type='national ').filter(ca_year__year__in=years).values('issuer__anb_name').annotate(avg_cri=Avg('cri_comp')).order_by('-avg_cri')[:10]
    # issuers = 
    for c in contracts:
        data.append([c['issuer__anb_name'], c['avg_cri']])

    columns = [
            { 'title': "Issuer" },
            { 'title': "Average CRI" },
        ]
    return {
        "columns": columns,
        "paging": 0,
        "searching": 0,
        "info": 0,
        "data": data
    }



def top_10_high_corruption_risk_issuers_regional(request):
    country = models.Country.objects.get(name=request.GET.get('country', 'Hungary'))
    markets = models.Market.objects.filter(name__in= request.GET.get('markets', 'Construction').split(','))
    years = request.GET.get('years', '2012').split(',')
    data = []

    contracts = models.Contract.objects.filter(country=country, market__in=markets, anb_type='regional/local ').filter(ca_year__year__in=years).values('issuer__anb_name').annotate(avg_cri=Avg('cri_comp')).order_by('-avg_cri')[:10]
    # issuers = 
    for c in contracts:
        data.append([c['issuer__anb_name'], c['avg_cri']])

    columns = [
            { 'title': "Issuer" },
            { 'title': "Average CRI" },
        ]
    return {
        "columns": columns,
        "paging": 0,
        "searching": 0,
        "info": 0,
        "data": data
    }


def section_4(request):
    section_data ={ 
        "charts": [
            corruption_risks_by_issuer_type_national_regional(request),
            corruption_risks_by_issuer_type_public_private(request),
        ],
        "tables":[
            top_10_high_corruption_risk_issuers_national(request),
            top_10_high_corruption_risk_issuers_regional(request)
        ]
        }

    response = HttpResponse(
        json.dumps(section_data, indent=4),
        content_type="application/json"
    )
    response['Access-Control-Allow-Origin'] = '*'
    return response

# ________________ END SECTION 4__________________


# Scatterplot - x-axis = CRI, default threshold line 0.5; y-axis = Influence, default threshold line 0.5; Priority quadrants: 1 = high CRI, high Influence, 2 = high CRI, low Influence, 3 = low CRI, high Influence, 4 = low CRI, low Influence



# ________________ START SECTION 6__________________

def intervention_priority_matrix(request):
    country = models.Country.objects.get(name=request.GET.get('country', 'Hungary'))
    markets = models.Market.objects.filter(name__in= request.GET.get('markets', 'Construction').split(','))
    years = request.GET.get('years', '2012').split(',')
    contracts = models.Contract.objects.filter(country=country, market__in=markets).exclude(issuer__influence=None).values('issuer__anb_name', 'issuer__influence').annotate(avg_cri=Avg('cri_comp')).prefetch_related('issuer')
    # print(contracts)
    data = []
    for contract in contracts:
        contract_dict = {
            "cri": contract['avg_cri'],
            "issuer": contract['issuer__anb_name']
        }
        influence_count = 0
        for year in years:
            for market in markets.values_list('name', flat=True):
                try:
                    contract_dict.setdefault('influence',0)
                    influence = contract['issuer__influence'][year][market]['influence']
                    contract_dict['influence'] += influence
                    influence_count += 1
                except Exception as e:
                    print(e)
                except Exception as e:
                    # print(e)
                    pass
        contract_dict['influence'] = contract_dict['influence']/influence_count if influence_count else contract_dict['influence']
        data.append(contract_dict)

    return {
        "data": {
            'type': 'scatter',
            'columns': data,
        },
        "title": {"text": "Corruption risks by issuer type (public/private)"}
    }


def section_6(request):
    section_data ={ 
        "charts": [
            intervention_priority_matrix(request),
        ]
        }

    response = HttpResponse(
        json.dumps(section_data, indent=4),
        content_type="application/json"
    )
    response['Access-Control-Allow-Origin'] = '*'
    return response

# ________________ END SECTION 6__________________


# Issuer connected to winner through public procurement contract; width of link = number of contracts; color of link = divergent palette (red/grey/green) by corruption risks (high/medium/low); size of nodes = Influence/size of nodes = Bridging Capacity; color of nodes = issuer type (national, regional/local, public, private, state-owned)



