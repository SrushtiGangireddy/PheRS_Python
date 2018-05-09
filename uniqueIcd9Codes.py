import pandas as pd
import sys
import json
import numpy as np

ic=open('icd9Codes.txt','r')

icd9s=[]

for i in ic:
	if i in icd9s:
		pass
	else:
		icd9s.append(i)

print(len(icd9s))

