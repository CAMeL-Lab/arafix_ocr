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


	models = os.listdir("models")
	if parameters["model_name"] not in models:
		print("Model does not exist!")
		incorrect = True

	mappings = os.listdir("mappings")
	if parameters["map_name"] not in mappings:
		print("Mapping does not exist!")
		incorrect = True

	if incorrect:
		exit(0)

def calculate_bounds():
	files = os.listdir("data/" + parameters["book_name"] + "/" + parameters["book_name"] + "_raw_ocr/")
	files.sort()
	files = files[1:]

	if parameters["start_page"]==None:
		parameters["start_page"] = int(files[0].split("_")[-1].strip(".txt"))
	if parameters["end_page"]==None:
		parameters["end_page"] = int(files[-1].split("_")[-1].strip(".txt"))

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
        command = "python3 " + alignerLocation + " -r " + OneEncodeFolder + OneName + " -c " + TwoEncodeFolder + TwoName 
        command +=  " -m basic -o " + saveAlignmentAs + results_prefix + str(i) 


        p = subprocess.getstatusoutput(command)


def align_ground_predicted():

	book_name = parameters["book_name"]
	sub_folder_one = book_name + "_ground_truth"
	sub_folder_two = parameters["book_name"] + "_model:" + parameters["model_name"].strip(".lm") + "_map:" + parameters["map_name"].strip(".map")

	save_alignment_as = book_name + "_" + sub_folder_one.replace(book_name + "_", "") + "_with_" + sub_folder_two.replace(book_name + "_", "") + "/"
	
	save_alignment_as = "data/" + book_name + "/aligment/" + save_alignment_as
	file_extension = ".txt"

	start_page = parameters["start_page"]
	end_page = parameters["end_page"]

	try:
		os.mkdir("data/" + book_name + "alignment/")

	except:
		pass

	try:
	    os.mkdir(save_alignment_as)

	except:
	    pass

	alignerLocation = "code/ced_word_alignment/align_text.py"

	truth_path = "data/" + book_name + "/" + sub_folder_one + "/"
	truth_prefix = 'ground_truth_' 

	hypothesis_path = "data/" + book_name + "/" + book_name + "_post_edited/" + sub_folder_two + "/"
	hypothesis_prefix = "predicted_"

	results_prefix = "ground_predicted_"

	alignFilesBasic(parameters["start_page"], parameters["end_page"], truth_prefix, truth_path, hypothesis_prefix, hypothesis_path, save_alignment_as, alignerLocation, results_prefix)


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

check_parameters()
calculate_bounds()

align_ground_predicted()