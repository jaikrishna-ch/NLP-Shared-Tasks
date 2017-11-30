import pickle 

g = ['a']*(2**10)
path = {}

def get(words):
	freq = [0]*26
	done = {}
	for word in words:
		for c in range(26) :
			ch = chr(ord('a')+c)
			if ch in done  or c >= 26: continue
			if path[ch] == 1: continue
			if ch in word:
				freq[c] += 1
	nc = chr(ord('a') + freq.index(max(freq)))
	return nc, [word for word in words if nc in word], [word for word in words if nc not in word]


def solve(id, words):
	if len(words) == 0 or id >= (2**10): return
	ch, left, right = get(words)
	g[id] = (ch)
	path[ch] = 1
	solve((id<<1), left)
	path[ch] = 0
	solve((id<<1)+1, right)

def build_tree():
	F = open('train.txt', 'r')
	words = [x.strip() for x in F.readlines()]
	for i in range(26): path[chr(ord('a')+i)] = 0
	print "words in the training file are ",len(words)
	root = solve(1, words)
	i = 1
	print "Done building the decision tree"

build_tree()
pickle.dump(g,open('max_tree.txt','wb'))
