# Installing brew, git and python
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install git
brew install python

#Installing required python packages

pip install -r code/utils/dependencies.txt


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

if [ ! -d srilm ]
then
	echo "install srilm"
	mkdir srilm-1.7.3
	cd ..
	mv srilm-1.7.3.tar.gz code/srilm-1.7.3/
	cd code/srilm-1.7.3
	tar xvf srilm-1.7.3.tar.gz
	srilm_dir=$(pwd)
	srilm_dir=${srilm_dir//\//\\/}

	sed -i '.backup' "s/# SRILM = \/home\/speech\/stolcke\/project\/srilm\/devel/SRILM = $srilm_dir/g" Makefile
	rm Makefile.backup

	cp ../utils/Makefile.machine.macosx common/Makefile.machine.macosx

	make World 

else
	echo "srilm already installed!"
fi