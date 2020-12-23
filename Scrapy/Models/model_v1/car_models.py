import pandas as pd 
import numpy as np 

models = pd.read_csv('models.csv')
df = pd.DataFrame(models)
df = df.drop_duplicates(subset="model")
df = df.dropna() 
df[['brand', 'model_type']] = df['model'].str.split(' ', 1, expand=True)
df = df[['brand', 'model']]

# df[['brand','models']] = df.model.str.split(" ",expand = True)
df.to_csv('car_models.csv')
print(df)