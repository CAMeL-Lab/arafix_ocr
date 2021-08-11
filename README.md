# arafix_ocr

## Introduction
This tool improves the output of generic OCR systems by utilizing an n-gram based post-correction approach. While most techniques that seek to improve Arabic OCR output focus on the Computer Vision aspect of converting image to text, the post correction module in our tool focuses on improving the output of OCR systems without any knowledge of the image and relying completely on the OCR text.

In addition to the post-correction system, this repo contains modules that: 
1) Utilize an external OCR API to convert image to text
2) Convert images into embedded/searchable PDFs
3) Evaluate the quality of results of the system on the word level (when the ground truth is known)

![Arafix Layout](https://github.com/aizazansari/arafix_ocr/blob/841b9deca62abe53b5647474de4a72536fb0d37f/code/utils/Arafix%20Layout.png)

## Installation Guide

- Download srilm: Navigate to this [link](http://www.speech.sri.com/projects/srilm/download.html) and download version of 1.7.3 of srilm into the main directory of this repo
- Inside configs/default.txt, add the api key in line 2
- Download models from this [link](http://www.speech.sri.com/projects/srilm/download.html). To start off, download the msa_5m.lm only
- Run the following commands:

  ```cd code```
  
  ```sh install.sh```
  
  The previous commands will install all the required dependencies for arafix. The tool should be ready to use!
  
## Usage

Arafix has 3 main modules:
1) image_to_text: converts image to text and searchable pdf
2) predict: improves the generated text from previous module
3) evaluate: evaluates the word error rate of outputs from the first and second modules

IMPORTANT NOTE: As of now, the predict module is not ready for use. Thus, all related commands in arafix have been commented out. Given the current functionality, a user can scan an image and evaluate its accuracy but the output cannot be improved using the predict module.

To run arafix, do the following:
1) Open the data folder and create a subfolder with the name of the book you intend to run arafix on
2) Within the book's subfolder, create a subfolder named <book_name>_raw_images
3) Within the <book_name>_raw_images subfolder, add all the pages of the respective book as .tif files
4) Optionally, if you intend to perform evaluation of your result (only if you have ground truth), create another subfolder within the <book_name> folder called <book_name>_ground_truth. This folder should contain the ground truth text files for your book (one file for every page). 
5) Open code/arafix.sh in a text editor
6) Modify variables* as needed
7) Open terminal and navigate to arafix_ocr
8) ```cd code```
9) ```sh arafix.sh 'book_name'```

*arafix.sh variables:
- config_name: which config file should arafix read the settings from
- start_page: which page should arafix start running from. Set it to "None" to run it from the lowest possible page.
- end_page: which page should arafix run till (inclusive). Set it to "None" to run till the highest possible page.

### [Optional] Configuration

Arafix runs with the default settings as described in the configs/default.txt file. If you wish to modify these settings, do the following:
1) Create a copy of default.txt and modify the parameters within this file
2) Update arafix.sh with the name of the new config file in config_name variable.

Configuration Parameters:
- image_to_text
  - api_key: Obtained from ocr.space, a commercial scanning software
  - skip_converted (True/False): If true, it skips files which have already been converted to save API calls
  - create_pdf (True/False): If true, it creates searchable pdfs as well

- predict
  - map_name (check mappings directory for possible options): Different mapping files are used to fix different kinds of errors
  - model_name (openiti_5m.lm, openiti_70m.lm, msa_5m.lm, msa_70m.lm): openiti models are based on islamic data while msa models are based on novels. 5m versions are quicker but less accurate
  - order (1-8): the tool performs best at order 8. if it's lower, it will take lesser time to execute at the cost of reduced accuracy
  - keep_scratch (True/False): if set to False, it deletes all the scratch files generated during prediction
  - create_pdf (True/False): if set to true, it will use fix the errors in the searchable pdf created in the previous module.

- evaluate

  select the next 3 parameters depending on the results you would like to evaluate (e.g. if you fixed errors using order 8 and segmenter mapping then select the same in this step to carry out its evaluation)
  
  - map_name 
  - model_name
  - order
  - keep_scratch (True/False): if set to False, it deletes all the scratch files generated during evaluation


