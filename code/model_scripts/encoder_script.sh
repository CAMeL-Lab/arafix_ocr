#!/bin/bash
#SBATCH --mail-type=ALL
#SBATCH --mail-user=aaa974


module purge
module load anaconda/2-4.1.1
source activate srilm_env

cat ../../../nlp/CAMeLBERT/data/raw_clean_sents/MSA-* | python encoder.py > encoded_msa_433.txt

source deactivate