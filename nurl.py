# Load the data
import pandas as pd
data = pd.read_csv('data/customer_data.csv',names = ['CustomerId','CustomerCode','CustomerName','AreaName','IndustryName','OrderNumber','OrderDate','ProductCode','ProductName','Length'],header=None)
data.drop(['CustomerCode','CustomerName','OrderNumber','OrderDate','ProductCode','Length'],axis=1,inplace=True)
data.drop_duplicates(inplace=True)
# Preprocess the data
from sklearn.preprocessing import OneHotEncoder
enc = OneHotEncoder()
X = enc.fit_transform(data[['CustomerId', 'AreaName', 'IndustryName']])
y = data['ProductName']

# Split the data into training and validation sets
from sklearn.model_selection import train_test_split
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Define the embedding layers
from keras.layers import Input, Embedding, Concatenate, Dense
from keras.models import Model
num_customers = X.shape[1]
num_products = len(y.unique())
num_areas = len(data['AreaName'].unique())
num_industries = len(data['IndustryName'].unique())

customer_input = Input(shape=(num_customers,))
customer_embedding = Embedding(num_customers, 32, input_length=num_customers)(customer_input)
area_input = Input(shape=(num_areas,))
area_embedding = Embedding(num_areas, 8, input_length=num_areas)(area_input)
industry_input = Input(shape=(num_industries,))
industry_embedding = Embedding(num_industries, 16, input_length=num_industries)(industry_input)

# Build the model
concatenated = Concatenate()([customer_embedding, area_embedding, industry_embedding])
dense1 = Dense(64, activation='relu')(concatenated)
dense2 = Dense(32, activation='relu')(dense1)
output = Dense(num_products, activation='softmax')(dense2)
model = Model(inputs=[customer_input, area_input, industry_input], outputs=output)
model.compile(loss='categorical_crossentropy', optimizer='adam')

# Train the model
model.fit([X_train[:,0], X_train[:,1], X_train[:,2]], y_train, epochs=10, batch_size=32, validation_data=([X_val[:,0], X_val[:,1], X_val[:,2]], y_val))

# Evaluate the model
model.evaluate([X_val[:,0], X_val[:,1], X_val[:,2]], y_val)

def get_top_recommendations(model, customer_id, area_name, industry_name, num_recommendations=10):
    customer_encoded = enc.transform([[customer_id, area_name, industry_name]])
    predictions = model.predict([customer_encoded[:,0], customer_encoded[:,1], customer_encoded[:,2]])
    product_names = y.unique()
    sorted_indices = (-predictions).argsort()[0][:num_recommendations]
    top_product_names = [product_names[i] for i in sorted_indices]
    return top_product_names    