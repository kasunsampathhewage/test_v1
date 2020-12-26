
import pandas as pd 

target_csv = '/app/Banking_churn_prediction.csv'

df = pd.read_csv(target_csv)

print(df.head())