import os
import subprocess
import pandas as pd
import csv
import camel_tools.utils.charsets
import pyarabic.araby as araby
import pyarabic.number as number
import difflib
import argparse
import configparser
import pyarabic.araby as araby
import pyarabic.number as number
import shutil
import re


arabic_punctuation = [c for c in camel_tools.utils.charsets.UNICODE_PUNCT_CHARSET if 1536 <= ord(c) <= 1791]

def check_parameters():

	parameters["book_name"] = args.bookname
	parameters["start_page"] = args.startpage
	parameters["end_page"] = args.endpage


	if parameters["start_page"]=="None":
		parameters["start_page"] = None

	if parameters["end_page"]=="None":
		parameters["end_page"] = None

	incorrect = False

	books = os.listdir("data")
	if parameters["book_name"] not in books:
		print("Book does not exist!")
		incorrect = True

	if parameters["start_page"]!=None:
		if not parameters["start_page"].isdigit():
			print("Start page must be a positive number!")
			incorrect = True
		else:
			parameters["start_page"] = int(parameters["start_page"])
	

	if parameters["end_page"]!=None:
		if not parameters["end_page"].isdigit():
			print("End page must be positive a number!")
			incorrect = True
		else:
			parameters["end_page"] = int(parameters["end_page"])


	if incorrect:
		exit(0)

def calculate_bounds():
	spec_prefix = parameters["book_name"] + "_model_" + parameters["model_name"][:-3] + "_map_" + parameters["map_name"][:-4]
	files = os.listdir("data/" + parameters["book_name"] + "/" + parameters["book_name"] + "_post_edited/" + spec_prefix + "/")
	new_files = []
	for file in files:
		if file.endswith(".txt"):
			new_files.append(int(file.split("_")[-1].strip(".txt")))
	new_files.sort()
	files = new_files

	if parameters["start_page"]==None:
		parameters["start_page"] = files[0]
	if parameters["end_page"]==None:
		parameters["end_page"] = files[-1]

	if parameters["start_page"]>parameters["end_page"]:
		print("Start page cannot be greater than end page")
		exit(0)

def parseOssamaBasic(file_name):
    df = pd.read_csv(file_name, sep = "\t", header = None, engine="python", quoting=csv.QUOTE_NONE)
    df.columns = ["one", 'op', "two", "extra"]
    df["operation"] = df.apply(operationName, axis = 1)
    return df[["operation", "one", "two"]]

def operationName(row):
    if row["op"] == "=":
        return "OK"
    
    elif row["op"] == "|":
        return "SUB"
    
    elif row["op"] == "<":
        return "INS"
    
    else:
        return "DEL"


# Basic alignment - Ossama's code
def alignFilesBasic(start_page, end_page, OneEncodePrefix, OneEncodeFolder, TwoEncodePrefix, TwoEncodeFolder, saveAlignmentAs, alignerLocation, results_prefix):
    for i in range(start_page, end_page + 1):

        OneName = OneEncodePrefix + str(i) + ".txt"
        TwoName = TwoEncodePrefix + str(i) + ".txt"

        #"python align_text.py -r ocr_tokenized.txt -c rafed_tokenized.txt -m basic -o sample/sample.ar"
        command = "python3 " + alignerLocation + " -s " + OneEncodeFolder + OneName + " -t " + TwoEncodeFolder + TwoName 
        command +=  " -m basic -o " + saveAlignmentAs + results_prefix + str(i) 

        p = subprocess.getstatusoutput(command)

def strip_text(raw_text):
	no_punc_text = "".join([c for c in raw_text.replace("\n", " ") if (c not in arabic_punctuation and 1536 <= ord(c) <= 1791) or c == " " ])
	no_punc_text = re.sub(" +", " ", no_punc_text)

	no_punc_text = araby.strip_shadda(araby.strip_harakat(no_punc_text)).replace("آ", "ا").replace("إ", "ا").replace("أ", "ا")

	return no_punc_text


