import pandas as pd 
import numpy as np 

models = pd.read_csv('bike_models.csv')
df = pd.DataFrame(models)
df[['brand', 'model_type']] = df['model'].str.split(' ', 1, expand=True)
df = df[['brand', 'model']]

# df[['brand','models']] = df.model.str.split(" ",expand = True)
df.to_csv('bike_models_v1.csv')
print(df)