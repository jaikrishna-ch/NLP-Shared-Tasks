#!/usr/bin/python
import pickle
from sklearn.neighbors import NearestNeighbors as nnbr
import numpy as np
import string

diction = {}
def load_vectors(file_name):
	global diction
	word_vec = {}
	count = 0
	validChars = set(string.ascii_lowercase)
	with open(file_name, 'r') as f:
		for line in f:
			try:
				x = line.split()
				mylist = list(map(float,x[1:]))
				if len(mylist)!=300:
					continue
				if any(char not  in validChars for char in x[0].lower()):
					continue
				word_vec[x[0]] = mylist
			except:
				continue
			count+=1
			if count%10000==0:
				pass
				#print count
	diction = word_vec
	return word_vec

def get_all_vectors():
	output = {}
	diction = pickle.load(open("fast_inp.pkl","r"))
	porm_dic = {}
	vectors = []
	with open('input_words','r') as f:
		lines = f.readlines()
		line_cnt = len(lines)
		crt_line = 47
		while crt_line+2 < line_cnt:
			word1 = lines[crt_line].split()[0]
			if word1 in diction.keys():
				output[word1] = diction[word1]
			word2 = lines[crt_line+2].split()[0]
			if word2 in diction.keys():
				output[word2] = diction[word2]
			porm_word = lines[crt_line+4].split()[0]
			if porm_word in diction.keys():
				output[porm_word] = diction[porm_word]
				porm_dic[porm_word] = diction[porm_word]
			crt_line+=8
		pickle.dump(output,open('fast_inp2.pkl','w'))
		pickle.dump(porm_dic,open('porm_dic.pkl','w'))

def get_input_vectors():
	output = pickle.load(open('fast_inp.pkl','r'))
	vectors = []
	words = []
	pom_vecs = []
	with open('input_words','r') as f:
		lines = f.readlines()
		line_cnt = len(lines)
		crt_line = 47
		while crt_line+2 < line_cnt:
			word1 = lines[crt_line].split()[0]
			word2 = lines[crt_line+2].split()[0]
			porm_word = lines[crt_line+4].split()[0]
			if word1 in output.keys() and word2 in output.keys() and porm_word in output.keys():
				vectors.append((output[word1],output[word2],output[porm_word]))
				words.append((word1, word2, porm_word))
				pom_vecs.append(output[porm_word])
			crt_line+=8
		pickle.dump(vectors,open('vectors.pkl','w'))
		pickle.dump(words,open('given_words.pkl','w'))
		pickle.dump(pom_vecs, open('given_outvec.pkl','w'))	

def get_nearest_words():
	diction = pickle.load(open('porm_dic.pkl','r'))
	output = pickle.load(open('gen_vectors.pkl','r'))
	md = nnbr(n_neighbors=1).fit(np.array(diction.values()))
	#print "Trained the model!"
	Y = np.array(output)
	#print "Retrived the similarities"
	distances, indices = md.kneighbors(Y)
	word_indexes = [int(x) for x in indices]
	words = [diction.keys()[index] for index in word_indexes]
	#print "Dumping the generated words!"
	pickle.dump(words, open("gen_words.pkl","w"))

def main():
	load_vectors('wiki.en.vec')
	#print "Successfully loaded the vectors!"
	#print "\n"
	get_all_vectors()
	

if __name__=='__main__':
	main()