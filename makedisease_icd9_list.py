import pandas as pd
import sys
import json
import numpy as np
import os

PheRS_map=pd.read_table('disease_to_phecodes.txt', sep="\t")
icd9_to_phecodes=pd.read_table("icd9_to_phecode.txt", sep="\t",dtype = {'icd9':np.object,'phecode':np.object})

diseases=PheRS_map.MIM.tolist()
icd9_codes=icd9_to_phecodes.icd9.tolist()

d=open('diseaseIds.txt','w')

for item in diseases:
	d.write("%s\n" %item)

d.close()
ic=open('icd9Codes.txt','w')

for item in icd9_codes:
	ic.write("%s\n" %item)
	
ic.close()
