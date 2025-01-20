import pandas as pd

class AdAnalyse:
    def __init__(self, data):
        self.df = pd.DataFrame(data)

    def process_data(self):
        # Ensure necessary columns are present
        required_columns = ['ad_id', 'ad_name', 'status', 'effective_status', 'created_time', 'updated_time']
        for column in required_columns:
            if column not in self.df.columns:
                print(f"Warning: Missing column: {column}")
        
        # Convert 'created_time' and 'updated_time' to datetime
        self.df['created_time'] = pd.to_datetime(self.df['created_time'])
        self.df['updated_time'] = pd.to_datetime(self.df['updated_time'])
        
        # Convert to UTC (or any other desired timezone) if already tz-aware
        if self.df['created_time'].dt.tz is not None:
            self.df['created_time'] = self.df['created_time'].dt.tz_convert('UTC')
        if self.df['updated_time'].dt.tz is not None:
            self.df['updated_time'] = self.df['updated_time'].dt.tz_convert('UTC')
        
        return self.df

    def comparative_analysis(self):
        analysis = []
        
        for index, row in self.df.iterrows():
            ad_status = row['status']
            effective_status = row['effective_status']
            created_time = row['created_time']
            updated_time = row['updated_time']
            creative_name = row['creative_name']
            image_url = row['image_url']
            video_id = row['video_id']
            ad_name = row['ad_name']
            
            # Create a summary for the ad's status
            status_comparison = f"Ad Status: {ad_status}, Effective Status: {effective_status}"
            
            # Create a comparison based on the creation and update times
            time_comparison = f"Created on: {created_time}, Updated on: {updated_time}"
            
            # Add information about the creative (name and media type)
            creative_comparison = f"Creative Name: {creative_name}, Image URL: {image_url}, Video ID: {video_id if video_id != 'No Video ID' else 'No video'}"
            
            # Combine all the details
            analysis.append({
                'ad_id': row['ad_id'],
                'ad_name': ad_name,
                'status_comparison': status_comparison,
                'time_comparison': time_comparison,
                'creative_comparison': creative_comparison
            })

        # Convert the analysis result into a DataFrame for easier viewing
        analysis_df = pd.DataFrame(analysis)
        # print("\nComparative Analysis:")
        # print(analysis_df)

        return analysis_df

