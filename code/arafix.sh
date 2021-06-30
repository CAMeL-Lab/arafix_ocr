#!/bin/sh
config_name="default.txt"
book_name="aub_aco003204"
start_page="None"
end_page="None"

echo ""

echo "~~~RUNNING ARAFIX FOR BOOK: ${book_name}~~~"

python image_to_text.py \
-config "${config_name}" \
-bookname "${book_name}" \
-startpage "${start_page}" \
-endpage "${end_page}" 


python predict.py \
-config "${config_name}" \
-bookname "${book_name}" \
-startpage "${start_page}" \
-endpage "${end_page}" 

# python evaluate.py \
# -config "${config_name}" \
# -bookname "${book_name}" \
# -startpage "${start_page}" \
# -endpage "${end_page}" 

