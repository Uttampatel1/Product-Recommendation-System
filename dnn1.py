import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from tensorflow import keras

def are_ind(AreaName,IndustryName):
    
    data = pd.read_csv('data/final.csv')
    model = keras.models.load_model('models/softmax.h5')
    # Perform any necessary data cleaning and preprocessing here

    # Step 2: Encode categorical variables
    cat_vars = ['AreaName', 'IndustryName','ProductName']
    label_encoders = {}
    for var in cat_vars:
        label_encoders[var] = LabelEncoder()
        data[var] = label_encoders[var].fit_transform(data[var])
    print("####################################################################")
    num_features = 2
    # Step 7: Model Prediction
    # Assuming you have new customer data in a variable called 'new_data'
    new_data = np.array([[str(AreaName), str(IndustryName)]])  # Replace with actual new data

    # Preprocess the new data
    new_data_encoded = np.zeros((new_data.shape[0], num_features))
    for i, var in enumerate(cat_vars[:2]):
        new_data_encoded[:, i] = label_encoders[var].transform(new_data[:, i])

    # Make predictions
    predictions = model.predict(new_data_encoded)

    # Get the top 10 recommended products
    top_10_indices = np.argsort(predictions, axis=1)[:, -10:]  # Indices of top 10 products for each customer
    top_10_products = label_encoders['ProductName'].inverse_transform(top_10_indices.flatten())
    top_10_products = top_10_products.reshape((-1, 10))

    return top_10_products[0]
