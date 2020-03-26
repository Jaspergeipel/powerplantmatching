# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 11:31:48 2020

@author: geipel
"""

import pandas as pd
import powerplantmatching as pm
wepp        = pm.data.WEPP()
geo         = pm.data.GEO()
entsoe      = pm.data.ENTSOE()
carma       = pm.data.CARMA()
gpd         = pm.data.GPD()
opsd        = pm.data.OPSD()
df1         = pm.powerplants(reduced = True, from_url=False, update=True)

capacity_per_fuel_matched=round(df1.groupby('Fueltype').Capacity.sum()/1000,0)
#df1=pm.heuristics.fill_missing_commyears(df1)
#df1=pm.heuristics.fill_missing_decommyears(df1)
#df1=pm.heuristics.remove_oversea_areas(df1)
df1=pm.heuristics.rescale_capacities_to_country_totals(df1)
#df=pm.powerplants(reduced = True, from_url=False, update=True)
#pm.collection.matched_data(update=True, use_saved_aggregation=False, use_saved_matches=False)
print(round(pm.data.CARMA().groupby('Fueltype').Capacity.sum()/1000,0))


#xxsum['percentage']=xxsum/xxsum.groupby(['Country', 'Fueltype'])['Capacity'].sum()
#xxsum['percentage']=xxsum['Capacity']/xxsum.groupby(['Country', 'Fueltype'])['Capacity'].transform('sum')

#pm.gather_fueltype_info(wepp)
#pm.gather_fueltype_info(opsd)
#chp=wepp.query('Set == "CHP"')


#dfw=pm.data.WEPP()

#fig, ax = pm.plot.powerplant_map(df)
#pm.plot.fueltype_stats(df)
#fig,  ax = pm.plot.fueltype_and_country_totals_bar(df)
#pm.plot.fueltype_totals_bar(df)
#pm.plot.country_totals_hbar(df)
#pm.plot.factor_comparison(df)

