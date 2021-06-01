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


def ocr_space_func(filename, overlay=False, api_key='helloworld', language='eng'):
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

    payload = {'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               }
    with open(filename, 'rb') as f:
        r = requests.post('https://apipro3.ocr.space/parse/image',
                          files={filename: f},
                          data=payload,
                          )
    return r.content.decode()

def convert_book()
	
	raw_path = "data/" + parameters["book_name"] + "/" + parameters["book_name"] + "_scanned/"
	try:
		os.mkdir(raw_path)
	except:
		pass 

	ocr_path = "data/" + parameters["book_name"] + "/" + parameters["book_name"] + "_raw_ocr/"
	try:
		os.mkdir(raw_path)
	except:
		pass 


	for i in range(parameters["start_page"], parameters["end_page"]):
	    os.system("clear")
	    print("Converting images to text")
	    print("Start Page: ", parameters["start_page"])
		print("End Page: ", parameters["end_page"])
		print("Current Page: ", i)
	    page_json = ocr_space_func(filename= raw_path + parameters["file_prefix"] + str(i) + ".tiff", language='Ara', api_key = "OCRP7509898A")
	    page_text = json.loads(page_json)["ParsedResults"][0]["ParsedText"]
	    output_file = open(ocr_path  + "ocr_space_output_" + str(i) + ".txt", "w", encoding = "utf8")
	    output_file.write(page_text)
	    output_file.close()

	os.system("clear")
	print("Image to text conversion completed!")

os.chdir("..")

parser = argparse.ArgumentParser()
parser.add_argument("-config", "--config", help="Name of config file")
args = parser.parse_args()
config_name = args.config

config = configparser.RawConfigParser()
config.read('config_files/' + config_name)    
parameters = dict(config.items('image_to_text'))