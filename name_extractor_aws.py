	from ast import literal_eval
import os
import json
import sys
import re
from sets import Set
import time 
import nltk
from nltk import pos_tag, ne_chunk


"""
Keywords: contains list of all the business type that we want to use for processing.
"""

keywords=["spa","center"]

"""
Input Directory containing all files
"""
inputDir=""

"""
OutputDir
"""
outputDir="./output/"

def getPos(toks,nes):
	start=0
	nes_pos={}
	i=0
	for each_tok in toks:
		if start == len(nes):
			break
		if each_tok==nes[start]:
			nes_pos[nes[start]+str(start)]=i
			start+=1
		i+=1
	return nes_pos

def getName(text_string,type1):
	toks = text_string.split()
	words=[]
	i=0
	for each_word in toks:		
		if each_word.lower()==type1:
			words.append(int(i))
		i+=1
	pos = pos_tag(toks)	
	nes_back={}	
	for each_pos in pos:
		if each_pos[0].lower() != type1 and ( each_pos[1]=="NN" or each_pos[1]=="NNP" or each_pos[1]=="JJ"):
			nes_back[each_pos[0]]=1	
	ans=[]
	for each_type in words:
		i=each_type			
		while i>0 and toks[i-1] in nes_back:
			ans.append(toks[i-1])
			i=i-1
		if len(ans) >0:
			break;
	if len(ans)>0:
		ans=ans[::-1]
		ans=" ".join(ans)
		return ans+' '+type1
	else:
		return ""

def extractName(text,p,type1,names):	
	end=-1	
	m=p.search(text.lower())
	if m!=None:
		flag=0
		mid=m.span()[0]+len(type1)		
		result=getName(text[:mid],type1)
		names.add(result)
		m=p.search(text.lower(),mid)
		if m!=None:
			extractName(text[mid],p,type1,names)
	return names	

def processFile(input_file_name,keywords,finalNamesData):
	input_data=""
	temp={}
	with open(input_file_name,'r') as data_file:			
		for each_line in data_file:
			j = literal_eval(each_line)
			input_data=json.loads(j[1])			
			each_a=input_data['readability_text'][0]
			temp["input"]=each_a
			temp["url"]=input_data['url']
			names=Set()
			for each_keyword in keywords:
				p = re.compile(r'\b%s\b' % each_keyword.lower(), re.I)
				m=p.search(each_a.lower())
				if m!=None:
					extractName(each_a,p,each_keyword,names)			
			temp["names"]=list(names)		
			finalNamesData.append(temp)			
	return finalNamesData		




if __name__ == '__main__':
	total=len(os.listdir(inputDir))	
	count=1
	if len(argv) <2:
		print "Pass Input Dir; Usage: python name_extractor_aws.py <input_dir_path>"
		return 
	inputDir=argv[1]	
	for file in os.listdir(inputDir):				
		finalNamesData=[]
		finalNamesData=processFile(inputDir+'/'+file,keywords,finalNamesData)		
		outputFile=open(outputDir+file+"_extraction_out.txt","w")
		json.dump(finalNamesData,outputFile,sort_keys=False,indent=2)	
		outputFile.close()
		print "Processed: ",count,"/",total
		count+=1	
