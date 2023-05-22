from flask import Flask, request, jsonify, render_template
from tensorflow import keras
import joblib
import pandas as pd
from dnn1 import are_ind
# from sklearn.utils import shuffle


app = Flask(__name__)


# sfm_model = keras.models.load_model('models/softmax.h5')
nmf = joblib.load('models/nmf.pkl')
df = pd.read_csv('data/final.csv')

customer_idxs = df['CustomerId'].unique().tolist()

# get top 10 products
top_10_products = list(df['ProductName'].value_counts()[:10].keys())

df['PurchaseCount'] = 1
pivoted_df = df.groupby(['CustomerId', 'ProductName']).sum().reset_index()
# create pivot table
pivoted_df = pivoted_df.pivot_table(index='CustomerId', columns='ProductName', values='PurchaseCount', fill_value=0)
data = pivoted_df.copy()
for i in range(len(data)):
    total = data.iloc[i].sum().sum()
    for j in range(len(pivoted_df.iloc[0])):
        data.iloc[i,j] = round((data.iloc[i,j] / total) * 10 , 2)
        

        
customer_id_to_idx = {cust_id: i for i, cust_id in enumerate(data.index)}
product_codes = data.columns.tolist()
purchase_matrix = data.to_numpy()
W = nmf.fit_transform(purchase_matrix)
H = nmf.components_
# Get the latent factor matrix for customers
customer_latent_factors = W
# Get the latent factor matrix for products
product_latent_factors = H.T



def recommend_products_nmf(customer_id, num_recs=10):
    # already customer buy products
    customer_pro = df[df['CustomerId'] == customer_id]['ProductName'].unique()
    customer_idx = customer_id_to_idx[customer_id]
    customer_vec = customer_latent_factors[customer_idx]
    rec_scores = product_latent_factors.dot(customer_vec)
    rec_indices = (-rec_scores).argsort()[:num_recs]
    return [product_codes[i] for i in rec_indices if product_codes[i] not in customer_pro]


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommendations')
def get_recommendations():
    customer_id = request.args.get('customerId')
    area_name = request.args.get('areaName')
    industry_name = request.args.get('industryName')
    print(area_name,industry_name)
    
    try:
        customer_id = int(customer_id)
    except:
        pass
    
    if customer_id in customer_idxs:
        products = recommend_products_nmf(customer_id)
        return jsonify({'products': products})
    elif area_name and industry_name:
        products = list(are_ind(area_name,industry_name))
        return jsonify({'products': products})
    else:
        return jsonify({'products': top_10_products})
    
    
    
    # if customer_id in recommendations:
    #     products = recommendations[customer_id]
    #     return jsonify({'products': products})
    # else:
    #     return jsonify({'error': 'Customer ID not found'})


if __name__ == '__main__':
    app.run(debug=True)
