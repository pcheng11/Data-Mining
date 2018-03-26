import pandas as pd
header = ['id', 'mid_scores', 'final_scores']
data = pd.read_csv('data.online.scores.txt', delimiter = '\t', names = header)
print (data['mid_scores'].describe())
modes = data['mid_scores'].mode().values
emp_var = data['mid_scores'].var()

print ('empirical variance is {0}'.format(emp_var))
print ('modes are {0}'.format(modes))
