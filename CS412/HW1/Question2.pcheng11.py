import numpy as np
import pandas as pd

header = ['id', 'mid_scores', 'final_scores']
data = pd.read_csv('data.online.scores.txt', delimiter = '\t', names = header)

#Q2 part a

data['z_score'] = (data['mid_scores'] - data['mid_scores'].mean())/(data['mid_scores'].std())

print ('the variance after normalization is {0}'.format(data['z_score'].var(ddof = 1)))
print('\n')
#Q2 part b
df_90 = data.query('mid_scores == 90')
print (df_90)

print('\n')
print (data.cov())
print('\n')
#we find the covariance between midterm scores and final exam scores to be 78.254194
#base on the formula for calculating perason's correlation coefficient, we get:
print ("Pearson's correlation coefficient between midterm scores and final scores is {0}".format(78.254194 / (data['mid_scores'].std() * data['final_scores'].std())))