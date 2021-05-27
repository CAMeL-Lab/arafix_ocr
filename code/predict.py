import os 
import subprocess


def disambig():
	print(1)


def get_bookname():
	bookname = input("Enter the name of book: ")
	
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
	start_page = input("Enter start page for prediction: ")
	end_page = input("Enter end page for prediction: ")



os.chdir("..")
get_model()
print()
get_mapping()
