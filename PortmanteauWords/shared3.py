#!/usr/bin/python
import csv
from random import shuffle
import tensorflow as tf
import pickle
import read

sess = tf.Session()
pred = 0
loss = 0
u = 0
v = 0
y = 0

def build_model(config):
	global u,v,y

	A = tf.Variable(tf.random_normal([config['dim'], config['dim']], stddev=config['std_dev']), name = 'A')
	B = tf.Variable(tf.random_normal([config['dim'], config['dim']], stddev=config['std_dev']), name = 'B')
	u = tf.placeholder(tf.float32, [None, config['dim']], name = 'u')
	v = tf.placeholder(tf.float32, [None, config['dim']], name = 'v')
	y = tf.placeholder(tf.float32, [None, config['dim']], name = 'y')
	p = tf.add( tf.transpose(tf.matmul(A, tf.transpose(u))), tf.transpose(tf.matmul(B, tf.transpose(v))) )
	#p = tf.add( tf.transpose(tf.matmul(A, tf.transpose(u))), tf.transpose(tf.matmul(A, tf.transpose(v))) )
	return p, y 

def train(train_data, config):
	global pred, loss
#
	pred, labels = build_model(config)
#
	loss = tf.losses.mean_squared_error(labels, pred)
##
	train_step = tf.train.AdamOptimizer(1e-3).minimize(loss)
	#train_step = tf.train.GradientDescentOptimizer(1e1).minimize(loss)
	#
	train_u, train_v, train_y = ([],[],[])
	for entry in train_data:
		train_u.append(entry[0])
		train_v.append(entry[1])
		train_y.append(entry[2])
	
	batch_size = 60
	init = tf.global_variables_initializer()
	sess.run(init)
	for epoch in range(config['epochs']):
		for batch_index in range(len(train_u)/batch_size):
			batch_u = train_u[batch_index*batch_size:(batch_index+1)*batch_size]
			batch_v = train_v[batch_index*batch_size:(batch_index+1)*batch_size]
			batch_y = train_y[batch_index*batch_size:(batch_index+1)*batch_size]
			sess.run(train_step, feed_dict = {u:batch_u, v:batch_v, y:batch_y})

		if(epoch%3 == 0):
			#pass
			print sess.run(loss, feed_dict = {u:train_u, v:train_v, y:train_y})

def test(test_data):
	test_u, test_v, test_y = ([],[],[])
	for entry in test_data:
		test_u.append(entry[0])
		test_v.append(entry[1])
		test_y.append(entry[2])
#
	loss_out, output = sess.run([loss, pred], feed_dict = {u:test_u, v:test_v, y:test_y})
	print loss_out
	return output

def get_data(filename):
	data = csv.DictReader(open(filename, "r"))
	data = list(data)
	clean_data = []
	for entry in data:
		try:
			a = {}
			a['Source word1'] = word_vectors[entry['Source word1']]
			a['Source word2'] = word_vectors[entry['Source word1']]
			a['Portmanteu Word'] = word_vectors[entry['Portmanteu Word']]
			clean_data.append(a)
		except:
			continue
	train = clean_data[:int(len(clean_data)*0.8)]
	test = clean_data[int(len(clean_data)*0.8):]
	return train, test

def main(_):
	read.get_input_vectors()
	read.get_all_vectors()
	data = pickle.load(open("vectors.pkl","r"))
	#shuffle(data)
	word_tuples = pickle.load(open("given_words.pkl","r"))
	config = {'dim':300, 'epochs':300, 'std_dev':0.1}
	train(data[:int(len(data)*1.8)], config)
	test_ground_truth = [word_tuple[2] for word_tuple in word_tuples[int(len(word_tuples)*0.8):]]
	out =  [list(x) for x in test(data[int(len(data)*0.8):])]
	pickle.dump(out, open("gen_vectors.pkl","w"))
	read.get_nearest_words()
	nearest_words = pickle.load(open("gen_words.pkl","r"))
	correct_predicted = 0


	for i in zip(test_ground_truth, nearest_words):
		predicted_word = i[1]
		if predicted_word == i[0]:
			correct_predicted += 1 
		print ("%s, %s"%(i[0],predicted_word))

	print "Accuracy - ", correct_predicted / float(len(nearest_words))


if __name__=='__main__':
	tf.app.run()