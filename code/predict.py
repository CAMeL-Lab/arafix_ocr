import os 
import subprocess
import configparser
import pyarabic.araby as araby
import pyarabic.number as number
import argparse

# arabic letters range
begin = int("0600", 16)
end = int("06FF", 16)

def check_parameters():

	incorrect = False

	books = os.listdir("data")
	if parameters["book_name"] not in books:
		print("Book does not exist!")
		incorrect = True

	configs = os.listdir("configs")
	if config_name not in configs:
		print("Config does not exist!")
		incorrect = True

	if parameters["start_page"]!=None:
		if not parameters["start_page"].isdigit():
			print("Start page must be a number!")
			incorrect = True
		if parameters["start_page"]<0:
			print("Start page must be positive!")
			incorrect = True

	if parameters["end_page"]!=None:
		if not parameters["end_page"].isdigit():
			print("End page must be a number!")
			incorrect = True
		if parameters["end_page"]<0:
			print("End page must be positive!")
			incorrect = True

	if parameters["start_page"]!=None and parameters["end_page"]!=None:
		if parameters["end_page"]<parameters["start_page"]:
			print("Start page must be lesser than end page")
			incorrect = True

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

	if args.startpage:
		parameters["start_page"] = int(args.startpage)
	else:
		parameters["start_page"] = int(files[0].split("_")[-1].strip(".txt"))
	if args.endpage:
		parameters["end_page"] = int(args.endpage)
	else:
		parameters["end_page"] = int(files[-1].split("_")[-1].strip(".txt"))

def encode(line):
    new_l = []
    line = araby.strip_shadda(araby.strip_harakat(line)).replace("آ", "ا").replace("إ", "ا").replace("أ", "ا")
    new_line = ""
    for letter in line:
        if (ord(letter) < begin or ord(letter) > end) and (letter!=' '):
            continue
        new_line = new_line + letter
    line = new_line
    
    for w in line.split():
        i = 0
       	for c in w:
            if len(w)==1:
                new_l.append(c)
            elif i == len(w) - 1:
                new_l.append("#" + c)
            elif i == 0:
                new_l.append(c + "#")
            else:
                new_l.append("#" + c + "#")
            i += 1
    return "<s> " + " ".join(new_l) + " </s>"

def write_encoded():

	try:
		os.mkdir("data/" + parameters["book_name"]+ "/" + parameters["book_name"] + "_raw_ocr_encoded/")
	except:
		pass

	for i in range(parameters["start_page"],parameters["end_page"]+1):
		os.system("clear")
		print("Encoding raw ocr for book: ", parameters["book_name"])
		print("Start Page: ", parameters["start_page"])
		print("End Page: ", parameters["end_page"])
		print("Current Page: ", i)
		original_file = open("data/" + parameters["book_name"]+ "/" + parameters["book_name"] +"_raw_ocr/" + "ocr_space_output_" + str(i) + ".txt","r")
		encoded_text = ""
		for line in original_file:
			encoded_text = encoded_text + encode(line) + "\n"

		encoded_file = open("data/" + parameters["book_name"]+ "/" + parameters["book_name"] + "_raw_ocr_encoded/" + "ocr_space_output_encoded_" + str(i) + ".txt","w")
		encoded_file.write(encoded_text)
		original_file.close()
		encoded_file.close()

def decode(l):
	#     l = l.replace("+", "#")
    # there is an unexpected case in disambig results - #A #B#. 
    # we are unsure of whether to split or merge this case, and currently we are spliting
    l = l.replace("# #", "").replace("+ ", "").replace("</s>", "").replace("<s>", "")
    l = l.replace("# #", "").replace("+ ", "").replace("</s>", "").replace("<s>", "")
    l = l.replace("# ", " ").replace(" #", " ")
    return l

