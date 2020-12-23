import pandas as pd 
import numpy as np

df = pd.read_csv('jobs.csv')
df = pd.DataFrame(df)
df['link']  = df['link'].astype(str) 
# df['link'] = df['link'].str.replace("'../","")
# df['link'] = df['link'].str.replace("JavaScript:openSizeWindow('..","https://www.topjobs.lk")
df[['link','links']] = df.link.str.split("(", n = 1, expand = True) 
df['links'] = df['links'].str.replace("'../","https://www.topjobs.lk/")
df['links'] = df['links'].str.replace(")","")
print(df['links'])

df.to_csv('jobs_v1.csv')