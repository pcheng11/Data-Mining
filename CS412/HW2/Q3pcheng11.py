import csv
import copy
import pprint
from collections import defaultdict
from itertools import combinations
reader = csv.reader(open('Data.txt'), delimiter = ' ')
transaction_list = list(reader)
print(transaction_list)

should_remove = []
Li = []
countList = []
dict_list = []

for i in range(1, 7):
	new_dict = {}
	count = 0
	freq_item = []
	freq_dict = defaultdict(lambda : 0)
	transactions_temp = []
	for transaction in transaction_list:
		transaction = list(combinations(transaction,i))
		transactions_temp.append(transaction)

	for transaction in transactions_temp:
		for item in transaction:
			freq_dict[item] += 1
	
	for item in freq_dict:
		if(freq_dict[item] >= 10):
			freq_item.append(item)
			count += 1
			new_dict[item] = freq_dict[item]
	
	dict_list.append(new_dict)
	countList.append(count)
	Li.append(freq_item)

pprint.pprint(Li)
pprint.pprint(dict_list)
print(countList)
print(sum(countList))

'''
confidence
'''
'''
con1 = dict_list[2][('A', 'C', 'E')]/ dict_list[1][('C', 'E')]
print(con1)
con2 = dict_list[3][('A', 'B', 'C', 'E')]/ dict_list[2][('A', 'B', 'C')]
print(con2)


#find max pattern
length = len(Li)


for i in range(0, length):
	if(i+1<length):
		for j in range(0,len(Li[i+1])):
				a = set(combinations(Li[i+1][j],i+1))
				for it in Li[i]:
					if it in a:
						should_remove.append(it)

combined = [item for sublist in Li for item in sublist]	
max_pattern = list(set(combined)- set(should_remove))
pprint.pprint(max_pattern)
'''
