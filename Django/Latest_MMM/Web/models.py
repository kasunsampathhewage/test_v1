from django.db import models
import pandas as pd
import csv
from sort_dataframeby_monthorweek import *

# Create your models here.


def cd_year():
        df1 = pd.read_csv(r'E:\DatasetV7.csv')
        df1['date'] = pd.to_datetime(df1['date'])
        df1 = df1.sort_values(['year'])
        ylist = df1['year'].unique()
        years = ylist.tolist()
        return years

def cd_month():
        df2 = pd.read_csv(r'E:\DatasetV7.csv')
        df2['date'] = pd.to_datetime(df2['date'])
        # df1 = df1.sort_values(['year'])
        mlist = df2['month'].unique()
        months = mlist.tolist()
        return months

def cd_bigc():
        df3 = pd.read_csv(r'E:\DatasetV7.csv')
        df3['date'] = pd.to_datetime(df3['date'])
        clist = df3['bigc'].unique()
        bigcs =  clist.tolist()
        return bigcs

def cd_brands():
        df4 = pd.read_csv(r'E:\DatasetV7.csv')
        df4['date'] = pd.to_datetime(df4['date'])
        blist = df4['Brand_name'].unique()
        brands =  blist.tolist()
        return brands

def cd_FoodBrands():
        df4 = pd.read_csv(r'E:\DatasetV7.csv')
        df4['date'] = pd.to_datetime(df4['date'])
        df4 = df4[(df4.bigc == 'Foods')]
        FoodBrandslist = df4['Brand_name'].unique()
        FoodBrands =  FoodBrandslist.tolist()
        return FoodBrands

def cd_BeveragesBrands():
        df4 = pd.read_csv(r'E:\DatasetV7.csv')
        df4['date'] = pd.to_datetime(df4['date'])
        df4 = df4[(df4.bigc == 'Beverages')]
        BeveragesBrandslist = df4['Brand_name'].unique()
        BeveragesBrands =  BeveragesBrandslist.tolist()
        return BeveragesBrands

def cd_HomeProductsBrands():
        df4 = pd.read_csv(r'E:\DatasetV7.csv')
        df4['date'] = pd.to_datetime(df4['date'])
        df4 = df4[(df4.bigc == 'Home Products')]
        HomeProductsBrandslist = df4['Brand_name'].unique()
        HomeProductsBrands =  HomeProductsBrandslist.tolist()
        return HomeProductsBrands

def cd_SelfCareBrands():
        df4 = pd.read_csv(r'E:\DatasetV7.csv')
        df4['date'] = pd.to_datetime(df4['date'])
        df4 = df4[(df4.bigc == 'Self Care')]
        SelfCareBrandslist = df4['Brand_name'].unique()
        SelfCareBrands =  SelfCareBrandslist.tolist()
        return SelfCareBrands

def chart1():
        chart1 = pd.read_csv(r'E:\DatasetV7.csv')
        # chart1 = chart1.groupby(['year','month','bigc','Brand_name'], as_index=False).agg({"Sales": "sum"})
        chart1 = chart1.groupby(['year'], as_index=False).agg({"Sales": "sum"})
        return chart1

def SummarydataframeCreation():
        df = pd.read_csv(r'E:\DatasetV7.csv')
        df['date'] = pd.to_datetime(df['date'])
        df['year'] = df['year'].astype(str)
        df = Sort_Dataframeby_Month(df=df, monthcolumnname='month')
        return df
