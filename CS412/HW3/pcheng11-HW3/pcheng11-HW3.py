from itertools import product,combinations
import csv
import copy
import pprint
from collections import defaultdict
import itertools


itemList = []
T = csv.reader(open('Data.txt'),skipinitialspace=True)
transactionList = list(T)
first_row = transactionList[0]

support = float(first_row[0])
resilience = float(first_row[1])
#print("support is {0}".format(support))
#print("resilience is {0}".format(resilience))
transactionList = transactionList[1:]
sizeOfList = len(transactionList)
#print("size of List is {0}\n\n\n".format(sizeOfList))



freq_item_set = []
for i in range(1, len(max(transactionList,key=len))):
	
	freq_dict = defaultdict(lambda : 0)
	transactions_temp = []
	for transaction in transactionList:
		transaction = sorted(list(set(transaction)))

		transaction = list(combinations(transaction,i))
		transactions_temp.append(transaction)

	for transaction in transactions_temp:
		for item in transaction:
			freq_dict[item] += 1
	
	for item in freq_dict:
		if((freq_dict[item]/sizeOfList) >= support):
			freq_item_set.append(item)

#pprint.pprint(freq_item_set)




#iterate throught the frequent itemsets to find 1-item set
txt = open('pcheng11-HW3.txt','w')

for i in freq_item_set:
	if(len(i) == 1):
		#num of outliers will always be 0 so they will always less then epsilon
		#they are all outlier resilient.
		a = [item for item in i]
		a = ', '.join(a)
		txt.write('{0}'.format(a))
		txt.write('\n')

	else:
		resilience_count = 0
		b = [item for item in i]
		#print('frequent pattern:{0}'.format(b))
		#print('--------------------------------------------------------------')
		for sub_list in transactionList:
			#check if the prequent pattern in a subset of the sequence
			if(set(b).issubset(set(sub_list))):

				#print('sequence:{0}'.format(sub_list))

				dic = {}
				for item in b:
					if item in sub_list:
						indices = [index for index, x in enumerate(sub_list) if x == item]
						dic[item] = indices
				#pprint.pprint(dic)
				#if all the item occur only once:
				index_list =[]
				L = []
				for key in dic:
					L.append(dic[key])
				
				product_list = list(itertools.product(*L))
				#print(product_list)
			
				resilience_list = []
				outlier_list = []
				for it in product_list:
					num_outliers = 0
					for x in range(min(it), max(it)+ 1):
						if sub_list[x] not in b:
							num_outliers += 1
					ε_resilience = num_outliers/len(b)
					resilience_list.append(ε_resilience)
					outlier_list.append(num_outliers)
				num_outliers = min(outlier_list)
				ε_resilience = min(resilience_list)
				if ε_resilience <= resilience:
					resilience_count += 1
				#print("num_outliers is {0}".format(num_outliers))
				#print("ε-resilience is {0}\n".format(ε_resilience))

		if resilience_count/len(transactionList) >= support:
			b = sorted(b,key = int)
			b = ', '.join(b)
			
			#print('[' +b + '] is outlier resilent\n--------------------------------------------------------------\n\n\n')
			txt.write('{0}'.format(b))
			txt.write('\n')








				











