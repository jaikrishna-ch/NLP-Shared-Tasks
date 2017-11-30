import csv
import string 
import pickle
train_data = []

def isalpha_(ch): return ch in ['$', '#'] or ch.isalpha()


def generate(gram_len, names_of_files):
	print "Making " + str(gram_len) + " gram pickle file " 
	character_counts = {}

	gram_size = gram_len
	four_grams = set()
	grams = {}
	for word in train_data:
		if(len(word) < gram_size):
			continue
		for position in range(0, len(word)-gram_size + 1):
			gram_short = word[position:position+gram_size]
			danger = 0
			for char in gram_short:
				if not isalpha_(char):
					danger = 1
			if danger == 1:
				continue
			if gram_short not in grams:
				grams[gram_short] = 1
			else:
				grams[gram_short] += 1

	a1_sorted_keys = sorted(grams, key=grams.get, reverse=True)
	f = open(names_of_files[gram_len-2],'w')
	pickle.dump(grams, f)

if __name__ == "__main__":
	list_of_chars = list(string.ascii_lowercase)

	names_of_files = ["twogram.txt", "threegram.txt", "fourgram.txt", "fivegram.txt", "sixgram.txt"]
	with open('train.txt', 'rb') as f:
		reader = csv.reader(f)
		for row in reader:
			train_data.append('#' + str(row[0]).strip() + '$')
	for size in range(2, 7):
		generate(size, names_of_files)