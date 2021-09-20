#!/bin/bash
config_name="default.txt"
book_name=$1
start_page="None"
end_page="None"

if [ $# -eq 1 ]; then
    first_arg="None"
	second_arg="None"
	third_arg="None"
fi

if [ $# -eq 2 ]; then
	first_arg=$2
	second_arg="None"
	third_arg="None"
fi

if [ $# -eq 3 ]; then
	first_arg=$2
	second_arg=$3
	third_arg="None"
fi

if [ $# -eq 4 ]; then
	first_arg=$2
	second_arg=$3
	third_arg=$4
fi 

cd code

echo ""

echo "~~~RUNNING ARAFIX FOR BOOK: ${book_name}~~~"


if [ $first_arg = "image_to_text" ] || [ $second_arg = "image_to_text" ] || [ $third_arg = "image_to_text" ]
then
python image_to_text.py \
-config "${config_name}" \
-bookname "${book_name}" \
-startpage "${start_page}" \
-endpage "${end_page}" 
fi

if [ $first_arg = "predict" ] || [ $second_arg = "predict" ] || [ $third_arg = "predict" ]
then
python predict.py \
-config "${config_name}" \
-bookname "${book_name}" \
-startpage "${start_page}" \
-endpage "${end_page}" 
fi

if [ $first_arg = "evaluate" ] || [ $second_arg = "evaluate" ] || [ $third_arg = "evaluate" ]
then
python evaluate.py \
-config "${config_name}" \
-bookname "${book_name}" \
-startpage "${start_page}" \
-endpage "${end_page}" 
fi
