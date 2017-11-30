import csv

f1 = open('test1.txt', 'w')
with open('test.txt', 'rb') as f:
	reader = csv.reader(f)
	count = 0
	for row in reader:
		if count == 0:
			count += 1
			continue
		f1.write(row[1] + "\n")