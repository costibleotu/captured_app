from __future__ import absolute_import, unicode_literals
from django.conf.urls import include, url
from django.contrib import admin
from api import views


urlpatterns = [
    url( r'^winners/$', views.winners_list ),
    url( r'^chart_type_of_sc/$', views.chart_type_of_sc ),
    url( r'^chart_level_of_sc/$', views.chart_level_of_sc ),
    url( r'^estimated_money_spent_on_high_corruption_risk_contracts/$', views.estimated_money_spent_on_high_corruption_risk_contracts ),
    url( r'^top10_high_corruption_risk_organizations/$', views.top10_high_corruption_risk_organizations ),
    url( r'^top10_low_corruption_risk_organizations/$', views.top10_low_corruption_risk_organizations ),
    url( r'^estimated_money_spent_on_high_corruption_risk_contracts/$', views.estimated_money_spent_on_high_corruption_risk_contracts ),
    url( r'^top_10_issuers_controlling_political_capture/$', views.top_10_issuers_controlling_political_capture ),
    url( r'^top_10_suppliers_controlling_business_capture/$', views.top_10_suppliers_controlling_business_capture ),
    url( r'^geographical_patterns/$', views.geographical_patterns ),
    url( r'^corruption_risks_by_issuer_type1/$', views.corruption_risks_by_issuer_type1 ),
    url( r'^corruption_risks_by_issuer_type2/$', views.corruption_risks_by_issuer_type2 ),
    url( r'^top_10_high_corruption_risk_issuers/$', views.top_10_high_corruption_risk_issuers ),
    url( r'^top_10_high_corruption_risk_winners/$', views.top_10_high_corruption_risk_winners ),
]