def strip_files():
	spec_prefix = parameters["book_name"] + "_model_" + parameters["model_name"][:-3] + "_map_" + parameters["map_name"][:-4]	

	for i in range(parameters["start_page"],parameters["end_page"]+1):

		ground_file = open("data/"+parameters["book_name"]+"/"+parameters["book_name"]+"_ground_truth/"+"ground_truth_"+str(i)+".txt","r")
		ocr_file = open("data/"+parameters["book_name"]+"/"+parameters["book_name"]+"_raw_ocr/"+"ocr_space_output_"+str(i)+".txt","r")
		predicted_file = open("data/"+parameters["book_name"]+"/"+parameters["book_name"]+"_post_edited/"+spec_prefix+"/predicted_"+str(i)+".txt","r")

		ground_file_stripped = open("data/"+parameters["book_name"]+"/"+parameters["book_name"]+"_ground_truth/"+"ground_truth_stripped_"+str(i)+".txt","w")
		ocr_file_stripped = open("data/"+parameters["book_name"]+"/"+parameters["book_name"]+"_raw_ocr/"+"ocr_space_output_stripped_"+str(i)+".txt","w")
		predicted_file_stripped = open("data/"+parameters["book_name"]+"/"+parameters["book_name"]+"_post_edited/"+spec_prefix+"/predicted_stripped_"+str(i)+".txt","w")

		ground_file_stripped.write(strip_text(ground_file.read()))
		ocr_file_stripped.write(strip_text(ocr_file.read()))
		predicted_file_stripped.write(strip_text(predicted_file.read()))

		ground_file.close()
		ocr_file.close()
		predicted_file.close()

		ground_file_stripped.close()
		ocr_file_stripped.close()
		predicted_file_stripped.close()




def align_ground_ocr():

	book_name = parameters["book_name"]
	sub_folder_one = book_name + "_ground_truth"
	sub_folder_two = book_name + "_raw_ocr"

	save_alignment_as = book_name + "_" + sub_folder_one.replace(book_name + "_", "") + "_with_" + sub_folder_two.replace(book_name + "_", "") + "/"
	

	save_alignment_as = "data/" + book_name + "/" + book_name + "_alignment/" + save_alignment_as
	file_extension = ".txt"

	start_page = parameters["start_page"]
	end_page = parameters["end_page"]

	try:
		os.mkdir("data/" + book_name + "/" + book_name + "_alignment/")

	except:
		pass

	try:
	    os.mkdir(save_alignment_as)

	except:
	    pass

	alignerLocation = "code/ced_word_alignment/align_text.py"

	truth_path = "data/" + book_name + "/" + sub_folder_one + "/"
	truth_prefix = 'ground_truth_stripped_' 

	hypothesis_path = "data/" + book_name + "/" + sub_folder_two + "/"
	hypothesis_prefix = "ocr_space_output_stripped_"

	results_prefix = "ground_raw_ocr_"

	print("-Aligning Ground Truth with Raw OCR")
	alignFilesBasic(parameters["start_page"], parameters["end_page"], truth_prefix, truth_path, hypothesis_prefix, hypothesis_path, save_alignment_as, alignerLocation, results_prefix)
	calculate_stats(start_page, end_page, save_alignment_as, results_prefix)

	if parameters["keep_scratch"]!="True":
		shutil.rmtree(save_alignment_as)


