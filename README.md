# arafix_ocr

## Installation Guide

- Download srilm: Navigate to this [link](http://www.speech.sri.com/projects/srilm/download.html) and download version of 1.7.3 of srilm
- Move srilm: Move srilm to the main directory of this repository
- Run the following commands:

  ```cd code```
  
  ```sh install.sh```
  
  The previous command will install all the required dependencies for arafix. The tool should be ready to use!
  
  
## File Organization

## Usage

To run arafix, do the following:
1) Open code/arafix.sh in a text editor
2) Modify variables as needed
3) Open terminal and navigate to arafix_ocr
4) ```cd code```
5) ```sh arafix.sh```

arafix.sh variables:
- config_name: which config file should arafix read the settings from
- book_name: which book should arafix run on
- start_page: which page should arafix start running from 
- end_page: which page should arafix run till (inclusive)


### [Optional] Configuration

Arafix runs with the default settings as described in the configs/default.txt file. If you wish to modify these settings, do the following:
1) Create a copy of default.txt and modify the parameters within this file
2) Update arafix.sh with the name of the new config file in config_name variable.

Configuration Parameters:
- [image_to_text]
  - api_key: Obtained from ocr.space, a commercial scanning software
  - skip_converted (True/False): If true, it skips files which have already been converted to save API calls
  - create_pdf (True/False): If true, it creates searchable pdfs as well

- [predict]
  - map_name (check mappings directory for possible options): Different mapping files are used to fix different kinds of errors
  - model_name (m1.lm/m2.lm): m1 is more accuracte but slower 
  - order (1-8): the tool performs best at order 8. if it's lower, it will take lesser time to execute at the cost of reduced accuracy
  - keep_scratch (True/False): if set to False, it deletes all the scratch files generated during prediction
  - create_pdf (True/False): if set to true, it will use fix the errors in the searchable pdf created in the previous module.

- [evaluate]
  select the next 3 parameters depending on the results you would like to evaluate (e.g. if you fixed errors using order 8 and segmenter mapping then select the same in this step to carry out its evaluation)
  - map_name 
  - model_name
  - order
  - keep_scratch (True/False): if set to False, it deletes all the scratch files generated during evaluation

## Documentation
  
  
