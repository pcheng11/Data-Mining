import random
import sys
import math
import os


def split_on_feature_value(data, best_attribute_index, value):
	split_data = []
	for i in data:
		if i[best_attribute_index] == value:
			split_data.append(i)	
	return split_data

def gini_index_for_value(split_data, num_records):
	label_list = {}
	for i in split_data:
		if i[0] not in label_list:
			label_list[i[0]] = 1
		else:
			label_list[i[0]] += 1

	value_sum = 0
	temp = 0
	for i in label_list.values():
		value_sum += i
	for i in label_list.values():
		temp += (i/value_sum)**2
	gini_value = (value_sum/num_records) *(1 - temp)

	return gini_value

def get_value_for_attribute(data, best_attribute_index):
	record_length = len(data[0])
	attribute_value = []
	for i in data:
		attribute_value.append(i[best_attribute_index])
	attribute_value = set(attribute_value)
	return list(attribute_value)

def GINI(data, attribute_set, use_feature_bagging):
	
	new_attribute_set = []
	#USING 'SELECT RANDOM ATTRIBUTE OF SIZE LESS THAN ATTRIBUTE NUMBER'
	#AKA. attribute bagging
	if use_feature_bagging == 1:
		attribute_size = len(attribute_set)
		#print (attribute_size)
		for i in range(0, int(attribute_size**(1/2))):
			new_attribute_set.append(list(attribute_set)[random.randint(0, attribute_size-1)])
	else:
		new_attribute_set = attribute_set
	
	gini_index_value_list = {}
	for attribute in new_attribute_set:
		num = 0
		for value in get_value_for_attribute(data, attribute):
			split_data = split_on_feature_value(data, attribute, value)
			gini_index = gini_index_for_value(split_data, len(data))
			num += gini_index
		gini_index_value_list[attribute] = num
	least_value = min(gini_index_value_list.values())
	attribute_with_least_gini= [k for k, v in gini_index_value_list.items() if v == least_value]
	return attribute_with_least_gini[0]



class creatTreeNode(object):
  def __init__(self, attribute_index = None , value = None, label = None, freq = None, attribute_left =0):
    self.attribute_index = attribute_index
    self.children = []
    self.value = value
    self.label = label
    self.freq = freq
    self.attribute_left = attribute_left


def decisionTree(data, attribute_set, use_feature_bagging):
	#print (len(attribute_set))
	check_label = []
	treeNode = creatTreeNode()
	#if all the class label is the same, assign that class label and return node.
	for i in data:
		check_label.append(i[0])
	distinct_label = list(set(check_label))


	if(len(distinct_label)== 1):
		treeNode.label = distinct_label[0]
		return treeNode
	

	#for led if there is attribute left to split and lables are distinct, we choose the majority
	#if(treeNode.attribute_left == 0 and len(distinct_label) > 1):
	if(len(attribute_set) == 0 and len(distinct_label) > 1):
		#print(check_label)
		majority = {}
		for it in check_label:
			if it not in majority:
				majority[it] = 1
			else:
				majority[it] += 1
		mj = max(majority.values())
		treeNode.label = [k for k, v in majority.items() if v == mj][0]
		return treeNode


	if treeNode.value == None:
		treeNode.value = ('ROOT')

	#choose an attribute to split
	treeNode.attribute_index = GINI(data, attribute_set, use_feature_bagging)
	#start to build a tree
	i = 0;
	for value in get_value_for_attribute(data, treeNode.attribute_index):
		new_data = split_on_feature_value(data, treeNode.attribute_index, value)
		new_attribute_set = set(attribute_set) - set([treeNode.attribute_index])
		treeNode.children.append(decisionTree(new_data, new_attribute_set, use_feature_bagging))
		treeNode.children[i].value = value

		most_common_label = {}
		for child in treeNode.children:
			if child.label not in most_common_label and child.freq not in most_common_label:
				if(child.label != None):
					most_common_label[child.label] = 1
				if(child.label == None and child.freq != None):
					most_common_label[child.freq] = 1
			else:
				if(child.label != None):
					most_common_label[child.label] += 1
				if(child.label == None and child.freq != None):
					most_common_label[child.freq] += 1
		
		if len(most_common_label.values())!= 0:
			mcl = max(most_common_label.values())
			treeNode.freq = [k for k, v in most_common_label.items() if v == mcl][0]
		i += 1

	return treeNode


