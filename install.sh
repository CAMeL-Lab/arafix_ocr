if [ ! -d ced_word_alignment ]; then
	git clone https://github.com/CAMeL-Lab/ced_word_alignment.git
	cd ced_word_alignment
	pip install -r requirements.txt
else; then
	echo "ced_word_alignment already installed"
