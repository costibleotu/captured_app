README_Codebook Data

"CivicDev Hackathon_7-8 Oct 2017/Data"

Source = unique ID Issuer of public procurement contract (usually public institution)
Target = Winner of public procurement contract (usually business company)
cri_comp = Corruption Risk Index (composite measure associated with the contracts); 0-1 (continuous)
icl.i = Issuer-controlled low corruption risk configuration (measure of clean issuer behavior); numeric (integer)
ich.i = Issuer-controlled high corruption risk configuration (measure of political capture); numeric (integer)
icm.i = Issuer-controlled mixed corruption risk configuration; numeric (integer) 
scl.s = Supplier-controlled low corruption risk configuration (measure of clean business behavior); numeric (integer)
sch.s = Supplier-controlled high corruption risk configuration (measure of business capture); numeric (integer)
scm.s = Supplier-controlled mixed corruption risk configuration; numeric (integer)
anb_name = Name of issuer; string
anb_nuts = Issuer's geographical location (NUTS codes - statistical geographical regions, usually county level - https://en.wikipedia.org/wiki/NUTS_statistical_regions_of_Hungary); geotag (categorical) 
ca_bids = Number of bidders per contract call (measure of competition per call); numeric (integer)
ca_cpv = Nature of the contract (for exact descriptions of codes see file ***CPV-codes-2008***); categorical 
ca_criteria_count = Number of criteria used to determine the winner of a contract call; numeric (integer)
ca_eufund = Whether th contract used EU funds or not; numeric (binary - 0 = no, 1 = yes)
ca_nuts = Contract's geographical location, usually county level; geotag (categorical)
ca_scntr_sc = Whether the winner used subcontractors or not; numeric (binary - 0 = no, 1 = yes)
ca_title = The exact title of the contract call; string
w_consortium = Whether the winner is part of a business consortium; numeric (binary - 0 = no, 1 = yes)
w_name = Name of winner; string
w_nuts = Winner's geographical location; geotag (categorical)
country = country; categorical
ca_date = Exact date when the public procurement contract was signed; DD/MM/YYYY
ca_year = Year when the public procurement contract was signed; YYYY
ca_contract_value = The net value of the contract signed, in EUR; numeric (decimal)
nocft = Whether or not the call for tenders was published in the Official Journal; numeric (binary - 0 = no; 1 = yes)
ca_procedure = The type of precedure used to award the contract; categorical --> needs recoding)
ca_criterion = The criteria used to award the contract; categorical --> needs recoding)
anb_type = The type of issuer; categorical --> needs recoding)
anb_sector = The sector in which the issuer operates; categorical --> needs recoding)
anb_empl_cat = The size of the issuer by number of employees; string --> needs ordinal recoding)




