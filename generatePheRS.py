from flask import Flask,render_template,request,url_for, jsonify
from flask_restful import Resource,Api,reqparse
from flask_cors import CORS,cross_origin
import pandas as pd
import sys
import json
import numpy as np
import os
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


app=Flask(__name__)
api=Api(app)

CORS(app)

PheRS_map=pd.read_table('disease_to_phecodes.txt', sep="\t")
icd9_to_phecodes=pd.read_table("icd9_to_phecode.txt", sep="\t",dtype = {'icd9':np.object,'phecode':np.object})


diseases=PheRS_map.MIM.tolist()
icd9_codes=icd9_to_phecodes.icd9.tolist()

icd9s=pd.DataFrame(columns=["ID","icd9"])

diseaseCode=str()

PheRS_Score=0

diseaseMatchingPhecodes=[]

parser = reqparse.RequestParser()
parser.add_argument('codes', type=list)
parser.add_argument('diseaseCode')

class DiseaseCodes(Resource):
        def get(self):
                return {'disease_codes':diseases}

class Icd9Codes(Resource):
	def get(self):
		c=[]
		for code in icd9_codes:
			c.append({"name":code,"value":code})
		return {'icd9_codes':c}

@app.route('/uploadFile', methods=['POST', 'OPTIONS'])
@cross_origin(origin='*', headers='X-Requested-With,content-type')
def uploadFile():
	icd9_codes=[]
	if request.method == 'POST':
		try:
			file=request.files['file[]']
			if file:
				file.save(os.path.join(os.getcwd(),file.filename))	
				df=pd.read_csv(file.filename)
				icd9=df['icd9']
				if icd9.count == 0:
					icd9=df['ICD9']
				with open('icd9_sample_data.txt','wb') as f:
					f.write(("ID"+"\t"+"icd9"+"\n").encode("utf-8"))
					for i in range(len(icd9)):
						f.write(("1"+"\t"+icd9[i]+"\n").encode("utf-8"))
					f.close()
				icd9_s=pd.read_table("icd9_sample_data.txt",sep="\t",dtype={'ID':np.object,'icd9':np.object})
				icd9_codes=icd9_s
		except Exception as ex:
			print(ex)
			pass
	return "file uploaded succesfully!!"


class Score(Resource):
	def get(self):
		sArgs=parser.parse_args()
		codes=sArgs['codes']
		diseaseCode=sArgs['diseaseCode']
		if len(codes) == 0:
			pass
		else:
			codeString=''.join(codes)
			codes=codeString.split(",")
			with open('icd9_sample_data.txt','wb') as f:
				f.write(("ID"+"\t"+"icd9"+"\n").encode("utf-8"))
				for i in range(len(codes)):
					f.write(("1"+"\t"+codes[i]+"\n").encode("utf-8"))
				f.close()

		PheRS_Score=0
		score=0
		icd9s=pd.read_table("icd9_sample_data.txt",sep="\t",dtype={'ID':np.object,'icd9':np.object})
		diseaseMatchingPhecodes=[]
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

		phecode_list=PheRS_map[PheRS_map.MIM==diseaseCode].phecodes.item()
		phecode_list=phecode_list.split(',')

		print(phecode_list)

		for phecode in phecode_list:
			if phecode in phes:
				score=score+phecodes[phecode].item()
				diseaseMatchingPhecodes.append(phecode)
			else:
				pass

		PheRS_Score=score
		return {'score':PheRS_Score,'diseaseMatchingPhecodes':diseaseMatchingPhecodes}

		
@app.route("/")
def index():
	return "Python code to calculate score"

@app.route('/autocomplete_icd9Codes',methods=['GET'])
def autocomplete_icd9Codes():
	icd9Codes=icd9_codes
	c=[]
	for code in icd9_codes:
		c.append({"name":code,"value":code})	
	return jsonify(codes=c)

@app.route("/index")
def home():
	return "Python code to calculate score"



api.add_resource(DiseaseCodes,'/diseaseCodes')
api.add_resource(Icd9Codes,'/icd9Codes')
api.add_resource(Score,'/score')
#api.add_resource(UploadFile,'/uploadFile')



if __name__=='__main__':
	app.run(debug=True)

	
















