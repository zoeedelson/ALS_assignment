## DOCUMENTATION:
## This script runs on Python 3.7.4, although likely runs successfully on other 
## versions. Download Python3 and pip3 install pandas and numpy libraries. 
## Place script in the same folder as cons.csv, cons_email.csv, and 
## cons_email_chapter_subscription.csv. On the command line, run "python3 ALS_assignment.py"
## from the folder that holds all four mentioned documents (CSVs and Python file).

import pandas as pd
import numpy as np

def ALS_Exercise():
    #import CSVs into DataFrames
    a = pd.read_csv('cons.csv')
    b = pd.read_csv('cons_email.csv')
    c = pd.read_csv('cons_email_chapter_subscription.csv')

    #selecting rows of the primary email address
    b_primary = b.loc[(b['is_primary'] ==1)] 

    #merging a and b along unique consituent id
    a_b_merge = a.merge(b_primary, how='left', on='cons_id')   

    #select rows where chapter_id is 1
    c_interested = c.loc[(c['chapter_id'] ==1)]

    #merging a and b with c along unique constitutent email id
    a_b_c_merge = a_b_merge.merge(c_interested, how='left', on='cons_email_id')

    a_b_c = a_b_c_merge[['email','isunsub','create_dt_x','modified_dt_x']]

    #change 'isunsub' to be boolean, ie change NaN to 0.
    a_b_c = a_b_c.assign(isunsub=lambda a_b_c: a_b_c['isunsub'].fillna(value=0))

    #rename columns
    a_b_c_renamed = a_b_c.rename(columns={'isunsub':'is_unsub','create_dt_x':'created_dt','modified_dt_x':'updated_dt'})

    a_b_c_renamed.to_csv('people.csv', header=True, index=False)

    #counted unique dates (without timestamp)
    unique_dates, counts = np.unique(a_b_c_renamed['created_dt'].map(lambda dt:dt.split(' ')[1]),return_counts=True) 
    acquisition_table = pd.DataFrame({'acquisition_date':unique_dates,'acquisitions':counts})

    acquisition_table.to_csv('acquisition_facts.csv', index=False)

ALS_Exercise()