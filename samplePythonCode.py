import pandas as pd
import sys
import numpy as np
import os

PheRS_map=pd.read_table('disease_to_phecodes.txt', sep="\t")
icd9_to_phecodes=pd.read_table("icd9_to_phecode.txt", sep="\t",dtype = {'icd9':np.object,'phecode':np.object})

diseases=PheRS_map.MIM.tolist()
icd9_codes=icd9_to_phecodes.icd9.tolist()

icd9s=pd.read_table("icd9_sample_data.txt",sep="\t",dtype={'ID':np.int64,'icd9':np.object})

phecodes=pd.merge(icd9s,icd9_to_phecodes,on="icd9")
phecodes=phecodes[['ID','phecode']].copy() 
phecodes=phecodes.drop_duplicates('phecode')
phecodes["value"]=1
phecodes=phecodes.pivot(index='ID',columns='phecode',values='value')

weights=pd.read_table('weights_VUMC_discovery.txt', sep="\t",dtype={'phecode':np.object,'case_count':np.int64,'prev':np.float64,'w':np.float64})
weights=weights.rename(index=weights['phecode'])

phes=phecodes.columns.tolist()

for i in range(len(phes)):
	phe=phes[i]
	try:
		phecodes[[phe]]=phecodes[[phe]]*weights[weights.phecode==phe].w[0]
	except IndexError:
		phecodes[[phe]]=phecodes[[phe]]*0

phecode_list=PheRS_map[PheRS_map.MIM=="OMIM_600376"].phecodes.item()
phecode_list=phecode_list.split(',')

PheRS_Score=0
score=0

for phecode in phecode_list:
	if phecode in phes:
		score=score+phecodes[phecode].item()
	else:
		pass
PheRS_Score=score
print(PheRS_Score)