## File Organization
```
📦code 
 ┣ 📂ced_word_alignment /
 ┣ 📂srilm-1.7.3 
 ┣ 📂utils 
 ┃ ┣ 📜Makefile.machine.macosx 
 ┃ ┗ 📜dependencies.txt
 ┣ 📜align_text.py
 ┣ 📜alignment.py
 ┣ 📜arafix.sh 
 ┣ 📜evaluate.py 
 ┣ 📜image_to_text.py 
 ┣ 📜install.sh 
 ┗ 📜predict.py 

📦configs 
 ┗ 📜default.txt
 
📦mappings 
 ┣ 📂empirical
 ┃ ┣ 📜emp_space_perc_f5_pg_1_top_10.map
 ┃ ┗ 📜emp_space_perc_f5_pg_1_top_5.map
 ┣ 📂visual
 ┃ ┣ 📜visual_type_1_prob_40top_6.map
 ┃ ┗ 📜visual_type_1_prob_40top_7.map
 ┗ 📜segmenter.map
 
📦models 
 ┗ 📜m2.lm
 
📦data 
┗ 📂princeton_aco001005_hi
┃ ┣ 📂princeton_aco001005_hi_alignment 
┃ ┣ 📂princeton_aco001005_hi_ground_truth 
┃ ┃ ┣ 📜ground_truth_1.txt
┃ ┃ ┣ 📜ground_truth_2.txt
┃ ┃ ┗ 📜ground_truth_3.txt
┃ ┣ 📂princeton_aco001005_hi_post_edited
┃ ┃ ┣ 📂princeton_aco001005_hi_model_m2_map_segmenter
┃ ┃ ┃ ┣ 📜predicted_1.txt
┃ ┃ ┃ ┣ 📜predicted_2.txt
┃ ┃ ┃ ┗ 📜predicted_3.txt
┃ ┣ 📂princeton_aco001005_hi_raw_embed_pdf
┃ ┣ 📂princeton_aco001005_hi_raw_images
┃ ┃ ┣ 📜princeton_aco001005_n000001_d.tif
┃ ┃ ┣ 📜princeton_aco001005_n000002_d.tif
┃ ┃ ┗ 📜princeton_aco001005_n000003_d.tif
┃ ┣ 📂princeton_aco001005_hi_raw_ocr
┃ ┃ ┣ 📜ocr_space_output_1.txt
┃ ┃ ┣ 📜ocr_space_output_2.txt
┃ ┃ ┗ 📜ocr_space_output_3.txt
```


## Technical Documentation
  - Versioning: As for python, version 3.8.3 was used. utils/dependencies.txt and install.sh contain the required packages with their respective versions.
  - Models: The models were built using the ```ngram-count``` function in the SRILM toolkit. The following specfications were used:
    - Order: 8
    - Smoothing: Kneser-Ney
    - keep-unk: True

  - arafix.sh: This bash script is the main function to be executed. It calls the 3 main modules of arafix tool. arafix_dalma.sh provides the same code but with dalma compatibility
  - image_to_text.py: This module uses the OCR Space API to convert images into text. It also stores relevant JSON info of the OCR'ed files. The settings for the API calls can be modified within ocr_space_func() 
  - predict.py: This module does the following:
    - encode the input text as follows:
      - start of word (ABC -> A\#)
      - middle of word ( ABC -> \#B\#)
      - end of word (ABC -> \#C)
      - independent letter (A -> A)
    Example: I am an apple -> I a# #m a# #n a# #p# #p# #l# #e
    - pass the encoded text to ```disambig``` function of SRILM toolkit which determines if any token needs to be changed based on the tokens that preceed it (n-gram)
    - decode the text outputted by disambig as follows:
      A# #r# #a# #f# #i# #x O# #C# #R-> Arafix OCR
      
Note: occasionally, the predicted output for a line will contain an impossible scenario such as: A #l# #a. Here, the 'A' token says that it is completely independent (A la), but the '#l#' that follows it says that it should be connected to the 'A' (Ala). In these cases, the default decoding decision is to split the word.
      
  - evaluate.py: This module uses ced_word_alignment tool to align the ground truth against ocr and predicted. Then it calculates word error rate using the following formula: (subs + deletions + insertions) / (subs + deletions + correct words) 

## Contact us

For any queries or concerns regarding the tool, feel free to contact us (the authors of the tool) on the following channels:
- Aizaz Ansari (aizaz.ansari@nyu.edu)
- Anas Jawed (anas.jawed@nyu.edu)


  
