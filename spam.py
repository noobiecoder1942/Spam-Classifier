import sys
import os
import numpy as np
from collections import defaultdict
import re
from tqdm import tqdm


# READING COMMAND LINE ARGUMENTS

(training_directory, testing_directory, output_file) = sys.argv[1:]

# (training_directory, testing_directory, output_file) = ('train', 'test', 'output_file.txt')

# PREPARE TRAINING AND TESTING DATA

X_train = []
Y_train = []

X_test = []
Y_preds = []

for tag in os.listdir(training_directory):
    for document in os.listdir(os.path.join(training_directory, tag)):
        with open(os.path.join(training_directory, tag, document), 'r', encoding = 'ISO-8859-1') as f:
            X_train.append(f.read())
            Y_train.append(tag)


ini = Y_train.count('spam') / len(Y_train)


# CLEANING DATA

def text_cleaning(list_of_instances):

	# CARRY OUT CLEANING OPEARTIONS eg. REGEX PARSING FOR REMOVING EMAIL HEADERS ETC.
	for i in list_of_instances:
		i = i.lower()
		i = re.sub("<.*?>", " ", i)


	return 'DONE'

text_cleaning(X_train)
text_cleaning(X_test)

class NBC():

	# init constructor
	def __init__(self, ini = ini):
		self.ini = ini
		self.prob = []

	# training function
	def train(self, training_data, training_labels):
		total_spam = 0
		total_notspam = 0

		for tl in tqdm(training_labels):
			if tl == 'spam':
				total_spam += 1
			else:
				total_notspam += 1

		counts = self.count_words(training_data, training_labels)
		self.prob = self.probabilities(counts, total_spam, total_notspam)

	def count_words(self, training_data, training_labels):
		counts = defaultdict(lambda : {'spam' : 0, 'notspam' : 0})

		for td, tl in zip(training_data, training_labels):
			for word in td.split():
				counts[word][tl] += 1

		return counts

	def probabilities(self, counts, total_spam, total_notspam):
		temp = {}

		for t in list(counts.items()):
			prob_word_spam = (self.ini + t[1]['spam']) / (2 * self.ini + total_spam)
			prob_word_notspam = (self.ini + t[1]['notspam']) / (2 * self.ini + total_notspam)
			temp[t[0]] = {'spam' : prob_word_spam, 'notspam': prob_word_notspam}

		return temp

	def predict(self, testing_instance):
		spam_prob = 0
		notspam_prob = 0


		# print('LENGTH OF DICT ======', len(self.prob))
		for word in testing_instance.split():
			try:
				spam_prob += np.log(self.prob[word]['spam'])
				notspam_prob += np.log(self.prob[word]['notspam'])
			except:
				spam_prob += np.log(0.5)
				notspam_prob += np.log(0.5)

		if spam_prob > notspam_prob:
			return 'spam'
		else:
			return 'notspam'

	def accuracy(self, true_labels, predicted_labels):
		cnt = 0
		for i in range(len(true_labels)):
			if true_labels[i] == predicted_labels[i]:
				cnt += 1

		return cnt/len(true_labels)

	def predict_over_mutiple_instances(self, testing_data):
		results = []
		for i in testing_data:
			results.append(self.predict(i))

		return results

model = NBC()

model.train(X_train, Y_train)

outputs = []

for i in os.listdir(testing_directory):
	t = str(i)
	with open(os.path.join(testing_directory, i), 'r', encoding = 'ISO-8859-1') as fp:
		test = fp.read()
	x = model.predict(test)
	t += ' '
	t += x
	outputs.append(t)


with open(output_file, 'w') as fp:
	for i in outputs:
		fp.write('%s\n' %i)


# y = model.predict_over_mutiple_instances(X_test)

# print(model.accuracy(y, Y_preds))

#### ACCURACY IS 98.39467%.