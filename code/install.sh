#installing ced_word_alignment

if [ ! -d ced_word_alignment ]
then
	git clone https://github.com/CAMeL-Lab/ced_word_alignment.git
	cd ced_word_alignment
	pip install -r requirements.txt
	cd ..
else
	echo "ced_word_alignment already installed!"
fi

if [! -d srilm ]
then
	echo "install srilm"
	mkdir srilm
	cd ..
	mv srilm-1.7.3.tar.gz code/srilm/
	cd code/srilm
	tar xvf srilm-1.7.3.tar.gz
	srilm_dir=$(pwd)
	srilm_dir=${srilm_dir//\//\\/}

	sed -i '.backup' "s/# SRILM = \/home\/speech\/stolcke\/project\/srilm\/devel/SRILM = $srilm_dir/g" Makefile
	rm Makefile.backup

	mv ../utils/Makefile.machine.macosx Makefile.machine.macosx

	make World 

else
	echo "srilm already installed!"
fi