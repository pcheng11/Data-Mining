import numpy as np
import pandas as pd
import math
from scipy.spatial.distance import minkowski
from sklearn.metrics.pairwise import cosine_similarity as cos

#Q3 part b
data = pd.read_csv('data.libraries.inventories.txt', delimiter = '\t')
#print (data)
CML = data.iloc[0][1:]
#print(CML)
CBL = data.iloc[1][1:]
#print(CBL)

#Q3 part c
h_1 = minkowski(CBL, CML, 1)
h_2 = minkowski(CBL, CML, 2)
h_inf = minkowski(CBL, CML, math.inf)
print ('minkowski distance for h == 1 is {0}'.format(h_1))
print ('minkowski distance for h == 2 is {0}'.format(h_2))
print ('minkowski distance for h approaches infinity is {0}'.format(h_inf))

#Q3 part d
cos_sim = np.dot(CML, CBL) / (np.linalg.norm(CML) * np.linalg.norm(CBL))
print (cos_sim)

length = len(CML)

CML_sum = CML.sum()
CBL_sum = CBL.sum()
book_sum = CBL_sum + CML_sum
CML_prob = np.zeros(length,)
CBL_prob = np.zeros(length,)
for i in range(len(CML)):
	CML_prob[i] = CML[i] / CML_sum
	CBL_prob[i] = CBL[i] / CBL_sum
#calculating KL divergence:
KLD = np.sum(CML_prob*np.log(CML_prob/CBL_prob))
print (KLD)


buy_beer_sum = 190
no_beer_sum = 3315
buy_diaper_sum = 165
no_diaper_sum = 3340

tol_sum = buy_beer_sum  + no_beer_sum
buy_beer = np.array([150, 40])
no_beer = np.array([15, 3300])
buy_beer_exp = np.array([buy_diaper_sum * (buy_beer_sum/tol_sum), no_diaper_sum * (buy_beer_sum/tol_sum)])
no_beer_exp = np.array([buy_diaper_sum * (no_beer_sum/tol_sum), no_diaper_sum * (no_beer_sum/tol_sum)])
chi_square = np.sum((buy_beer - buy_beer_exp)**2 / buy_beer_exp) + np.sum((no_beer - no_beer_exp)**2 / no_beer_exp)


print (chi_square)

