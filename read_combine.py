import os
import json

"Set InputDir containing the path of extracted files from name_extractor script"
inputDir="output/"

final_data=[]
final_dict_data={}
for each_file in os.listdir(inputDir):
	with open(inputDir+each_file) as d:
		input_data=json.load(d)
	for each_d in input_data:
		final_data.append(each_d)
		final_dict_data[each_d['url']]=each_d['names']

output_file1=open("all_combine_list_name.txt",'w')
json.dump(final_data,output_file1,sort_keys=False,indent=2)
output_file1.close()

output_file2=open("all_final_dict_name.txt",'w')
json.dump(final_dict_data,output_file2,sort_keys=False,indent=2)
output_file2.close()
