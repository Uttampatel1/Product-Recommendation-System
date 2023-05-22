import pandas as pd
import numpy as np
from scipy.sparse.linalg import svds
from scipy.sparse import csr_matrix

# Load the dataset
df = pd.read_csv('data/customer_data.csv',names = ['CustomerId','CustomerCode','CustomerName','AreaName','IndustryName','OrderNumber','OrderDate','ProductCode','ProductName','Length'],header=None)

# Add a PurchaseCount column and set its value to 1 for each row
df["PurchaseCount"] = 1

# Create a pivot table to represent customer-product purchase history
pivoted_df = pd.pivot_table(df, values='PurchaseCount', index='CustomerId', columns='ProductCode')

# Fill missing values with zeros
pivoted_df = pivoted_df.fillna(0)

# Normalize the pivot table by subtracting the mean purchase count
pivoted_df_mean = np.mean(pivoted_df, axis=1)
pivoted_df_norm = pivoted_df - pivoted_df_mean.values.reshape(-1, 1)

# Convert the pivot table to a sparse matrix
pivoted_df_norm_sparse = csr_matrix(pivoted_df_norm.values)

# Perform Singular Value Decomposition (SVD) on the normalized pivot table
U, sigma, Vt = svds(pivoted_df_norm_sparse, k=50)

# Convert the diagonal matrix of singular values to a diagonal matrix
sigma_diag_matrix = np.diag(sigma)

# Reconstruct the purchase history matrix using the SVD components
all_user_predicted_purchase_counts = np.dot(np.dot(U, sigma_diag_matrix), Vt) + pivoted_df_mean.values.reshape(-1, 1)

# Convert the reconstructed matrix to a dataframe
preds_df = pd.DataFrame(all_user_predicted_purchase_counts, columns = pivoted_df.columns)

# Define a function to recommend products to a given customer based on their purchase history
def recommend_products(customer_id, num_recommendations=10):
    # Sort the predicted purchase counts of the given customer's historical purchases
    sorted_customer_purchase_counts = preds_df.loc[customer_id].sort_values(ascending=False)
    # Get the top recommended products that the customer has not purchased before
    recommended_products = sorted_customer_purchase_counts[~sorted_customer_purchase_counts.index.isin(pivoted_df.loc[customer_id].index)].index[:num_recommendations]
    return recommended_products
