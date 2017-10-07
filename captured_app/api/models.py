from django.db import models
from django.contrib.postgres.fields import ArrayField, HStoreField, JSONField

class CategoryCode(models.Model):
    code = models.CharField(max_length=20)
    title = models.CharField(max_length=300)

    def __str__(self):
        return '{}({})'.format(self.code, self.title)


class Influence(models.Model):
    market = models.ForeignKey('api.Market')
    obj_id = models.CharField(max_length=20)
    contracts_no = models.IntegerField()
    bridging_capacity = models.IntegerField()
    influence = models.FloatField()
    year = models.DateField()


class Country(models.Model):
    name = models.CharField(max_length=30)
    short = models.CharField(max_length=20)

    def __str__(self):
        return '{}'.format(self.name)


class Market(models.Model):
    name = models.CharField(max_length=50)
    long_name = models.CharField(max_length=200)


    def __str__(self):
        return 'Market: {}'.format(self.name)

class StateCapture(models.Model):
    market = models.ForeignKey(Market)
    values = JSONField()

class LevelStateCapture(models.Model):
    country = models.ForeignKey(Country)
    values = JSONField()

class Issuer(models.Model):
    anb_id = models.CharField(max_length=10)
    anb_name = models.CharField(max_length=100)
    anb_nuts = models.CharField(null=True, blank=True, max_length=100)
    anb_type = models.CharField(max_length=50, null=True)
    anb_sector = models.CharField(max_length=50, null=True)
    influence = JSONField(null=True)

    def __str__(self):
        return self.anb_id


class Winner(models.Model):
    w_id = models.CharField(max_length=20)
    w_name = models.CharField(max_length=200)
    w_nuts = models.CharField(null=True, blank=True, max_length=100)
    w_consortium = models.IntegerField(null=True)
    influence = JSONField(null=True)

    def __str__(self):
        return self.w_id


class Contract(models.Model):
    issuer = models.ForeignKey(Issuer, null=True)
    winner = models.ForeignKey(Winner, null=True)
    category = models.ForeignKey(CategoryCode, null=True)
    market = models.ForeignKey(Market, null=True)
    country = models.ForeignKey(Country)

    anb_id = models.CharField(max_length=20)
    rowid = models.CharField(null=True, max_length=20)
    cri_comp = models.FloatField()
    icl_i = models.IntegerField(null=True)
    ich_i = models.IntegerField(null=True)
    icm_i = models.IntegerField(null=True)
    scl_s = models.IntegerField(null=True)
    sch_s = models.IntegerField(null=True)
    scm_s = models.IntegerField(null=True)

    ca_bids = models.IntegerField(null=True)
    ca_cpv = models.CharField(max_length=20, null=True)
    ca_criteria_count = models.IntegerField(null=True)
    ca_eufund = models.IntegerField(null=True)
    ca_nuts = models.CharField(max_length=20, null=True)
    ca_scntr_sc = models.IntegerField(null=True)
    ca_title = models.CharField(max_length=500, null=True)

    ca_date = models.DateField(null=True)
    ca_year = models.DateField(null=True)
    ca_contract_value = models.FloatField(null=True)
    nocft = models.IntegerField(null=True)
    ca_procedure = models.CharField(max_length=50, null=True)
    ca_criterion = models.CharField(max_length=50, null=True)
    anb_type = models.CharField(max_length=50, null=True)
    anb_sector = models.CharField(max_length=50, null=True)
    anb_empl_cat =  models.CharField(max_length=20, null=True)
    anb_empl_cat_ordinal =  models.IntegerField(null=True)
    cpv_div = models.CharField(max_length=200, null=True)

    contract_value_category = models.CharField(max_length=20)

    def __str__(self):
        return '{} - {} [{}]'.format(self.issuer, self.winner, self.cri_comp)