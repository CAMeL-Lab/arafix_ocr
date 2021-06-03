#!/bin/sh
config_name="default.txt"
book_name="princeton_aco001005_hi"

python image_to_text.py --config "${config_name}" --bookname "${book_name}"
python predict.py --config "${config_name}" --bookname "${book_name}"