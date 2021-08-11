import os 
import subprocess
import configparser
import pyarabic.araby as araby
import pyarabic.number as number
import argparse
import shutil

# arabic letters range
begin = int("0600", 16)
end = int("06FF", 16)

#check if arguments valid
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

#if start and end not defined, assign them lowest and highest possible values
def calculate_bounds():
	files = os.listdir("data/" + parameters["book_name"] + "/" + parameters["book_name"] + "_raw_ocr/")
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

#function to encode text
def encode(line):
    new_l = []
    
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
    return ("<s> " + " ".join(new_l) + " </s>")

#function to convert raw ocr to raw ocr encoded
def write_encoded():

	try:
		os.mkdir("data/" + parameters["book_name"]+ "/" + parameters["book_name"] + "_raw_ocr_encoded/")
	except:
		pass

	# print("-Encoding raw ocr")
	# print("Start Page: ", parameters["start_page"])
	# print("End Page: ", parameters["end_page"])

	for i in range(parameters["start_page"],parameters["end_page"]+1):

		# print("Current Page: ", i, end = "\r")
		original_file = open("data/" + parameters["book_name"]+ "/" + parameters["book_name"] +"_raw_ocr/" + "ocr_space_output_" + str(i) + ".txt","r", encoding="utf8")
		encoded_text = ""
		for line in original_file:
			encoded_text = encoded_text + encode(line) + "\n"

		encoded_file = open("data/" + parameters["book_name"]+ "/" + parameters["book_name"] + "_raw_ocr_encoded/" + "ocr_space_output_encoded_" + str(i) + ".txt","w", encoding="utf8")
		encoded_file.write(encoded_text)
		original_file.close()
		encoded_file.close()

	# print("\n")

#function to decode text
def decode(l):
	#     l = l.replace("+", "#")
    # there is an unexpected case in disambig results - #A #B#. 
    # we are unsure of whether to split or merge this case, and currently we are spliting
    l = l.replace("# #", "").replace("+ ", "").replace("</s>", "").replace("<s>", "")
    l = l.replace("# #", "").replace("+ ", "").replace("</s>", "").replace("<s>", "")
    l = l.replace("# ", " ").replace(" #", " ")
    return l

#function to convert predicted encoded to predicted text
def write_decoded():

	spec_prefix = parameters["book_name"] + "_model_" + parameters["model_name"][:-3] + "_map_" + parameters["map_name"][:-4]	
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

	# print("-Decoding predicted output")
	# print("Start Page: ", parameters["start_page"])
	# print("End Page: ", parameters["end_page"])

	for i in range(parameters["start_page"],parameters["end_page"]+1):

		# print("Current Page: ", i, end = "\r")

		original_file = open(prediction_path_encoded + "predicted_encoded_" + str(i) + ".txt","r", encoding="utf8")
		decoded_text = decode(original_file.read())
		decoded_file = open(prediction_path + "predicted_" + str(i) + ".txt","w", encoding="utf8")
		decoded_file.write(decoded_text)
		original_file.close()
		decoded_file.close()

	# print("\n")
	print("Results written in: ",prediction_path)

#function to predict on raw ocr encoded and get predicte encoded
def predict():
	spec_prefix = parameters["book_name"] + "_model_" + parameters["model_name"][:-3] + "_map_" + parameters["map_name"][:-4]		
	prediction_path = "data/" + parameters["book_name"] + "/" + parameters["book_name"] + "_post_edited_encoded/"+ spec_prefix + "/"
	
	try:
		os.mkdir("data/" + parameters["book_name"] +"/" + parameters["book_name"] + "_post_edited_encoded/")
	except:
		pass
	try:
		os.mkdir(prediction_path)
	except:
		pass

	print("-Predicting output")
	print("Start Page: ", parameters["start_page"])
	print("End Page: ", parameters["end_page"])

	if os.path.isdir("data/" + parameters["book_name"] + "/" + parameters["book_name"] + "_post_edited/") and os.path.isdir("data/" + parameters["book_name"] + "/" + parameters["book_name"] + "_post_edited/"+ spec_prefix + "/"):
		already_predicted = os.listdir("data/" + parameters["book_name"] + "/" + parameters["book_name"] + "_post_edited/"+ spec_prefix + "/")
	else:
		already_predicted = []

	for i in range(parameters["start_page"],parameters["end_page"]+1):

		print("Current Page: ", i, end = "\r")
		raw_ocr_arg = "data/" + parameters["book_name"]+ "/" + parameters["book_name"] + "_raw_ocr_encoded/" + "ocr_space_output_encoded_" + str(i) + ".txt"
		predicted_arg = prediction_path + "predicted_encoded_" + str(i) + ".txt"
		model_arg = "-lm models/" + parameters["model_name"] + " "
		map_arg = "-map mappings/" + parameters["map_name"] + " "
		order_arg = "-order " + parameters["order"] + " "
		text_files = "-text " + raw_ocr_arg + ">" + predicted_arg

		command = "code/srilm-1.7.3/bin/macosx/disambig " + model_arg + "-keep-unk " + order_arg + map_arg + text_files
		
		if "predicted_" + str(i) + ".txt" in already_predicted and parameters["skip_converted"]=="True":
			continue
		else:
			p = subprocess.getstatusoutput(command)

	print("\n")


os.chdir("..")

#add arguments to python file
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

parameters = dict(config.items('predict'))


print()
print("---PREDICTION MODULE STARTED---\n")

check_parameters()
calculate_bounds()
write_encoded()
predict()
write_decoded()


#delete scratch files if needed
if parameters["keep_scratch"] == "False":
	spec_prefix = parameters["book_name"] + "_model_" + parameters["model_name"][:-3] + "_map_" + parameters["map_name"][:-4]
	prediction_path_encoded = "data/" + parameters["book_name"] + "/" + parameters["book_name"] + "_post_edited_encoded/"+ spec_prefix + "/"
	shutil.rmtree(prediction_path_encoded)

print()
print("---PREDICTION MODULE COMPLETED---\n")
