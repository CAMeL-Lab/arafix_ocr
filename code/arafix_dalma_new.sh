#!/bin/bash
#SBATCH --mem=100000
#SBATCH --time=48:00:00
#SBATCH --mail-type=ALL
#SBATCH --mail-user=aaa974

module purge
module load anaconda/2-4.1.1
module load gcc
module load srilm
source activate srilm_env

config_name=$1
book_name=$2
start_page="9"
end_page="29"

echo ""

echo "~~~RUNNING ARAFIX FOR BOOK: ${book_name}~~~"

# python image_to_text_dalma.py \
# -config "${config_name}" \
# -bookname "${book_name}" \
# -startpage "${start_page}" \
# -endpage "${end_page}" 


python predict_dalma_new.py \
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
