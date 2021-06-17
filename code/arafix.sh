#!/bin/sh
config_name="default.txt"
book_name="princeton_aco001005_hi"
start_page="1"
end_page="5"

echo ""

echo "~~~RUNNING ARAFIX FOR BOOK: ${book_name}~~~"

python image_to_text.py \
-config "${config_name}" \
-bookname "${book_name}" 

python predict.py \
-config "${config_name}" \
-bookname "${book_name}" \
-startpage "${start_page}" \
-endpage "${end_page}" 

python evaluate.py \
-config "${config_name}" \
-bookname "${book_name}" \
-startpage "${start_page}" \
-endpage "${end_page}" 