def build_randomForest(train_data_file, tree_num, sample_size, use_feature_bagging):
	data= []
	with open(train_data_file,'r') as raw:
		for i in raw:
			#print(i)
			record = []
			temp1 = i.replace(' ',',')
			temp2 = temp1.replace(':',',')
			temp3 = temp2.replace('\n',',')
			j = 0
			temp = ''
			while temp3[j]!= ',':

				temp += temp3[j]
				j+=1
				if j >= len(temp3):
					break
				if temp3[j] == ',':
					record.append(int(temp))
					temp = ''
					j+= 1
				if j >= len(temp3):
					break
			#print(record)

			for index in range(1, len(record)-1, 2):
				record[index] = 0
			record = [value for value in record if value != 0]
			data.append(record)
		sample_num = len(data)

	attribute_set = []
	for i in range(1, len(data[0])):
		attribute_set.append(i)	

	#create a forest list
	forest = []
	for j in range(0, tree_num):
		bootstrap_data = []
		for i in range(0, sample_size):
			bootstrap_data.append(data[random.randint(0,sample_num-1)])
		#print(attribute_set)
		forest.append(decisionTree(bootstrap_data, attribute_set, use_feature_bagging))

	return forest


def test_each_tree(treeNode, sample):
	if treeNode.label != None:
		#print('predict label {0}'.format(treeNode.label))
		predicted_label = treeNode.label
		return predicted_label

	else:
		num = 0
		for child in treeNode.children:
			num += 1
			attr = treeNode.attribute_index
			if child.value == sample[attr]:
				return test_each_tree(child,sample)
			else:
				if child.value != sample[attr] and num == len(treeNode.children):
					predicted_label = treeNode.freq
					return predicted_label

def test_whole_forest(forest, sample):
	vote = {}
	for treeNode in forest:
		predicted_label = test_each_tree(treeNode, sample)
		if predicted_label not in vote:
			vote[predicted_label] = 1
		else:
			vote[predicted_label] += 1
	predicted_label = max(vote, key = vote.get)
	return predicted_label

def predict(test_data_file, forest):
	test_data = []
	with open(test_data_file,'r') as raw:
		for i in raw:
			#print(i)
			record = []
			temp1 = i.replace(' ',',')
			temp2 = temp1.replace(':',',')
			temp3 = temp2.replace('\n',',')
			j = 0
			temp = ''
			while temp3[j]!= ',':

				temp += temp3[j]
				j+=1
				if j >= len(temp3):
					break
				if temp3[j] == ',':
					record.append(int(temp))
					temp = ''
					j+= 1
				if j >= len(temp3):
					break

			for index in range(1, len(record)-1, 2):
				record[index] = 0
			record = [value for value in record if value != 0]
			test_data.append(record)


	confusion_dic = {}
	correct_num = 0
	if 'led' in test_data_file:
		class_label_num = 2
		for i in range(1, 3):
			confusion_dic[i] = [0] * class_label_num 
	if 'balance' in test_data_file:
		class_label_num = 3
		for i in range(1, 4):
			confusion_dic[i] = [0] * class_label_num 
	if 'synthetic' in test_data_file:
		class_label_num = 4
		for i in range(1, 5):
			confusion_dic[i] = [0] * class_label_num 
	if 'nursery' in test_data_file:
		class_label_num = 5
		for i in range(1, 6):
			confusion_dic[i] = [0] * class_label_num 

	for sample in test_data:
		predicted_label = test_whole_forest(forest, sample)
		confusion_dic[sample[0]][predicted_label-1] += 1
		if predicted_label == sample[0]:
			correct_num += 1

	correctness = correct_num/len(test_data)
	#print(correctness)
	temp_list = []
	for i in confusion_dic.keys():
		temp_list.append(i)
	temp_list = sorted(temp_list)
	#print(temp_list)
	for i in temp_list:
		for j in confusion_dic[i]:
			print(str(j) + ' ', end = '')
		print()


training_file = os.path.abspath(sys.argv[1])
testing_file = os.path.abspath(sys.argv[2])

# tree num , sample size , use feautre bagging
if 'nursery' in training_file:

	forest = build_randomForest(training_file, 240, 1740, 1)
	predict(testing_file, forest)

if 'led' in training_file:
	forest = build_randomForest(training_file, 130, 155, 1)
	predict(testing_file, forest)
	
if 'balance.scale' in training_file:
	
	forest = build_randomForest(training_file, 150, 20, 1)
	predict(testing_file, forest)

if 'synthetic.social' in training_file:
	forest = build_randomForest(training_file, 300, 2000, 1)
	predict(testing_file, forest)
