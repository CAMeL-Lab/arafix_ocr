#!/bin/sh
config_name="default.txt"
book_name="princeton_aco001005_hi"
start_page="7"
end_page="5"


# python image_to_text.py 
# --config "${config_name}" 
# --bookname "${book_name}"

python predict.py \
--config "${config_name}" \
--bookname "${book_name}" \
--startpage "${start_page}" \
--endpage "${end_page}" \
