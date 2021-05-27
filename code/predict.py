import os 
import subprocess


def get_bookname():
	books = os.listdir("data")
	for i,book in enumerate(books):
		print(i+1," - ",book)

	booknumber = input("Select the book: ")
	bookname = books[int(booknumber)-1]
	print(bookname, " selected")
	bookname = "data/" + bookname
	return bookname

def get_model():
	
	models = os.listdir("models")
	models.sort()
	for i,model in enumerate(models):
		print(i+1," - ",model)

	modelnumber = input("Select the model: ")
	modelname = models[int(modelnumber)-1]
	print(modelname, " selected")
	modelname = "models/" + modelname


def get_mapping():
	print("1 - Segmenter")
	print("2 - Visual")
	print("3 - Empirical")
	mappingtype = input("Enter the type of mapping: ")
	if mappingtype == "1":
		mappingname = "mappings/segmenter.map"
	elif mappingtype == "2":
		mappings = os.listdir("mappings/visual")
		mappings.sort()
		for i,mapping in enumerate(mappings):
			print(i+1," - ",mapping)

		mappingnumber = input("Select the visual mapping: ")
		mappingname = mappings[int(mappingnumber)-1]
		print(mappingname, " selected")
		mappingname = "mappings/visual/" + mappingname
	else:
		mappings = os.listdir("mappings/empirical")
		mappings.sort()
		for i,mapping in enumerate(mappings):
			print(i+1," - ",mapping)

		mappingnumber = input("Select the empircal mapping: ")
		mappingname = mappings[int(mappingnumber)-1]
		print(mappingname, " selected")
		mappingname = "mappings/empircal/" + mappingname

def get_range():
	pages = os.listdir(bookname+"/ocr/")
	print("Number of pages available to post-process: ",len(pages))
	start_page = input("Enter start page for prediction: ")
	end_page = input("Enter end page for prediction: ")

def encode();

def write_encoded():


def predict():
	spec_prefix = bookname + "_" + modelname + "_" + mappingname
	os.mkdir(bookname+"/post_edited/")
	os.mkdir(bookname+"/post_edited/"+spec_prefix)

	for i in range(start_page,end_page+1):
		print("wow")


bookname = ""
os.chdir("..")
bookname = get_bookname()
print()
get_model()
print()
get_mapping()
print()
get_range()
