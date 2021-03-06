from __future__ import absolute_import, unicode_literals
from django.conf.urls import include, url
from django.contrib import admin
from api import views


urlpatterns = [
	

    url( r'^section-1/$', views.section_1),
    url( r'^section-2/$', views.section_2),
    url( r'^section-3/$', views.section_3),
    url( r'^section-4/$', views.section_4),

    url( r'^chart_type_of_sc/$', views.chart_type_of_sc ),
    url( r'^chart_level_of_sc/$', views.chart_level_of_sc ),
    url( r'^estimated_money_spent_on_high_corruption_risk_contracts/$', views.estimated_money_spent_on_high_corruption_risk_contracts ),
    url( r'^top10_high_corruption_risk_organizations/$', views.top10_high_corruption_risk_organizations ),
    url( r'^top10_low_corruption_risk_organizations/$', views.top10_low_corruption_risk_organizations ),
    url( r'^estimated_money_spent_on_high_corruption_risk_contracts_by_market/$', views.estimated_money_spent_on_high_corruption_risk_contracts_by_market ),
    url( r'^top_10_issuers_controlling_political_capture/$', views.top_10_issuers_controlling_political_capture ),
    url( r'^top_10_suppliers_controlling_business_capture/$', views.top_10_suppliers_controlling_business_capture ),
    url( r'^geographical_patterns/$', views.geographical_patterns ),
    url( r'^corruption_risks_by_issuer_type_national_regional/$', views.corruption_risks_by_issuer_type_national_regional ),
    url( r'^corruption_risks_by_issuer_type_public_private/$', views.corruption_risks_by_issuer_type_public_private ),
    url( r'^top_10_high_corruption_risk_issuers_national/$', views.top_10_high_corruption_risk_issuers_national ),
    url( r'^top_10_high_corruption_risk_issuers_regional/$', views.top_10_high_corruption_risk_issuers_regional ),
    url( r'^intervention_priority_matrix/$', views.intervention_priority_matrix ),
]

