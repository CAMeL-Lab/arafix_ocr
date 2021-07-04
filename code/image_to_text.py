import os
from os import listdir
from os.path import isfile, join
import ocrspace
import pyarabic.araby as araby
import pyarabic.number as number
import subprocess
import difflib
import requests
from PyPDF2 import PdfFileWriter, PdfFileReader
import json
import argparse
import configparser
import img2pdf

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
	files = os.listdir("data/" + parameters["book_name"] + "/" + parameters["book_name"] + "_raw_images/")
	
	filtered_files = []

	for file in files:
		if file.endswith(".tif") and file.split("_")[2].startswith("n"):
			filtered_files.append(int(get_page_num(file)))

	files = filtered_files
	files.sort()
	
	if parameters["start_page"]==None:
		parameters["start_page"] = files[0]
	if parameters["end_page"]==None:
		parameters["end_page"] = files[-1]

	if parameters["start_page"]>parameters["end_page"]:
		print("Start page cannot be greater than end page")
		exit(0)

def ocr_space_func(filename, create_pdf, overlay=False, api_key='helloworld', language='eng'):
    """ OCR.space API request with local file.
        Python3.5 - not tested on 2.7
    :param filename: Your file path & name.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """
    if create_pdf=="True":
    	create_pdf = True
    else:
    	create_pdf = False

    payload = {'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               "isCreateSearchablePdf": create_pdf,
               "isSearchablePdfHideTextLayer": create_pdf,
               "isTable":True
               }
    with open(filename, 'rb') as f:
        r = requests.post('https://apipro3.ocr.space/parse/image',
                          files={filename: f},
                          data=payload,
                          )
    return r.content.decode()


def get_page_num(filename):
	started = False
	number = ""
	for i in range(len(filename)-1,-1,-1):
	    
	    if filename[i].isdigit():
	        started = True
	        number = filename[i] + number
	    else:
	        if started == True:
	            break
	return str(int(number))

def convert_book():
	
	raw_path = "data/" + parameters["book_name"] + "/" + parameters["book_name"] + "_raw_images/"
	try:
		os.mkdir(raw_path)
	except:
		pass 

	ocr_path = "data/" + parameters["book_name"] + "/" + parameters["book_name"] + "_raw_ocr/"
	try:
		os.mkdir(ocr_path)
	except:
		pass 

	embed_path = "data/" + parameters["book_name"] + "/" + parameters["book_name"] + "_raw_embed_pdf/"
	try:
		os.mkdir(embed_path)
	except:
		pass 

	raw_json_path = "data/" + parameters["book_name"] + "/" + parameters["book_name"] + "_raw_json/"
	try:
		os.mkdir(raw_json_path)
	except:
		pass

	files = os.listdir(raw_path)
	files.sort()

	converted_files = os.listdir(ocr_path)

	print("-Converting images to text")
	print("Start Page: ", parameters["start_page"])
	print("End Page: ", parameters["end_page"])

	for i,file_name in enumerate(files):
		if not file_name.endswith(".tif") or not file.split("_")[2].startswith("n"):
			continue

		cur_page = int(get_page_num(file_name))
		if cur_page<parameters["start_page"]:
			continue
		if cur_page>parameters["end_page"]:
			print("\n")
			print("Results written in: ", ocr_path)
			return

		print("Current Page: ", cur_page, end = "\r")

		if parameters["skip_converted"]=="True":
			if "ocr_space_output_" + get_page_num(file_name) + ".txt" in converted_files:
				continue

		# file_name_pdf = file_name.strip(".tif")+".pdf"
		# with open(raw_path+file_name_pdf,"wb") as f:
		# 	f.write(img2pdf.convert(raw_path+file_name))

		page_json = ocr_space_func(filename= raw_path+file_name, language='Ara', api_key = parameters["api_key"], create_pdf = parameters["create_pdf"])
		page_text = json.loads(page_json)["ParsedResults"][0]["ParsedText"]
		output_file = open(ocr_path  + "ocr_space_output_" + get_page_num(file_name) + ".txt", "w", encoding = "utf8")
		output_file.write(page_text)
		output_file.close()

		output_json = open(raw_json_path + "raw_json_" + get_page_num(file_name) + ".txt", "w", encoding = "utf8")
		output_json.write(page_json)
		output_json.close()

		if parameters["create_pdf"] == "True":
			page_url = json.loads(page_json)["SearchablePDFURL"]
			r = requests.get(page_url, allow_redirects=True)
			open(embed_path + "ocr_space_output_embed_pdf" + get_page_num(file_name) + ".pdf", 'wb').write(r.content)


	print("\n")
	print("Results written in: ", ocr_path)

	
os.chdir("..")

parser = argparse.ArgumentParser()
parser.add_argument("-config", "--config", help="Name of config file")
parser.add_argument("-bookname", "--bookname", help="Name of book to ocr on")
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
parameters = dict(config.items('image_to_text'))


print()
print("---IMAGE TO TEXT MODULE STARTED---\n")

check_parameters()

calculate_bounds()

convert_book()

print()
print("---IMAGE TO TEXT MODULE COMPLETED---\n")