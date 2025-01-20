import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.cluster import KMeans, DBSCAN
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
class AdAnalyse:

    def __init__(self, data):
        self.data = data

    def peform_analysis(self):
        # Convert to DataFrame
        df = pd.DataFrame(self.data)

        # Convert created_time and updated_time to datetime format
        df['created_time'] = pd.to_datetime(df['created_time'])
        df['updated_time'] = pd.to_datetime(df['updated_time'])

        # Extract features from timestamps (e.g., year, month, day, etc.)
        df['created_year'] = df['created_time'].dt.year
        df['created_month'] = df['created_time'].dt.month
        df['created_day'] = df['created_time'].dt.day

        # One-hot encoding categorical variables (e.g., status, effective_status)
        encoder = OneHotEncoder(drop='first', sparse=False)
        encoded_status = encoder.fit_transform(df[['status', 'effective_status']])

        # Create a DataFrame for the encoded variables
        encoded_df = pd.DataFrame(encoded_status, columns=encoder.get_feature_names_out(['status', 'effective_status']))

        # Combine the original DataFrame with the encoded variables
        df = pd.concat([df, encoded_df], axis=1)

        # Drop non-numerical columns that aren't relevant to clustering (e.g., URLs, names)
        df.drop(columns=['ad_name', 'creative_name', 'image_url', 'video_id', 'thumbnail_url'], inplace=True)

        # Optional: Select numerical columns for clustering
        numerical_features = df.select_dtypes(include=np.number)

        # Ensure there are enough samples for clustering
        if len(df) >= 3:
            # Step 2: K-Means Clustering
            kmeans = KMeans(n_clusters=3, random_state=42)

            # Fit the model
            df['cluster_kmeans'] = kmeans.fit_predict(numerical_features)

            # Step 3: DBSCAN Clustering
            dbscan = DBSCAN(eps=0.5, min_samples=5)

            # Fit DBSCAN
            df['cluster_dbscan'] = dbscan.fit_predict(numerical_features)

            # Step 4: Evaluate the clustering
            silhouette_kmeans = silhouette_score(numerical_features, df['cluster_kmeans'])
            print(f'Silhouette Score (K-Means): {silhouette_kmeans}')
            
            # Only calculate silhouette score for DBSCAN if there are more than one cluster
            if len(np.unique(df['cluster_dbscan'])) > 1:
                silhouette_dbscan = silhouette_score(numerical_features, df['cluster_dbscan'])
                print(f'Silhouette Score (DBSCAN): {silhouette_dbscan}')
            else:
                print("Silhouette Score (DBSCAN): Not calculated due to only one cluster.")

            # Inspect clusters
            print(df[['ad_id', 'cluster_kmeans', 'cluster_dbscan']].head())

            # Step 5: PCA for Dimensionality Reduction and Visualization
            pca = PCA(n_components=2)  # Reducing to 2D for easy visualization
            pca_components = pca.fit_transform(numerical_features)

            # Create a DataFrame with PCA components and cluster labels
            pca_df = pd.DataFrame(pca_components, columns=['PCA1', 'PCA2'])
            pca_df['KMeans Cluster'] = df['cluster_kmeans']
            pca_df['DBSCAN Cluster'] = df['cluster_dbscan']

            # Visualize KMeans Clusters
            plt.figure(figsize=(8, 6))
            plt.scatter(pca_df['PCA1'], pca_df['PCA2'], c=pca_df['KMeans Cluster'], cmap='viridis', label='KMeans Clusters')
            plt.title('PCA - KMeans Clusters')
            plt.xlabel('PCA1')
            plt.ylabel('PCA2')
            plt.colorbar(label='Cluster')

            # Visualize DBSCAN Clusters
            plt.figure(figsize=(8, 6))
            plt.scatter(pca_df['PCA1'], pca_df['PCA2'], c=pca_df['DBSCAN Cluster'], cmap='plasma', label='DBSCAN Clusters')
            plt.title('PCA - DBSCAN Clusters')
            plt.xlabel('PCA1')
            plt.ylabel('PCA2')
            plt.colorbar(label='Cluster')
            plt.savefig("plt_image.png")
            plt.close()

        else:
            print("Insufficient samples for clustering.")
# if __name__ =="__main__":
#     data = [
#     {'ad_id': '23843668654810655', 'ad_name': 'Default name - Conversions', 'status': 'ACTIVE', 
#      'effective_status': 'ADSET_PAUSED', 'created_time': '2019-09-15T09:58:17+0200', 'updated_time': '2019-09-15T11:43:39+0200',
#      'creative_id': '23843668654990655', 'creative_name': 'Fasten Your Beans Belt 2019-09-15-07ce6c070d1a5363dfbb3814ace179f2', 
#      'image_url': 'https://scontent.fdac151-1.fna.fbcdn.net/v/t45.1600-4/70761056_23843668652360655_7645549778431901696_n.png?stp=dst-jpg_tt6&_nc_cat=106&ccb=1-7&_nc_sid=890911&_nc_ohc=T6ZJoFvcyWgQ7kNvgEaDEqf&_nc_zt=1&_nc_ht=scontent.fdac151-1.fna&edm=AAT1rw8EAAAA&_nc_gid=ArWoPOB9SkP0L9Y0B3bV6R1&oh=00_AYCTt5n15MjUNFdKrVQJDddGdGNjwRTxwXkOYxh8Xzz1ZA&oe=678EA0D9', 
#      'video_id': None, 'thumbnail_url': 'https://external.fdac151-1.fna.fbcdn.net/emg1/v/t13/1543504636695547862?url=https%3A%2F%2Fwww.facebook.com%2Fads%2Fimage%2F%3Fd%3DAQI-6cOmb-XGD3cUqL7Zhfflqa84GiFFHey4C3z-pz617-hDFUmXwxP0O5h_LzNlKhNaEnmbsGmw91UGzqTwgN2fKpJp7R6SPgjiFGjZ81x1rRD2sz36fYo5A-MpIxaVbBGp4r1erslU55LFE8lcSYpb&fb_obo=1&utld=facebook.com&stp=c0.5000x0.5000f_dst-emg0_p64x64_q75_tt6&ccb=13-1&oh=06_Q3992b1QV0wrn6mFztPMBXqaPv_WfhKI0j0tpnlbu_JwjCU&oe=678AAB04&_nc_sid=58080a'},

#      {'ad_id': '23843668654810655', 'ad_name': 'Default name - Conversions', 'status': 'ACTIVE', 
#      'effective_status': 'ADSET_PAUSED', 'created_time': '2019-09-15T09:58:17+0200', 'updated_time': '2019-09-15T11:43:39+0200',
#      'creative_id': '23843668654990655', 'creative_name': 'Fasten Your Beans Belt', 
#      'image_url': 'https://example.com/image1.jpg', 'video_id': None, 'thumbnail_url': 'https://example.com/thumb1.jpg'},
#     {'ad_id': '23843668654810656', 'ad_name': 'Another Ad', 'status': 'ACTIVE', 
#      'effective_status': 'ADSET_ACTIVE', 'created_time': '2020-09-15T09:58:17+0200', 'updated_time': '2020-09-15T11:43:39+0200',
#      'creative_id': '23843668654990656', 'creative_name': 'Fasten Your Beans Belt 2', 
#      'image_url': 'https://example.com/image2.jpg', 'video_id': None, 'thumbnail_url': 'https://example.com/thumb2.jpg'}
#     # Add more rows as needed
#     # Add more rows as needed
# ]
#     analyse = AdAnalyse(data)
#     analyse.peform_analysis()