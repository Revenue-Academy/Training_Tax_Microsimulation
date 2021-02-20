
"""
app000.py illustrates use of pitaxcalc-demo release 2.0.0 (India version).
USAGE: python app000.py > app000.res
CHECK: Use your favorite Windows diff utility to confirm that app0.res is
       the same as the app0.out file that is in the repository.
"""
from taxcalc import *

# create Records object containing pit.csv and pit_weights.csv input data
recs = Records()

assert isinstance(recs, Records)
assert recs.data_year == 2020
assert recs.current_year == 2020

# create GSTRecords object containing gst.csv and gst_weights.csv input data
grecs = GSTRecords(data='gst_cmie_august_2020.csv', weights='gst_weights_cmie_august_2020.csv')

assert isinstance(grecs, GSTRecords)
assert grecs.data_year == 2020
assert grecs.current_year == 2020

# create CorpRecords object containing cit.csv and cit_weights.csv input data
crecs = CorpRecords()

assert isinstance(crecs, CorpRecords)
assert crecs.data_year == 2020
assert crecs.current_year == 2020

# create Policy object containing current-law policy
pol = Policy()

assert isinstance(pol, Policy)
assert pol.current_year == 2020

# specify Calculator object for current-law policy
calc1 = Calculator(policy=pol, records=recs, corprecords=crecs,
                   gstrecords=grecs, verbose=False)

# NOTE: calc1 now contains a PRIVATE COPY of pol and a PRIVATE COPY of recs,
#       so we can continue to use pol and recs in this script without any
#       concern about side effects from Calculator method calls on calc1.

assert isinstance(calc1, Calculator)
assert calc1.current_year == 2020

# Produce DataFrame of results using cross-section
calc1.calc_all()
id_gst = calc1.garray('ID_NO')
#gst_cereal = calc1.garray('gst_cereal')
total_consumption_food = calc1.garray('total_consumption_food')
total_consumption_non_food = calc1.garray('total_consumption_non_food')
total_consumption = total_consumption_food + total_consumption_non_food
gst_total = calc1.garray('gst')
gst_total_food = calc1.garray('gst_food')
gst_total_non_food = calc1.garray('gst_non_food')
wgt_gst = calc1.garray('WEIGHT0')
weighted_gst_food = calc1.weighted_garray('gst_food')
weighted_gst_non_food = calc1.weighted_garray('gst_non_food')
weighted_gst = calc1.weighted_garray('gst')
weighted_consumption_food = calc1.weighted_garray('total_consumption_food')
weighted_consumption_non_food = calc1.weighted_garray('total_consumption_non_food')
weighted_consumption_education = calc1.weighted_garray('total_consumption_education')
weighted_consumption_health = calc1.weighted_garray('total_consumption_health')
weighted_consumption_all = (weighted_consumption_food + weighted_consumption_non_food +
                            weighted_consumption_education + weighted_consumption_health)
total_consumption_food_all = calc1.weighted_total_garray('total_consumption_food')
total_consumption_non_food_all = calc1.weighted_total_garray('total_consumption_non_food')
total_consumption_education_all = calc1.weighted_total_garray('total_consumption_education')
total_consumption_health_all = calc1.weighted_total_garray('total_consumption_health')
total_consumption_all = ((total_consumption_food_all+total_consumption_non_food_all+
                          total_consumption_education_all + total_consumption_health_all) / 10**7)
#total_consumption_all1 = calc1.weighted_total_garray('total_consumption') / 10**7
total_gst = calc1.weighted_total_garray('gst') / 10**7
total_weight = calc1.garray('WEIGHT0').sum() / 10**7
print(f'Total Consumption in Economy - 2020 (Rupees Crores): {total_consumption_all:,.0f}')
#print(f'Total Consumption in Economy - 2020 (Rupees Crores): {total_consumption_all1:,.0f}')
print(f'Total GST Collection - 2020 (Rupees Crores): {total_gst:,.0f}')
print(f'Total Households - 2020 (Crores): {total_weight:,.0f}')
results = pd.DataFrame({'GST_ID_NO': id_gst,
                        'Weight': wgt_gst,
                        'Weighted Consumption Food': weighted_consumption_food,
                        'Weighted Consumption Non-Food': weighted_consumption_non_food,                        
                        'Weighted Total Consumption': weighted_consumption_all,
                        'Weighted GST_Food': weighted_gst_food,
                        'Weighted GST_Non_Food': weighted_gst_non_food,                         
                        'Weighted GST': weighted_gst})
results.to_csv('app000-dump-gst-august-2000.csv', index=False,
               float_format='%.0f')
