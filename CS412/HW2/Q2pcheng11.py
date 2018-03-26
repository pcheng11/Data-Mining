import pandas as pd 
header = ['Business id', 'State', 'City', 'Category', 'Price', 'Rating']
cube = pd.read_csv('Q2data.csv', names = header)
#print(cube[['City', 'Category', 'Price', 'Rating']])
cube1 = cube[['City', 'Category', 'Price', 'Rating']].drop_duplicates()
print(len(cube1))

cube2 = cube[['State', 'Category', 'Price', 'Rating']].drop_duplicates()
print(len(cube2))

cube3 = cube[['Category', 'Price', 'Rating']].drop_duplicates()
print(len(cube3))

print(cube.loc[(cube['State'] == 'Illinois') & (cube['Rating'] == 3) & (cube['Price'] == 'moderate')])
print(cube.loc[(cube['City'] == 'Chicago') & (cube['Category'] == 'food')])