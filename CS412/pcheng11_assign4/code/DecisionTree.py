import sys
import random
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

def GINI(data, attribute_set):
	#temp = 1
	gini_index_value_list = {}
	for attribute in attribute_set:
		num = 0
		for value in get_value_for_attribute(data, attribute):
			split_data = split_on_feature_value(data, attribute, value)
			gini_index = gini_index_for_value(split_data, len(data))
			num += gini_index
		gini_index_value_list[attribute] = num
	#if len(gini_index_value_list.values()) == 0:
		#return 0
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


def decisionTree(data, attribute_set):
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
	treeNode.attribute_index = GINI(data, attribute_set)
	#start to build a tree
	i = 0;
	for value in get_value_for_attribute(data, treeNode.attribute_index):
		new_data = split_on_feature_value(data, treeNode.attribute_index, value)
		new_attribute_set = set(attribute_set) - set([treeNode.attribute_index])
		treeNode.children.append(decisionTree(new_data, new_attribute_set))
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

def build_tree(train_data_file):
#parse the file
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

	attribute_set = []
	for i in range(1, len(data[0])):
		attribute_set.append(i)	

#build the tree
	return decisionTree(data, attribute_set)


'''
ONLY for Print Tree

'''
'''
def print_tree(current_node, indent="", last='updown'):

    nb_children = lambda node: sum(nb_children(child) for child in node.children) + 1
    size_branch = {child: nb_children(child) for child in current_node.children}

    """ Creation of balanced lists for "up" branch and "down" branch. """
    up = sorted(current_node.children, key=lambda node: nb_children(node))
    down = []
    while up and sum(size_branch[node] for node in down) < sum(size_branch[node] for node in up):
        down.append(up.pop())

    """ Printing of "up" branch. """
    for child in up:     
        next_last = 'up' if up.index(child) is 0 else ''
        next_indent = '{0}{1}{2}'.format(indent, ' ' if 'up' in last else '│', " " * (len(str(current_node.value)) + 36))
        print_tree(child, indent=next_indent, last=next_last)

    """ Printing of current node. """
    if last == 'up': start_shape = '┌'
    elif last == 'down': start_shape = '└'
    elif last == 'updown': start_shape = ' '
    else: start_shape = '├'

    if up: end_shape = '┤'
    elif down: end_shape = '┐'
    else: end_shape = ''
    if current_node.label == None:
    	print ('{0}{1}{2}--(Attr:{3})--(most_common_label:{4})-{5}-{6}'.format(indent, start_shape, current_node.value, current_node.attribute_index, current_node.freq,current_node.attribute_left,end_shape))
    else:
    	print ('{0}{1}{2}----(CLASS {3})-{4}{5}'.format(indent, start_shape, current_node.value, current_node.label,current_node.attribute_left, end_shape))

    """ Printing of "down" branch. """
    for child in down:
        next_last = 'down' if down.index(child) is len(down) - 1 else ''
        next_indent = '{0}{1}{2}'.format(indent, ' ' if 'down' in last else '│', " " *( len(str(current_node.value))+36))
        print_tree(child, indent=next_indent, last=next_last)
'''



#test each sample in the test data set
def test(treeNode, data_record):
	if treeNode.label != None:
		predicted_label = treeNode.label
		return predicted_label
	else:
		num = 0
		for child in treeNode.children:
			num += 1
			attr = treeNode.attribute_index
			if child.value == data_record[attr]:
				return test(child,data_record)
			else:
				#unseen values for a featrue
				if child.value != data_record[attr] and num == len(treeNode.children):
					predicted_label = treeNode.freq
					return predicted_label
					#return test(child,data_record)

#calculate the accuracy of the tree
def predict(test_data_file, root):
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
		predicted_label = test(root, sample)
		confusion_dic[sample[0]][predicted_label-1] += 1
		if predicted_label == sample[0]:
			correct_num += 1

	correctness = correct_num/len(test_data)

	temp_list = []
	for i in confusion_dic.keys():
		temp_list.append(i)
	temp_list = sorted(temp_list)
	#print(temp_list)
	for i in temp_list:
		for j in confusion_dic[i]:
			print(str(j) + ' ', end = '')
		print()



#run the program...
training_file = os.path.abspath(sys.argv[1])
testing_file = os.path.abspath(sys.argv[2])

root = build_tree(training_file)
predict(testing_file, root)

