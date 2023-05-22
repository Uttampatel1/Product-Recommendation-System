import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

data = pd.read_csv('data/customer_data.csv',names = ['CustomerId','CustomerCode','CustomerName','AreaName','IndustryName','OrderNumber','OrderDate','ProductCode','ProductName','Length'],header=None)

data.drop_duplicates(inplace=True)

data['Text'] = data['CustomerId'].astype(str) + ' ' + data['AreaName'] + ' ' + data['IndustryName']


vectorizer = CountVectorizer()
X = vectorizer.fit_transform(data['Text'])


similarity_matrix = cosine_similarity(X)

customer_id = 1662
customer_area = 'AUCKLAND SOUTH'
customer_industry = 'STEEL FABRICATORS'

customer_text = str(customer_id) + ' ' + customer_area + ' ' + customer_industry
customer_index = data[data['Text'] == customer_text].index[0]
similarity_scores = list(enumerate(similarity_matrix[customer_index]))
similarity_scores_sorted = sorted(similarity_scores, key=lambda x: x[1], reverse=True)


product_codes = []
for item in similarity_scores_sorted:
    idx = item[0]
    if idx in data.index and data.loc[idx, 'ProductName'] not in product_codes:
        product_codes.append(data.loc[idx, 'ProductName'])
    
print(product_codes[1:6])
