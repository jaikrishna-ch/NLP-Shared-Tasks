clean1 : clean.py
	python clean.py
	make start
start : ngram.py
	python ngram.py
	make tree
tree :  new_make.py
	python new_make.py
	make run
run : 	main.py
	python main.py
	make clean
clean : 
	rm -f twogram.txt threegram.txt fourgram.txt fivegram.txt sixgram.txt max_tree.txt test1.txt