def write_decoded():

	spec_prefix = parameters["book_name"] + "_model:" + parameters["model_name"].strip(".lm") + "_map:" + parameters["map_name"].strip(".map")	
	prediction_path = "data/" + parameters["book_name"] + "/" + parameters["book_name"] + "_post_edited/"+ spec_prefix + "/"
	prediction_path_encoded = "data/" + parameters["book_name"] + "/" + parameters["book_name"] + "_post_edited_encoded/"+ spec_prefix + "/"

	try:
		os.mkdir("data/" + parameters["book_name"] +"/" + parameters["book_name"] + "_post_edited/")
	except:
		pass

	try:
		os.mkdir(prediction_path)
	except:
		pass


	for i in range(parameters["start_page"],parameters["end_page"]+1):
		os.system("clear")
		print("Decoding predicted output for book: ", parameters["book_name"])
		print("Start Page: ", parameters["start_page"])
		print("End Page: ", parameters["end_page"])
		print("Current Page: ", i)

		original_file = open(prediction_path_encoded + "predicted_encoded_" + str(i) + ".txt","r")
		decoded_text = decode(original_file.read())
		decoded_file = open(prediction_path + "predicted_" + str(i) + ".txt","w")
		decoded_file.write(decoded_text)
		original_file.close()
		decoded_file.close()

	os.system("clear")
	print("Prediction complete!") 
	print("Results written in: ",prediction_path)

def predict():
	spec_prefix = parameters["book_name"] + "_model:" + parameters["model_name"].strip(".lm") + "_map:" + parameters["map_name"].strip(".map")
	prediction_path = "data/" + parameters["book_name"] + "/" + parameters["book_name"] + "_post_edited_encoded/"+ spec_prefix + "/"
	
	try:
		os.mkdir("data/" + parameters["book_name"] +"/" + parameters["book_name"] + "_post_edited_encoded/")
	except:
		pass
	try:
		os.mkdir(prediction_path)
	except:
		pass

	for i in range(parameters["start_page"],parameters["end_page"]+1):
		os.system("clear")
		print("Predicting output for book: ", parameters["book_name"])
		print("Start Page: ", parameters["start_page"])
		print("End Page: ", parameters["end_page"])
		print("Current Page: ", i)
		raw_ocr_arg = "data/" + parameters["book_name"]+ "/" + parameters["book_name"] + "_raw_ocr_encoded/" + "ocr_space_output_encoded_" + str(i) + ".txt"
		predicted_arg = prediction_path + "predicted_encoded_" + str(i) + ".txt"
		model_arg = "-lm models/" + parameters["model_name"] + " "
		map_arg = "-map mappings/" + parameters["map_name"] + " "
		order_arg = "-order " + parameters["order"] + " "
		text_files = "-text " + raw_ocr_arg + ">" + predicted_arg

		command = "/Users/aizazansari/Downloads/srilm-1.7.3/bin/macosx/disambig " + model_arg + "-keep-unk " + order_arg + map_arg + text_files
		p = subprocess.getstatusoutput(command)


	os.system("clear")


os.chdir("..")

parser = argparse.ArgumentParser()
parser.add_argument("-config", "--config", help="Name of config file", default="default.txt")
parser.add_argument("-bookname", "--bookname", help="Name of book to predict on")
parser.add_argument("-startpage", "--startpage", help="Starting page for prediction of selected book", default=None)
parser.add_argument("-endpage", "--endpage", help="Ending page for prediction of selected book", default = None)

args = parser.parse_args()
config_name = args.config

config = configparser.RawConfigParser()
config.read('configs/' + config_name)    

parameters = dict(config.items('predict'))
parameters["book_name"] = args.bookname

check_parameters()
calculate_bounds()
write_encoded()
predict()
write_decoded()

if parameters["keep_scratch"] == "False":
	os.rmdir("data/" + parameters["book_name"] +"/" + parameters["book_name"] + "_post_edited_encoded/")
	os.rmdir("data/" + parameters["book_name"] +"/" + parameters["book_name"] + "_raw_ocr_encoded/")


