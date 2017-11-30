import string
import pickle  

list_of_chars = list(string.ascii_lowercase)

class model:
	def __init__(self):
		self.reset()
		self.grams = []
		with open('max_tree.txt','rb') as max_tree_file:
			self.max_tree = pickle.load(max_tree_file)
		with open('twogram.txt','rb') as two_gram_file:
			self.grams.append(pickle.load(two_gram_file))
		with open('threegram.txt','rb') as three_gram_file:
			self.grams.append(pickle.load(three_gram_file))
		with open('fourgram.txt','rb') as four_gram_file:
			self.grams.append(pickle.load(four_gram_file))
		with open('fivegram.txt', 'rb') as five_gram_file:
			self.grams.append(pickle.load(five_gram_file))
		with open('sixgram.txt', 'rb') as six_gram_file:
			self.grams.append(pickle.load(six_gram_file))

	def reset(self):
		self.index = 1
		self.fails = 0
		self.word = ""
		self.to_try = set()
		self.count=0
		for i in xrange(97, 123): self.to_try.add(chr(i))

	def use_gram(self, next_word):
		new_word = "#"+next_word+"$"
		mp, mc = 0, 'a'
		for i in range(2,7):
			for start in range(len(new_word)-i+1):
				cur = new_word[start : start + i]
				cnt = sum([1 for ch in cur if ch != '_'])
				if (cnt != i - 1): continue
				index = cur.index('_')
				den = 0
				for j in self.to_try:
					new = cur[:index] + j + cur[index+1:]
					if (new in self.grams[i-2]):
						num = self.grams[i-2][new]
						den += num
				for j in self.to_try:
					new = cur[:index] + j + cur[index+1:]
					if (new not in self.grams[i - 2]): continue
					num = self.grams[i-2][new]
					p = num / (den + .0)  #* (0.98 ** (4-i))
					if p > mp:
						mp = p
						mc = j
					# if j not in pos[index].keys():
					# 	pos[index][j] = num / (den + .0)
					# else:
					# 	pos[index][j] = max(pos[index][j], num / (den + .0))
		if mp > 0:
			return mc
		else:
			raise Exception('ykbh')

	def get_next_char(self, next_word):
		if self.word == "":
			self.word = next_word
		elif self.word == next_word:
			self.fails += 1
			self.index = ((self.index << 1) | 1)
		else:
			self.word = next_word
			self.index = (self.index << 1)
		count = sum([1 for c in self.word if c is '_'])
		self.count += 1
		if count > len(self.word)/3 and self.fails < 5 and self.index < len(self.max_tree):
			ch = self.max_tree[self.index]
		else:
			ch = self.use_gram(next_word)
		# print ch, self.to_try
		self.to_try.remove(ch)
		return ch

def solve():
	file = open('output_file.txt', 'w')
	_model = model()
	f = open('test1.txt', 'r')
	distance = 0.0
	num_words = 0.0
	index = 1
	id = 1
	#file.write("id,word,predicted_word\n")
	for line in f.readlines():
		characters_predicted = []
		_model.reset()
		index = 1
		target_word = line.strip()
		word = '_' * len(target_word)
		num_words += 1
		life = 8
		if num_words % 1000 == 0:
			print "average lavenshtein's distance for ", num_words, " words is ", distance / num_words
		while life > 0:
			if '_' not in word: break

			next_char = _model.get_next_char(word)
			characters_predicted.append(next_char)
			if next_char not in target_word:
				life -= 1
	
			temp = ""
			for i in range(len(word)):
				if target_word[i] == next_char:
					temp += next_char
				else:
					temp += word[i] 
			word = temp

		distance += sum([1 for i in range(len(word)) if not word[i] == target_word[i]])
		file.write(str(id) + "\t" + str(word) + "\t")
		characters_predicted_file = "["
		for char in characters_predicted:
			characters_predicted_file = characters_predicted_file + char + ","
		characters_predicted_file = characters_predicted_file[:-1] + "]"
		file.write(characters_predicted_file + "\n")
		id += 1 

	return distance / num_words

if __name__ == "__main__":
	print "mean lavenshtein's distance is " + str(solve())
	print "generated the output in output_file.txt"
