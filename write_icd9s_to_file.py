import csv
import sys
from io import BytesIO

icd9s=[]

for i in range(len(sys.argv)):
	print(sys.argv[i])

icd9s=sys.argv[1].split("=")[1]

print(icd9s)

icd9s=(str(icd9s)[1:-1]).split(",")

with open('icd9_sample_data.txt','wb') as f:
	f.write(("ID"+"\t"+"icd9"+"\n").encode("utf-8"))
	for i in range(len(icd9s)):
		f.write(("1"+"\t"+icd9s[i]+"\n").encode("utf-8"))

	f.close()



