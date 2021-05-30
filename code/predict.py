import os 
import subprocess
import configparser


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
		os.mkdir("data/" + parameters[book_name]+ "/" + parameters[book_name] + "_ocr_encoded/")
	except:
		pass

	for i in range(parameters[start_page],parameters[end_page]+1):
		original_file = open("data/" + parameters[book_name]+ "/" + parameters[book_name] +"_ocr/" + "ocr_" + str(i) + ".txt")
		encoded_text = encode(original_file.read())
		encoded_file = open("data/" + parameters[book_name]+ "/" + parameters[book_name] + "_ocr_encoded/" + "ocr_encoded_" + str(i) + ".txt")
		encoded_file.write(encoded_text)
		original.close()
		encoded_file.close()


def predict():
	spec_prefix = parameters[book_name] + "_" + parameters[model_name] + "_" + parameters[mapping_name]
	os.mkdir("data/" + parameters[book_name] +"/" + parameters[book_name] + "_post_edited/")
	prediction_path = "data/" + parameters[book_name] + "/" + parameters[book_name] + "_post_edited/"+ parameters[book_name] + "_" spec_prefix + "/"
	os.mkdir(prediction_path)


	for i in range(start_page,end_page+1):
		raw_ocr_arg = "data/" + parameters[book_name]+ "/" + parameters[book_name] + "_ocr_encoded/" + "ocr_encoded_" + str(i) + ".txt"
		predicted_arg = prediction_path + "predicted_" + str(i) + ".txt"
        model_arg = "-lm /models/" + parameters[model_name] + " "
        map_arg = "-map mappings" + parameters[mapping_name] " "
        order_arg = "-order 8 "
        text_files = "-text " + raw_ocr_arg + ">" + predicted_arg

        command = "/Users/aizazansari/Downloads/srilm-1.7.3/bin/macosx/disambig " + model_name + "-keep-unk " + order_name + map_name + text_files
        p = subprocess.getstatusoutput(command)



os.chdir("..")

config = configparser.RawConfigParser()
config.read('config_files/default.cfg')    
parameters = dict(config.items('predict'))