def align_ground_predicted():

	spec_prefix = parameters["book_name"] + "_model_" + parameters["model_name"][:-3] + "_map_" + parameters["map_name"][:-4]	

	book_name = parameters["book_name"]
	sub_folder_one = book_name + "_ground_truth"
	sub_folder_two = book_name + "_post_edited/" + spec_prefix

	save_alignment_as = book_name + "_" + sub_folder_one.replace(book_name + "_", "") + "_with_post_edited_" + spec_prefix.replace(book_name + "_", "") + "/"
	

	save_alignment_as = "data/" + book_name + "/" + book_name + "_alignment/" + save_alignment_as

	file_extension = ".txt"

	start_page = parameters["start_page"]
	end_page = parameters["end_page"]

	try:
		os.mkdir("data/" + book_name + "/" + book_name + "_alignment/")

	except:
		pass

	try:
	    os.mkdir(save_alignment_as)

	except:
	    pass

	alignerLocation = "code/ced_word_alignment/align_text.py"

	truth_path = "data/" + book_name + "/" + sub_folder_one + "/"
	truth_prefix = 'ground_truth_stripped_' 

	hypothesis_path = "data/" + book_name + "/" + sub_folder_two + "/"
	hypothesis_prefix = "predicted_stripped_"

	results_prefix = "ground_predicted_"

	print("-Aligning Ground Truth with Predicted")
	alignFilesBasic(parameters["start_page"], parameters["end_page"], truth_prefix, truth_path, hypothesis_prefix, hypothesis_path, save_alignment_as, alignerLocation, results_prefix)
	calculate_stats(start_page, end_page, save_alignment_as, results_prefix)

	if parameters["keep_scratch"]!="True":
		shutil.rmtree(save_alignment_as)

def calculate_stats(start_page, end_page, save_alignment_as, results_prefix):

	summary_df = pd.DataFrame()
	for i in range(start_page, end_page+1):
		try:
			df = parseOssamaBasic(save_alignment_as + results_prefix + str(i) + ".basic")
			df.to_csv(save_alignment_as + results_prefix + str(i) + ".csv")

			my_dict = dict(df["operation"].value_counts())

			if "DEL" not in my_dict:
				my_dict["DEL"] = 0

			if "INS" not in my_dict:
				my_dict["INS"] = 0

			if "SUB" not in my_dict:
				my_dict["SUB"] = 0

			my_dict["page_num"] = i

			summary_df = summary_df.append(my_dict, ignore_index = True)
		except Exception as e:
			print(e)

	## WER CALCULATION, CHANGE IF NEEDED
	# WER = (del + ins + sub) / (ok + sub + del)
	temp_dict = summary_df.sum()
	del_, ins, ok, sub = temp_dict["DEL"], temp_dict["INS"], temp_dict["OK"], temp_dict["SUB"]
	temp_dict["WER"] = round((del_ + ins + sub) / (ok + sub + del_), 5)
	print("WER is ",temp_dict["WER"])
	print()
	# write to file
	summary_df.to_csv(save_alignment_as + results_prefix + "all.csv")


def remove_scratch():

	spec_prefix = parameters["book_name"] + "_model_" + parameters["model_name"][:-3] + "_map_" + parameters["map_name"][:-4]	

	if parameters["keep_scratch"]=="True":
		return

	for i in range(parameters["start_page"], parameters["end_page"]+1):
		os.remove("data/"+parameters["book_name"]+"/"+parameters["book_name"]+"_ground_truth/"+"ground_truth_stripped_"+str(i)+".txt")
		os.remove("data/"+parameters["book_name"]+"/"+parameters["book_name"]+"_raw_ocr/"+"ocr_space_output_stripped_"+str(i)+".txt")
		os.remove("data/"+parameters["book_name"]+"/"+parameters["book_name"]+"_post_edited/"+spec_prefix+"/predicted_stripped_"+str(i)+".txt")




os.chdir("..")

parser = argparse.ArgumentParser()
parser.add_argument("-config", "--config", help="Name of config file", default="default.txt")
parser.add_argument("-bookname", "--bookname", help="Name of book to predict on")
parser.add_argument("-startpage", "--startpage", help="Starting page for prediction of selected book", default=None)
parser.add_argument("-endpage", "--endpage", help="Ending page for prediction of selected book", default = None)

args = parser.parse_args()
config_name = args.config
configs = os.listdir("configs")

if config_name not in configs:
	print("Config does not exist!")
	exit(0)

config = configparser.RawConfigParser()
config.read('configs/' + config_name)    

parameters = dict(config.items('evaluate'))

print()
print("---EVALUATION MODULE STARTED---\n")

check_parameters()
calculate_bounds()


strip_files()
align_ground_ocr()
align_ground_predicted()
remove_scratch()

print()
print("---EVALUATION MODULE ENDED---\n")