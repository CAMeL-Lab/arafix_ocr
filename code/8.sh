#!/bin/bash
#SBATCH --mail-type=ALL
#SBATCH --mail-user=aaa974
#SBATCH --mem=50000
#SBATCH --time=48:00:00

module purge
module load anaconda/2-4.1.1
module load gcc
module load srilm
source activate srilm_env

config_name="default.txt"
book_name="princeton_aco001005_hi"
start_page="None"
end_page="None"

echo ""

echo "~~~RUNNING ARAFIX FOR BOOK: ${book_name}~~~"

# python image_to_text_dalma.py \
# -config "${config_name}" \
# -bookname "${book_name}" \
# -startpage "${start_page}" \
# -endpage "${end_page}" 


python predict_dalma.py \
-config "${config_name}" \
-bookname "${book_name}" \
-startpage "${start_page}" \
-endpage "${end_page}" 

# python evaluate.py \
# -config "${config_name}" \
# -bookname "${book_name}" \
# -startpage "${start_page}" \
# -endpage "${end_page}" 

source deactivate