#!/bin/bash
#SBATCH --mail-type=ALL
#SBATCH --mail-user=aaa974
#SBATCH --mem=50000

module purge
module load anaconda/2-4.1.1
source activate srilm_env

/share/apps/NYUAD/srilm/1.6.0/bin/i686-gcc4/ngram-count -unk -order 8 kndiscount1 -kndiscount2 -kndiscount3 -kndiscount4 -kndiscount5 -kndiscount6 -kndiscount7 -kndiscount8 -text encoded_gigaword.txt -lm gigaword_model.lm


source deactivate