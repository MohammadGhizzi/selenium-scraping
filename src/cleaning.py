import pandas as pd

# Read the scraped CSV file
df = pd.read_csv("/app/output/scraped_data.csv")

# Function to clean special characters from the data
def clean_data(df):
    # Replace special characters
    df.replace({'\*': '', ',': '', '"': '', '\'': ''}, regex=True, inplace=True)
    
    # Handle null values
    df.fillna("N/A", inplace=True)

    return df

# Clean the data
cleaned_df = clean_data(df)

# Save the cleaned data to a new CSV file
cleaned_df.to_csv("/app/output/cleaned_data.csv", index=False)

print("Data cleaning completed. Cleaned data saved to '/app/output/cleaned_data.csv'.")
