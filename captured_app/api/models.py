from django.db import models


class CategoryCode(models.Model):
    code = models.CharField(max_length=20)
    title = models.CharField(max_length=300)


    def __str__(self):
        return '{}({})'.format(self.code, self.title)


class Issuer(models.Model):
    anb_id = models.CharField(max_length=10)
    anb_name = models.CharField(max_length=100)
    anb_nuts = models.CharField(null=True, blank=True, max_length=100)

    def __str__(self):
        return self.anb_id

class Winner(models.Model):
    w_id = models.CharField(max_length=20)
    w_name = models.CharField(max_length=200)
    w_nuts = models.CharField(null=True, blank=True, max_length=100)
    w_consortium = models.IntegerField(null=True)

    def __str__(self):
        return self.w_id

class Contract(models.Model):
    issuer = models.ForeignKey(Issuer, null=True)
    winner = models.ForeignKey(Winner, null=True)
    category = models.ForeignKey(CategoryCode, null=True)
    
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

    country = models.CharField(max_length=20, null=True)
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
