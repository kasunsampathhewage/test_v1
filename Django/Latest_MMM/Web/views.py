from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import pandas as pd
import numpy as np
from datetime import datetime
from sorted_months_weekdays import *
from sort_dataframeby_monthorweek import *
from .models import *
import calendar
from .predict import *


# Create your views here.
def indexpage(request):

    years = cd_year()
    months = cd_month()
    bigcs = cd_bigc()
    
    #get values from filter
    yearf = request.POST.get('year')
    monthf = request.POST.get('month')
    bigcf = request.POST.get('bigc')

    # filter data frame
    if request.method == "POST":
        df = SummarydataframeCreation()
        df1 = df[(df.bigc == bigcf)&(df.year == yearf)]
        df1_1 =  df[(df.bigc == bigcf)&(df.year == yearf)&(df.month == monthf)]
    else:
        df = SummarydataframeCreation()
        df = df.sort_values(by='date') 
        a = df['year'].iloc[-1]
        b = df['month'].iloc[-1]
        df1 = df[(df.year == a)]
        df1_1 =  df[(df.year == a)&(df.month == b)]
 
    # Monthly sales chart1
    df2 = df1.groupby('month', as_index=False).agg({"Sales": "sum"})
    df2 = Sort_Dataframeby_Month(df=df2, monthcolumnname='month')
    Sale_Date = df2['month'].values.tolist()
    Sale_Amount = df2['Sales'].values.tolist()
      
    # monthly investment chart2
    df4 = df1[['month', 'date', 'Consumer_Promotion', 'AandP', 'Trade_Promotion', 'JBP', 'Distributor_Margins',
             'Loyalty_Schemes', 'Other', 'Video', 'Search_Only', 'Display_Only', 'facebook', 'instagram', 'messenger']]
    df4 = pd.melt(df4, id_vars=['date', 'month'], var_name='Investment_Types', value_name='value')
    df4 = df4.groupby(['month','date'])['value'].sum().reset_index()
    df4 = Sort_Dataframeby_Month(df=df4, monthcolumnname='month')
    investment_month = df4['month'].values.tolist()
    investment_Amount = df4['value'].values.tolist()

    # investment for promotion type chart3
    df5 = df1[['month', 'date', 'Consumer_Promotion', 'AandP', 'Trade_Promotion', 'JBP', 'Distributor_Margins',
             'Loyalty_Schemes', 'Other', 'Video', 'Search_Only', 'Display_Only', 'facebook', 'instagram', 'messenger']]
    df5 = pd.melt(df5, id_vars=['date', 'month'], var_name='Investment_Types', value_name='value')
    df5 = df5.groupby(['month', 'Investment_Types'])['value'].sum().reset_index()
    df5 = Sort_Dataframeby_Month(df=df5, monthcolumnname='month')

    df5_1= df5[df5['Investment_Types'] == 'AandP']
    investment_Amount_A_P = df5_1['value'].values.tolist()
    investment_month_A_P = df5_1['month'].values.tolist()

    df5_2 = df5[df5['Investment_Types'] == 'Consumer_Promotion']
    investment_Amount_Consumer_Promotion = df5_2['value'].values.tolist()

    df5_3 = df5[df5['Investment_Types'] == 'Display_Only']
    investment_Amount_Display_Only = df5_3['value'].values.tolist()

    df5_4 = df5[df5['Investment_Types'] == 'Distributor_Margins']
    investment_Amount_Distributor_Margins = df5_4['value'].values.tolist()

    df5_5 = df5[df5['Investment_Types'] == 'JBP']
    investment_Amount_JBP = df5_5['value'].values.tolist()

    df5_6 = df5[df5['Investment_Types'] == 'Loyalty_Schemes']
    investment_Amount_Loyalty_Schemes = df5_6['value'].values.tolist()

    df5_7 = df5[df5['Investment_Types'] == 'Search_Only']
    investment_Amount_Search_Only = df5_7['value'].values.tolist()

    df5_8 = df5[df5['Investment_Types'] == 'Trade_Promotion']
    investment_Amount_Trade_Promotion = df5_8['value'].values.tolist()

    df5_9 = df5[df5['Investment_Types'] == 'Video']
    investment_Amount_Video = df5_9['value'].values.tolist()

    df5_10 = df5[df5['Investment_Types'] == 'facebook']
    investment_Amount_facebook = df5_10['value'].values.tolist()

    df5_11 = df5[df5['Investment_Types'] == 'instagram']
    investment_Amount_instagram = df5_11['value'].values.tolist()

    df5_12 = df5[df5['Investment_Types'] == 'messenger']
    investment_Amount_messenger = df5_12['value'].values.tolist()

    # Total investment for thr year chart4    
    if request.method == "POST":
        df7 = df1.groupby(['date','month','bigc'])['Sales','Consumer_Promotion', 'AandP', 'Trade_Promotion', 'JBP', 'Distributor_Margins','Loyalty_Schemes', 'Other', 'Video', 'Search_Only', 'Display_Only', 'facebook', 'instagram', 'messenger'].sum().reset_index()
        df8 = df7[['month', 'date','bigc','Sales', 'Consumer_Promotion', 'AandP', 'Trade_Promotion', 'JBP', 'Distributor_Margins',
                'Loyalty_Schemes', 'Other', 'Video', 'Search_Only', 'Display_Only', 'facebook', 'instagram', 'messenger']]
        df8 = pd.melt(df8, id_vars=['date', 'month','Sales','bigc'], var_name='Investment_Types', value_name='value')
        df8 = df8.groupby(['date','month','bigc','Sales'])['value'].sum().reset_index()
        
        df8['ROI'] = df8['Sales']/(df8['value'])
        ROI_value = df8['ROI'].values.tolist()
        ROI_month = df8['month'].values.tolist()

    else:
        df7 = df1.groupby(['date','month'])['Sales','Consumer_Promotion', 'AandP', 'Trade_Promotion', 'JBP', 'Distributor_Margins','Loyalty_Schemes', 'Other', 'Video', 'Search_Only', 'Display_Only', 'facebook', 'instagram', 'messenger'].sum().reset_index()
        df8 = df7[['month', 'date','Sales', 'Consumer_Promotion', 'AandP', 'Trade_Promotion', 'JBP', 'Distributor_Margins',
                'Loyalty_Schemes', 'Other', 'Video', 'Search_Only', 'Display_Only', 'facebook', 'instagram', 'messenger']]
        df8 = pd.melt(df8, id_vars=['date', 'month','Sales'], var_name='Investment_Types', value_name='value')
        df8 = df8.groupby(['date','month','Sales'])['value'].sum().reset_index()
        
        df8['ROI'] = df8['Sales']/(df8['value'])
        ROI_value = df8['ROI'].values.tolist()
        ROI_month = df8['month'].values.tolist()
   
    # ROI for promotion types  chart5
    if request.method == "POST":
        df13 = df1_1.groupby(['year','month','bigc'])['Sales','Consumer_Promotion', 'AandP', 'Trade_Promotion', 'JBP', 'Distributor_Margins','Loyalty_Schemes', 'Other', 'Video', 'Search_Only', 'Display_Only', 'facebook', 'instagram', 'messenger'].sum().reset_index()
        df13 = df13[['month', 'year','bigc','Sales', 'Consumer_Promotion', 'AandP', 'Trade_Promotion', 'JBP', 'Distributor_Margins',
                    'Loyalty_Schemes', 'Other', 'Video', 'Search_Only', 'Display_Only', 'facebook', 'instagram', 'messenger']]
        df13 = pd.melt(df13, id_vars=['year', 'month','Sales','bigc'], var_name='Investment_Types', value_name='value')
        df13=df13[df13!=0].dropna()
        df13['ROI'] = df13['Sales']/(df13['value'])
        ROI_Investment_value = df13['ROI'].values.tolist()
        ROI_Investment_Types = df13['Investment_Types'].values.tolist()

    else:
        df13 = df1_1.groupby(['date','month'])['Sales','Consumer_Promotion', 'AandP', 'Trade_Promotion', 'JBP', 'Distributor_Margins','Loyalty_Schemes', 'Other', 'Video', 'Search_Only', 'Display_Only', 'facebook', 'instagram', 'messenger'].sum().reset_index()
        df13 = df13[['month', 'date','Sales', 'Consumer_Promotion', 'AandP', 'Trade_Promotion', 'JBP', 'Distributor_Margins',
                'Loyalty_Schemes', 'Other', 'Video', 'Search_Only', 'Display_Only', 'facebook', 'instagram', 'messenger']]
        df13 = pd.melt(df13, id_vars=['date', 'month','Sales'], var_name='Investment_Types', value_name='value')
        df13=df13[df13!=0].dropna()
        df13['ROI'] = df13['Sales']/(df13['value'])
        ROI_Investment_value = df13['ROI'].values.tolist()
        ROI_Investment_Types = df13['Investment_Types'].values.tolist()
        
    
    # get values for cart1 (Total sales)
    total_sales_cart = df1_1['Sales'].sum()/1000000
    total_sales_cart = round(total_sales_cart, 2)
    
    # get values for cart2 (Total investments)
    df3_1 = df1_1[['date', 'Consumer_Promotion', 'AandP', 'Trade_Promotion', 'JBP', 'Distributor_Margins', 'Loyalty_Schemes',
             'Other', 'Video', 'Search_Only', 'Display_Only', 'facebook', 'instagram', 'messenger']]
    df3_1 = pd.melt(df3_1, id_vars=['date'], var_name='Investment_Types', value_name='value')
    df3_1 = df3_1.groupby(['date'])['value'].sum().reset_index()
    df3_1['Date'] = pd.to_datetime(df3_1['date'])
    investment_Amount_cart = df3_1['value'].sum()/1000000
    investment_Amount_cart=round(investment_Amount_cart, 2)

    #get values for cart3 (Sales/investments)
    if request.method == "POST":
        df7_1 = df1_1.groupby(['date','month','bigc'])['Sales','Consumer_Promotion', 'AandP', 'Trade_Promotion', 'JBP', 'Distributor_Margins','Loyalty_Schemes', 'Other', 'Video', 'Search_Only', 'Display_Only', 'facebook', 'instagram', 'messenger'].sum().reset_index()
        df8_1 = df7_1[['month', 'date','bigc','Sales', 'Consumer_Promotion', 'AandP', 'Trade_Promotion', 'JBP', 'Distributor_Margins',
                'Loyalty_Schemes', 'Other', 'Video', 'Search_Only', 'Display_Only', 'facebook', 'instagram', 'messenger']]
        df8_1 = pd.melt(df8_1, id_vars=['date', 'month','Sales','bigc'], var_name='Investment_Types', value_name='value')
        df8_1 = df8_1.groupby(['date','month','bigc','Sales'])['value'].sum().reset_index()
        df8_1['ROI'] = df8_1['Sales']/(df8_1['value'])
        ROI_value_cart = round(df8_1['ROI'].sum(),4)
    else:
        df7_1 = df1_1.groupby(['date','month'])['Sales','Consumer_Promotion', 'AandP', 'Trade_Promotion', 'JBP', 'Distributor_Margins','Loyalty_Schemes', 'Other', 'Video', 'Search_Only', 'Display_Only', 'facebook', 'instagram', 'messenger'].sum().reset_index()
        df8_1 = df7_1[['month', 'date','Sales', 'Consumer_Promotion', 'AandP', 'Trade_Promotion', 'JBP', 'Distributor_Margins',
                'Loyalty_Schemes', 'Other', 'Video', 'Search_Only', 'Display_Only', 'facebook', 'instagram', 'messenger']]
        df8_1 = pd.melt(df8_1, id_vars=['date', 'month','Sales'], var_name='Investment_Types', value_name='value')
        df8_1 = df8_1.groupby(['date','month','Sales'])['value'].sum().reset_index()
        df8_1['ROI'] = df8_1['Sales']/(df8_1['value'])
        ROI_value_cart = round(df8_1['ROI'].sum(),4)
    
    #pass variables to html pages
    context = {'yearf':yearf,'monthf':monthf,'bigcf':bigcf,'total_sales_cart': total_sales_cart, 'investment_Amount_cart':investment_Amount_cart
               ,'Sale_Date': Sale_Date, 'Sale_Amount': Sale_Amount,'years':years,'months':months,'bigcs':bigcs
               ,'investment_Amount':investment_Amount,'investment_month':investment_month
               ,'investment_Amount_A_P':investment_Amount_A_P,'investment_month_A_P':investment_month_A_P
               ,'investment_Amount_Consumer_Promotion':investment_Amount_Consumer_Promotion
               ,'investment_Amount_Display_Only':investment_Amount_Display_Only
               ,'investment_Amount_Distributor_Margins':investment_Amount_Distributor_Margins
               ,'investment_Amount_JBP':investment_Amount_JBP
               ,'investment_Amount_Loyalty_Schemes':investment_Amount_Loyalty_Schemes
               ,'investment_Amount_Search_Only':investment_Amount_Search_Only
               ,'investment_Amount_Trade_Promotion':investment_Amount_Trade_Promotion
               ,'investment_Amount_Video':investment_Amount_Video
               ,'investment_Amount_facebook':investment_Amount_facebook
               ,'investment_Amount_instagram':investment_Amount_instagram
               ,'investment_Amount_messenger':investment_Amount_messenger
               ,'investment_Amount_Consumer_Promotion':investment_Amount_Consumer_Promotion
               ,'ROI_value':ROI_value,'ROI_month':ROI_month,'ROI_value_cart':ROI_value_cart
               ,'ROI_Investment_value':ROI_Investment_value,'ROI_Investment_Types':ROI_Investment_Types
               
               }

    #get values for cart4 (Sales growth)
         #get previous month
    if request.method == "POST":
        current_month = list(calendar.month_abbr).index(monthf)
        previous_month = current_month-1
        previous_month_abb = calendar.month_abbr[previous_month]
        current_year = yearf

        if previous_month == 0:
            previous_month = 12
            previous_month_abb = calendar.month_abbr[previous_month]
            current_year = int(yearf)-1
            current_year = str(current_year)
            

        df_total_sales_for_previous_month = df[(df.bigc == bigcf)&(df.year == current_year)&(df.month == previous_month_abb)]
        previous_total_sales = df_total_sales_for_previous_month['Sales'].sum()/1000000
        sales_growth_cart = (total_sales_cart - previous_total_sales)/previous_total_sales*100
        sales_growth_cart = round(sales_growth_cart, 2)

        context.update({'sales_growth_cart': sales_growth_cart,'previous_month_abb':previous_month_abb })

    else:
        pass

    
    return render(request, 'home.html', context)

def brand(request):

    years = cd_year()
    months = cd_month()
    bigcs = cd_bigc()
    Fbrands = cd_FoodBrands()
    Bbrands = cd_BeveragesBrands()
    HCbrands = cd_HomeProductsBrands()
    SCbrands = cd_SelfCareBrands()
    
    
    #get values from filter
    yearf = request.POST.get('year')
    monthf = request.POST.get('month')
    bigcf = request.POST.get('bigc')
    branf = request.POST.get('brand')

    # filter data frame
    if request.method == "POST":
        df = SummarydataframeCreation()
        df1 = df[(df.bigc == bigcf)&(df.Brand_name == branf)&(df.year == yearf)]
        df1_1 =  df[(df.bigc == bigcf)&(df.Brand_name == branf)&(df.year == yearf)&(df.month == monthf)]

    else:
        df = SummarydataframeCreation()
        df = df.sort_values(by='date') 
        a = df['year'].iloc[-1]
        b = df['month'].iloc[-1]
        df1 = df[(df.year == a)]
        df1_1 =  df[(df.year == a)&(df.month == b)]

    # Monthly sales chart1
    df2 = df1.groupby('month', as_index=False).agg({"Sales": "sum"})
    df2 = Sort_Dataframeby_Month(df=df2, monthcolumnname='month')
    Sale_Date = df2['month'].values.tolist()
    Sale_Amount = df2['Sales'].values.tolist()

    # monthly investment chart2
    df4 = df1[['month', 'date', 'Consumer_Promotion', 'AandP', 'Trade_Promotion', 'JBP', 'Distributor_Margins',
             'Loyalty_Schemes', 'Other', 'Video', 'Search_Only', 'Display_Only', 'facebook', 'instagram', 'messenger']]
    df4 = pd.melt(df4, id_vars=['date', 'month'], var_name='Investment_Types', value_name='value')
    df4 = df4.groupby(['month','date'])['value'].sum().reset_index()
    df4 = Sort_Dataframeby_Month(df=df4, monthcolumnname='month')
    investment_month = df4['month'].values.tolist()
    investment_Amount = df4['value'].values.tolist()

    # investment for promotion type chart3
    df5 = df1[['month', 'date', 'Consumer_Promotion', 'AandP', 'Trade_Promotion', 'JBP', 'Distributor_Margins',
             'Loyalty_Schemes', 'Other', 'Video', 'Search_Only', 'Display_Only', 'facebook', 'instagram', 'messenger']]
    df5 = pd.melt(df5, id_vars=['date', 'month'], var_name='Investment_Types', value_name='value')
    df5 = df5.groupby(['month', 'Investment_Types'])['value'].sum().reset_index()
    df5 = Sort_Dataframeby_Month(df=df5, monthcolumnname='month')

    df5_1= df5[df5['Investment_Types'] == 'AandP']
    investment_Amount_A_P = df5_1['value'].values.tolist()
    investment_month_A_P = df5_1['month'].values.tolist()

    df5_2 = df5[df5['Investment_Types'] == 'Consumer_Promotion']
    investment_Amount_Consumer_Promotion = df5_2['value'].values.tolist()

    df5_3 = df5[df5['Investment_Types'] == 'Display_Only']
    investment_Amount_Display_Only = df5_3['value'].values.tolist()

    df5_4 = df5[df5['Investment_Types'] == 'Distributor_Margins']
    investment_Amount_Distributor_Margins = df5_4['value'].values.tolist()

    df5_5 = df5[df5['Investment_Types'] == 'JBP']
    investment_Amount_JBP = df5_5['value'].values.tolist()

    df5_6 = df5[df5['Investment_Types'] == 'Loyalty_Schemes']
    investment_Amount_Loyalty_Schemes = df5_6['value'].values.tolist()

    df5_7 = df5[df5['Investment_Types'] == 'Search_Only']
    investment_Amount_Search_Only = df5_7['value'].values.tolist()

    df5_8 = df5[df5['Investment_Types'] == 'Trade_Promotion']
    investment_Amount_Trade_Promotion = df5_8['value'].values.tolist()

    df5_9 = df5[df5['Investment_Types'] == 'Video']
    investment_Amount_Video = df5_9['value'].values.tolist()

    df5_10 = df5[df5['Investment_Types'] == 'facebook']
    investment_Amount_facebook = df5_10['value'].values.tolist()

    df5_11 = df5[df5['Investment_Types'] == 'instagram']
    investment_Amount_instagram = df5_11['value'].values.tolist()

    df5_12 = df5[df5['Investment_Types'] == 'messenger']
    investment_Amount_messenger = df5_12['value'].values.tolist()


    # Total sales/ total investments chart 4 
    if request.method == "POST":

        df6 = df1[['month', 'date','bigc','Sales', 'Consumer_Promotion', 'AandP', 'Trade_Promotion', 'JBP', 'Distributor_Margins',
                'Loyalty_Schemes', 'Other', 'Video', 'Search_Only', 'Display_Only', 'facebook', 'instagram', 'messenger']]
        df6 = pd.melt(df6, id_vars=['date', 'month','bigc','Sales'], var_name='Investment_Types', value_name='value')
        df6 = df6.groupby(['date','month','bigc','Sales'])['value'].sum().reset_index()
        df6['ROI'] = df6['Sales']/(df6['value'])
        ROI_value = df6['ROI'].values.tolist()
        ROI_month = df6['month'].values.tolist()
    
    else:
        
        df7 = df1.groupby(['date','month'])['Sales','Consumer_Promotion', 'AandP', 'Trade_Promotion', 'JBP', 'Distributor_Margins','Loyalty_Schemes', 'Other', 'Video', 'Search_Only', 'Display_Only', 'facebook', 'instagram', 'messenger'].sum().reset_index()
        df8 = df7[['month', 'date','Sales', 'Consumer_Promotion', 'AandP', 'Trade_Promotion', 'JBP', 'Distributor_Margins',
                'Loyalty_Schemes', 'Other', 'Video', 'Search_Only', 'Display_Only', 'facebook', 'instagram', 'messenger']]
        df8 = pd.melt(df8, id_vars=['date', 'month','Sales'], var_name='Investment_Types', value_name='value')
        df8 = df8.groupby(['date','month','Sales'])['value'].sum().reset_index()    
        df8['ROI'] = df8['Sales']/(df8['value'])
        ROI_value = df8['ROI'].values.tolist()
        ROI_month = df8['month'].values.tolist()
    

    # ROI for promotion types  chart5
    if request.method == "POST":
        df13 = df1_1.groupby(['year','month','Brand_name'])['Sales','Consumer_Promotion', 'AandP', 'Trade_Promotion', 'JBP', 'Distributor_Margins','Loyalty_Schemes', 'Other', 'Video', 'Search_Only', 'Display_Only', 'facebook', 'instagram', 'messenger'].sum().reset_index()
        df13 = df13[['month', 'year','Brand_name','Sales', 'Consumer_Promotion', 'AandP', 'Trade_Promotion', 'JBP', 'Distributor_Margins',
                    'Loyalty_Schemes', 'Other', 'Video', 'Search_Only', 'Display_Only', 'facebook', 'instagram', 'messenger']]
        df13 = pd.melt(df13, id_vars=['year', 'month','Sales','Brand_name'], var_name='Investment_Types', value_name='value')
        df13=df13[df13!=0].dropna()
        df13['ROI'] = df13['Sales']/(df13['value'])
        ROI_Investment_value = df13['ROI'].values.tolist()
        ROI_Investment_Types = df13['Investment_Types'].values.tolist()

    else:
        df13 = df1_1.groupby(['date','month'])['Sales','Consumer_Promotion', 'AandP', 'Trade_Promotion', 'JBP', 'Distributor_Margins','Loyalty_Schemes', 'Other', 'Video', 'Search_Only', 'Display_Only', 'facebook', 'instagram', 'messenger'].sum().reset_index()
        df13 = df13[['month', 'date','Sales', 'Consumer_Promotion', 'AandP', 'Trade_Promotion', 'JBP', 'Distributor_Margins',
                'Loyalty_Schemes', 'Other', 'Video', 'Search_Only', 'Display_Only', 'facebook', 'instagram', 'messenger']]
        df13 = pd.melt(df13, id_vars=['date', 'month','Sales'], var_name='Investment_Types', value_name='value')
        df13=df13[df13!=0].dropna()
        df13['ROI'] = df13['Sales']/(df13['value'])
        ROI_Investment_value = df13['ROI'].values.tolist()
        ROI_Investment_Types = df13['Investment_Types'].values.tolist()
        


    # ROI with contribution

    # NoMonths=3
    # bigcf ='Foods'
    # brandf ='Brd00001'
    

    # dfprep=DataPreprocessing(bigcf,brandf)
    # df2,seconddiff,finaldf=test2(dfprep)
    # results=VARmodel(df2)
    # dfe_forecast=forecastData(results,df2,NoMonths,dfprep)
    # invertsale1=invert_transformation(dfprep,df2,second_diff=seconddiff)
    # invertsale1=np.exp(invertsale1)
    # invertSale=invert_transformation(dfprep,dfe_forecast,second_diff=seconddiff)
    # invertSale=np.exp(invertSale) 
 
    # #invert sale has only forecast data
    # #finaldf has the actual data
    # #appending the both dataframes togather to chart 1
    # #takes only last 12 rows for the plot as in line 146
    # fulldfForecast1=finaldf.append(invertSale)

    # #keeping a copy for later purpose
    # fulldfForecast1_2=fulldfForecast1.copy()
    
    # fulldfForecast1['date'] = fulldfForecast1.index
    # fulldfForecast1['date']=fulldfForecast1['date'].dt.strftime('%Y/%b/%d')
    # fulldfForecast1['Sales2']=fulldfForecast1['Sales']
    # fulldfForecast1=fulldfForecast1.tail(12)

    # A=fulldfForecast1.iloc[:-NoMonths]
    # A['Date']=A.index
    # A['Date']=A['Date'].dt.strftime('%Y/%b/%d')

    # B=fulldfForecast1.tail(NoMonths)
    # B['Date']=B.index
    # B['Date']=B['Date'].dt.strftime('%Y/%b/%d')

    # Sale_Date = fulldfForecast1['date'].values.tolist()
    # Sale_Amount =fulldfForecast1['Sales'].values.tolist()
    # Sale_AmountP =fulldfForecast1['Sales2'].values.tolist()

    # Sale_Amount1 =A['Sales'].values.tolist()
    # Sale_Amount2 =B['Sales'].values.tolist()

    # Sale_Date1 = A['Date'].values.tolist()
    # Sale_Date2 = B['Date'].values.tolist()
    # #contribution chart 
    
    # x=fulldfForecast1_2.shape[0]
    # elasticity=impulseResponse(results,x,fulldfForecast1_2)
    # contribution=Contribution(elasticity,fulldfForecast1_2)
    # contribution2=contribution.copy()
    
    # df_tt=ROI(contribution2,elasticity,3,2019,"Jan")
    # Investment_type=df_tt['Investment Type'].values.tolist()
    # ROI1=df_tt['ROI'].values.tolist()






    # get values for cart1 (total sales)
    total_sales_cart = df1_1['Sales'].sum()/1000000
    total_sales_cart = round(total_sales_cart, 2)
    
    # get values for cart2 (total investment)
    df3_1 = df1_1[['date', 'Consumer_Promotion', 'AandP', 'Trade_Promotion', 'JBP', 'Distributor_Margins', 'Loyalty_Schemes',
             'Other', 'Video', 'Search_Only', 'Display_Only', 'facebook', 'instagram', 'messenger']]
    df3_1 = pd.melt(df3_1, id_vars=['date'], var_name='Investment_Types', value_name='value')
    df3_1 = df3_1.groupby(['date'])['value'].sum().reset_index()
    df3_1['Date'] = pd.to_datetime(df3_1['date'])
    investment_Amount_cart = df3_1['value'].sum()/1000000
    investment_Amount_cart=round(investment_Amount_cart, 2)

    #get values for cart3 (total sales/ total investments)
    if request.method == "POST":

        df6_1 = df1_1[['month', 'date','bigc','Brand_name','Sales', 'Consumer_Promotion', 'AandP', 'Trade_Promotion', 'JBP', 'Distributor_Margins',
             'Loyalty_Schemes', 'Other', 'Video', 'Search_Only', 'Display_Only', 'facebook', 'instagram', 'messenger']]
        df6_1 = pd.melt(df6_1, id_vars=['date', 'month','bigc','Brand_name','Sales'], var_name='Investment_Types', value_name='value')
        df6_1 = df6_1.groupby(['date','month','bigc','Brand_name','Sales'])['value'].sum().reset_index()
        df6_1['ROI'] = df6_1['Sales']/(df6_1['value'])
        ROI_value_cart = round(df6_1['ROI'].sum(),4)
    else:
        
        df6_1 = df1_1.groupby(['date','month'])['Sales','Consumer_Promotion', 'AandP', 'Trade_Promotion', 'JBP', 'Distributor_Margins','Loyalty_Schemes', 'Other', 'Video', 'Search_Only', 'Display_Only', 'facebook', 'instagram', 'messenger'].sum().reset_index()
        df8_1 = df6_1[['month', 'date','Sales', 'Consumer_Promotion', 'AandP', 'Trade_Promotion', 'JBP', 'Distributor_Margins',
                'Loyalty_Schemes', 'Other', 'Video', 'Search_Only', 'Display_Only', 'facebook', 'instagram', 'messenger']]
        df8_1 = pd.melt(df8_1, id_vars=['date', 'month','Sales'], var_name='Investment_Types', value_name='value')
        df8_1 = df8_1.groupby(['date','month','Sales'])['value'].sum().reset_index()
        df8_1['ROI'] = df8_1['Sales']/(df8_1['value'])
        ROI_value_cart = round(df8_1['ROI'].sum(),4)
    

    context = {'years':years,'months':months,'bigcs':bigcs,
                'Fbrands':Fbrands,'Bbrands':Bbrands,'HCbrands':HCbrands,'SCbrands':SCbrands,
                'yearf':yearf, 'monthf':monthf,'bigcf':bigcf,'brandf':branf,
                'Sale_Date':Sale_Date ,'Sale_Amount':Sale_Amount,
                'investment_Amount':investment_Amount, 'investment_month':investment_month,
                'investment_Amount_A_P':investment_Amount_A_P,'investment_month_A_P':investment_month_A_P
                ,'investment_Amount_Consumer_Promotion':investment_Amount_Consumer_Promotion
                ,'investment_Amount_Display_Only':investment_Amount_Display_Only
                ,'investment_Amount_Distributor_Margins':investment_Amount_Distributor_Margins
                ,'investment_Amount_JBP':investment_Amount_JBP
                ,'investment_Amount_Loyalty_Schemes':investment_Amount_Loyalty_Schemes
                ,'investment_Amount_Search_Only':investment_Amount_Search_Only
                ,'investment_Amount_Trade_Promotion':investment_Amount_Trade_Promotion
                ,'investment_Amount_Video':investment_Amount_Video
                ,'investment_Amount_facebook':investment_Amount_facebook
                ,'investment_Amount_instagram':investment_Amount_instagram
                ,'investment_Amount_messenger':investment_Amount_messenger
                ,'investment_Amount_Consumer_Promotion':investment_Amount_Consumer_Promotion
                ,'total_sales_cart': total_sales_cart,'investment_Amount_cart':investment_Amount_cart,
                'ROI_value':ROI_value,'ROI_month':ROI_month, 'ROI_value_cart':ROI_value_cart
                ,'ROI_Investment_value':ROI_Investment_value,'ROI_Investment_Types':ROI_Investment_Types
                #  ,'Investment_type':Investment_type,'ROI1':ROI1
                }

    #get values for cart4 (sales growth)
    #get previous month
    if request.method == "POST":
        current_month = list(calendar.month_abbr).index(monthf)
        previous_month = current_month-1
        previous_month_abb = calendar.month_abbr[previous_month]
        current_year = yearf

        if previous_month == 0:
            previous_month = 12
            previous_month_abb = calendar.month_abbr[previous_month]
            current_year = int(yearf)-1
            current_year = str(current_year)
            
        df_total_sales_for_previous_month = df[(df.bigc == bigcf)&(df.Brand_name == branf)&(df.year == current_year)&(df.month == previous_month_abb)]
        previous_total_sales = df_total_sales_for_previous_month['Sales'].sum()/1000000
        sales_growth_cart = (total_sales_cart - previous_total_sales)/previous_total_sales *100
        sales_growth_cart = round(sales_growth_cart, 2)
     
        context.update({'sales_growth_cart': sales_growth_cart,'previous_month_abb':previous_month_abb })

    else:
        pass
    
    return render(request,'brand.html',context)

def predict(request):

    years = cd_year()
    months = cd_month()
    bigcs = cd_bigc()
    brands = cd_brands()
    Fbrands = cd_FoodBrands()
    Bbrands = cd_BeveragesBrands()
    HCbrands = cd_HomeProductsBrands()
    SCbrands = cd_SelfCareBrands()

    #get values from filter
    
    yearf = request.POST.get('year')
    monthf = request.POST.get('month')
    bigcf = request.POST.get('bigc')
    brandf = request.POST.get('brand')
    pyearf=request.POST.get('pyear')
    #slider1 = request.POST.get('range1')
    print("++++++++++++++++++++++Hello world+++++++++++++++++++++++++++++")
    print(bigcf)
  

    if request.method == "POST":
        NoMonths= int(pyearf)
    

    else:
        NoMonths=1
        bigcf ='Foods'
        brandf ='Brd00001'
    
    
    dfprep=DataPreprocessing(bigcf,brandf)
    df2,seconddiff,finaldf=test2(dfprep)
    results=VARmodel(df2)
    dfe_forecast=forecastData(results,df2,NoMonths,dfprep)
    invertsale1=invert_transformation(finaldf,df2,second_diff=seconddiff)
    invertsale1=np.exp(invertsale1)
    invertSale=invert_transformation(finaldf,dfe_forecast,second_diff=seconddiff)
    invertSale=np.exp(invertSale) 
 
    #invert sale has only forecast data
    #finaldf has the actual data
    #appending the both dataframes togather to chart 1
    #takes only last 12 rows for the plot as in line 146
    fulldfForecast1=finaldf.append(invertSale)
    print("Checking columns=========================")
    
    #keeping a copy for later purpose
    fulldfForecast1_2=fulldfForecast1.copy()
    print(fulldfForecast1_2.columns)
    
    fulldfForecast1['date'] = fulldfForecast1.index
    fulldfForecast1['date']=fulldfForecast1['date'].dt.strftime('%Y/%b/%d')
    fulldfForecast1['Sales2']=fulldfForecast1['Sales']
    fulldfForecast1=fulldfForecast1.tail(12)

    A=fulldfForecast1.iloc[:-NoMonths]
    A['Date']=A.index
    A['Date']=A['Date'].dt.strftime('%Y/%b/%d')

    B=fulldfForecast1.tail(NoMonths)
    B['Date']=B.index
    B['Date']=B['Date'].dt.strftime('%Y/%b/%d')

    Sale_Date = fulldfForecast1['date'].values.tolist()
    Sale_Amount =fulldfForecast1['Sales'].values.tolist()
    z=fulldfForecast1.Sales.tail(NoMonths)
    

    Sale_AmountP =fulldfForecast1['Sales2'].values.tolist()    
    #p1=Sale_AmountP[0]
    #p2=Sale_AmountP[1]
    #p3=Sale_AmountP[2]
    Sale_Amount1 =A['Sales'].values.tolist()
    Sale_Amount2 =B['Sales'].values.tolist()

    Sale_Date1 = A['Date'].values.tolist()
    Sale_Date2 = B['Date'].values.tolist()
    #contribution chart 
    
    x=fulldfForecast1_2.shape[0]
    elasticity=impulseResponse(results,x,fulldfForecast1_2)
    print("checking elasticity columns1------------")
    print(elasticity.columns)
    elasticity2=elasticity.copy()
    contribution=Contribution(elasticity,fulldfForecast1_2)
    contribution2=contribution.copy()
    
    contribution=contribution.tail(NoMonths)
    #tt=contributionVisual(contribution)

    #creating the columnlist
    #tl=tt.columns.tolist()
    #removewords=['Date_Contribution']
    #for word in list(removewords):  # iterating on a copy since removing will mess things up
     #   if word in removewords:
      #      tl.remove(word)
    #columnlist1=tl


    #tt['Month']=tt['Date_Contribution'].dt.month_name()
    #tt['Month1']=tt['Date_Contribution'].dt.strftime('%Y/%b/%d')
    
    #Month=tt['Month'].values.tolist()
    #Consumer_Promotion_Contribution=tt['Consumer_Promotion_Contribution'].values.tolist()
    #Trade_Promotion_Contribution=tt['Trade_Promotion_Contribution'].values.tolist()
    #AandP_Contribution=tt['AandP_Contribution'].values.tolist()
    #JBP_Contribution=tt['JBP_Contribution'].values.tolist()
    #Distributor_Margins_Contribution=tt['Distributor_Margins_Contribution'].values.tolist()
    #Loyalty_Schemes_Contribution=tt['Loyalty_Schemes_Contribution'].values.tolist()
    #Video_Contribution=tt['Video_Contribution'].values.tolist()
    #facebook_Contribution=tt['facebook_Contribution'].values.tolist()
   
    #instagram_Contribution=tt['instagram_Contribution'].values.tolist()
    #messenger_Contribution=tt['messenger_Contribution'].values.tolist()
  

    ########### Simulation#################
    #column list to show the slider bars
    tl2=elasticity.columns.tolist()
    tl2=[x for x in tl2 if x != "Sales"]
    columnlist2=tl2

    AandP =1 #request.POST.get('AandP')
    AndP1=request.POST.get('AandP_input')
    print("==========================================================================aaaaaaaaannnnnppppppp")
    print(AndP1)
    #AandP_input=int(AandP)
    Consumer_Promotion =1 #request.POST.get('customRange2')
    JBP =1 #request.POST.get('customRange4')
    facebook =1 #request.POST.get('customRange8')
    instagram =1 #request.POST.get('customRange9')
    video =1 #request.POST.get('customRange10')
    Search_Only=1#request.POST.get('customRange11')
    Display_Only=1#request.POST.get('customRange12')
    Distributor_Margins=1#request.POST.get('customRange6')
    Loyalty_Schemes=1#request.POST.get('customRange7')
    Trade_Promotion=1#request.POST.get('customRange5')
    messenger=1#request.POST.get('customRange13')
    li=['Consumer_Promotion', 'AandP', 'Trade_Promotion', 'JBP','Distributor_Margins', 'Loyalty_Schemes', 'Video', 'facebook','Search_Only', 'instagram', 'messenger', 'Display_Only']

    for i in elasticity.columns.values:
        for j in li:
            if i==j:
                li.remove(i)
    for col in li:
        elasticity[col]=0

  

    elasticity=elasticity.tail(3) 
    elasticity_T1=elasticity.head(1)

    elasticity_T1=elasticity_T1.reset_index()
    elasticity_T2=elasticity.iloc[1:]
    elasticity_T2=elasticity_T2.head(1)
    elasticity_T2=elasticity_T2.reset_index()
    elasticity_T3=elasticity.tail(1)
    elasticity_T3=elasticity_T3.reset_index()

    df=finaldf['Sales'].tail(1)
    Salestot=df.sum()
    #Salestot2=invertSale['Sales'].head(1).sum()
    #Salestot3=invertSale['Sales'].tail(1).sum()

    st1=abs(Salestot+elasticity_T1['Search_Only']*Search_Only+elasticity_T1['facebook']*facebook+elasticity_T1['instagram']*instagram+elasticity_T1['Display_Only']*Display_Only+elasticity_T1['Distributor_Margins']*Distributor_Margins+elasticity_T1['JBP']*JBP+elasticity_T1['Loyalty_Schemes']*Loyalty_Schemes+elasticity_T1['Trade_Promotion']*Trade_Promotion+elasticity_T1['Consumer_Promotion']*Consumer_Promotion+elasticity_T1['Video']*video+elasticity_T1['AandP']*AandP*1000+elasticity_T1['messenger']*messenger)
    st2=abs(st1+elasticity_T2['Search_Only']*Search_Only+elasticity_T2['facebook']*facebook+elasticity_T2['instagram']*instagram+elasticity_T2['Display_Only']*Display_Only+elasticity_T2['Distributor_Margins']*Distributor_Margins+elasticity_T2['JBP']*JBP+elasticity_T2['Loyalty_Schemes']*Loyalty_Schemes+elasticity_T2['Trade_Promotion']*Trade_Promotion+elasticity_T2['Consumer_Promotion']*Consumer_Promotion+elasticity_T2['Video']*video+elasticity_T2['AandP']*AandP*10000+elasticity_T2['messenger']*messenger)
    st3=abs(st2+elasticity_T3['Search_Only']*Search_Only+elasticity_T3['facebook']*facebook+elasticity_T3['instagram']*instagram+elasticity_T3['Display_Only']*Display_Only+elasticity_T3['Distributor_Margins']*Distributor_Margins+elasticity_T3['JBP']*JBP+elasticity_T3['Loyalty_Schemes']*Loyalty_Schemes+elasticity_T3['Trade_Promotion']*Trade_Promotion+elasticity_T3['Consumer_Promotion']*Consumer_Promotion+elasticity_T3['Video']*video+elasticity_T3['AandP']*AandP*10000+elasticity_T3['messenger']*messenger)

    dfT={'Sales':st1} 
    dfT=pd.DataFrame(dfT)
    dfT2={'Sales':st2}
    dfT2=pd.DataFrame(dfT2)
    dfT3={'Sales':st3}
    dfT3=pd.DataFrame(dfT3)
    
    a=NoMonths
    if a==1:
        r=dfT
    elif a==2:
        r=dfT.append(dfT2,ignore_index=True)
    elif a==3:
        r=dfT.append(dfT2,ignore_index=True)
        r=r.append(dfT3,ignore_index=True)
    

    rr=r['Sales'].tolist()
    df_forecast=pd.DataFrame(data=rr,index=dfe_forecast.tail(a).index,columns=r.columns)

    
    print(df_forecast)

    simulation=fulldfForecast1_2.tail(5).merge(df_forecast,how='left',left_index=True, right_index=True)[['Sales_pred','Sales']]
    simulation.Sales.fillna(simulation.Sales_pred,inplace=True)
    simulation['date'] = simulation.index
    simulation['date']=simulation['date'].dt.strftime('%Y/%b/%d')

    forecastsales=simulation['Sales_pred'].values.tolist()
    simulationSales=simulation['Sales'].values.tolist()
    simulationDate=simulation['date'].values.tolist()
   
    print("Checking shapes--------------------")
    print(contribution2.columns)
    print(elasticity.columns)
    df_tt=ROI(contribution2,elasticity2,3,2019,"Jan")
    Investment_type=df_tt['Investment Type'].values.tolist()
    ROI1=df_tt['ROI'].values.tolist()

    context= {'years':years,'months':months,'bigcs':bigcs,'brands':brands, 'Fbrands':Fbrands,'Bbrands':Bbrands,'HCbrands':HCbrands,'SCbrands':SCbrands,
              'yearf':yearf, 'monthf':monthf,'bigcf':bigcf,'brandf':brandf,'NoMonths':NoMonths,
              'Sale_Amount':Sale_Amount,'Sale_Date':Sale_Date,'columnlist2':columnlist2,
              'forecastsales':forecastsales,'simulationSales':simulationSales,'simulationDate':simulationDate,
            'Investment_type':Investment_type,'ROI1':ROI1,'Sale_Amount1':Sale_Amount1,'Sale_Amount2':Sale_Amount2,
            'Sale_Date1':Sale_Date1 ,'Sale_Date2':Sale_Date2,'Sale_AmountP':Sale_AmountP,'AndP1':AndP1
            }

    return render(request,'predict.html',context)

    


    
def comparision(request):

    years = cd_year()
    months = cd_month()
    bigcs = cd_bigc()
    Fbrands = cd_FoodBrands()
    Bbrands = cd_BeveragesBrands()
    HCbrands = cd_HomeProductsBrands()
    SCbrands = cd_SelfCareBrands()
    
    
    #get values from filter
    yearf = request.POST.get('year')
    monthf = request.POST.get('month')
    bigcf = request.POST.get('bigc')
    branf = request.POST.get('brand')

    # filter data frame
    if request.method == "POST":
        df = SummarydataframeCreation()
        # df1 = df[(df.year == yearf)&(df.bigc == bigcf)|(df.Brand_name == branf)]
        df1 = df[(df.year == yearf)&(df.bigc == bigcf)]
        df1_1 =  df[(df.year == yearf)&(df.month == monthf)&(df.bigc == bigcf)&(df.Brand_name == branf)]

    else:
        df = SummarydataframeCreation()
        df = df.sort_values(by='date') 
        a = df['year'].iloc[-1]
        b = df['month'].iloc[-1]
        df1 = df[(df.year == a)]
        df1_1 =  df[(df.year == a)&(df.month == b)]

    # Monthly sales chart1
    df2 = df1.groupby('month', as_index=False).agg({"Sales": "sum"})
    df2 = Sort_Dataframeby_Month(df=df2, monthcolumnname='month')
    Sale_Date = df2['month'].values.tolist()
    Sale_Amount = df2['Sales'].values.tolist()

    # monthly investment chart2
    df4 = df1[['month', 'date', 'Consumer_Promotion', 'AandP', 'Trade_Promotion', 'JBP', 'Distributor_Margins',
             'Loyalty_Schemes', 'Other', 'Video', 'Search_Only', 'Display_Only', 'facebook', 'instagram', 'messenger']]
    df4 = pd.melt(df4, id_vars=['date', 'month'], var_name='Investment_Types', value_name='value')
    df4 = df4.groupby(['month','date'])['value'].sum().reset_index()
    df4 = Sort_Dataframeby_Month(df=df4, monthcolumnname='month')
    investment_month = df4['month'].values.tolist()
    investment_Amount = df4['value'].values.tolist()

    # investment for promotion type chart3
    df5 = df1[['month', 'date', 'Consumer_Promotion', 'AandP', 'Trade_Promotion', 'JBP', 'Distributor_Margins',
             'Loyalty_Schemes', 'Other', 'Video', 'Search_Only', 'Display_Only', 'facebook', 'instagram', 'messenger']]
    df5 = pd.melt(df5, id_vars=['date', 'month'], var_name='Investment_Types', value_name='value')
    df5 = df5.groupby(['month', 'Investment_Types'])['value'].sum().reset_index()
    df5 = Sort_Dataframeby_Month(df=df5, monthcolumnname='month')

    df5_1= df5[df5['Investment_Types'] == 'AandP']
    investment_Amount_A_P = df5_1['value'].values.tolist()
    investment_month_A_P = df5_1['month'].values.tolist()

    df5_2 = df5[df5['Investment_Types'] == 'Consumer_Promotion']
    investment_Amount_Consumer_Promotion = df5_2['value'].values.tolist()

    df5_3 = df5[df5['Investment_Types'] == 'Display_Only']
    investment_Amount_Display_Only = df5_3['value'].values.tolist()

    df5_4 = df5[df5['Investment_Types'] == 'Distributor_Margins']
    investment_Amount_Distributor_Margins = df5_4['value'].values.tolist()

    df5_5 = df5[df5['Investment_Types'] == 'JBP']
    investment_Amount_JBP = df5_5['value'].values.tolist()

    df5_6 = df5[df5['Investment_Types'] == 'Loyalty_Schemes']
    investment_Amount_Loyalty_Schemes = df5_6['value'].values.tolist()

    df5_7 = df5[df5['Investment_Types'] == 'Search_Only']
    investment_Amount_Search_Only = df5_7['value'].values.tolist()

    df5_8 = df5[df5['Investment_Types'] == 'Trade_Promotion']
    investment_Amount_Trade_Promotion = df5_8['value'].values.tolist()

    df5_9 = df5[df5['Investment_Types'] == 'Video']
    investment_Amount_Video = df5_9['value'].values.tolist()

    df5_10 = df5[df5['Investment_Types'] == 'facebook']
    investment_Amount_facebook = df5_10['value'].values.tolist()

    df5_11 = df5[df5['Investment_Types'] == 'instagram']
    investment_Amount_instagram = df5_11['value'].values.tolist()

    df5_12 = df5[df5['Investment_Types'] == 'messenger']
    investment_Amount_messenger = df5_12['value'].values.tolist()


    # Total sales/ total investments chart 4 
    if request.method == "POST":

        df6 = df1[['month', 'date','bigc','Sales', 'Consumer_Promotion', 'AandP', 'Trade_Promotion', 'JBP', 'Distributor_Margins',
                'Loyalty_Schemes', 'Other', 'Video', 'Search_Only', 'Display_Only', 'facebook', 'instagram', 'messenger']]
        df6 = pd.melt(df6, id_vars=['date', 'month','bigc','Sales'], var_name='Investment_Types', value_name='value')
        df6 = df6.groupby(['date','month','bigc','Sales'])['value'].sum().reset_index()
        df6['ROI'] = df6['Sales']/(df6['value'])
        ROI_value = df6['ROI'].values.tolist()
        ROI_month = df6['month'].values.tolist()
    
    else:
        
        df7 = df1.groupby(['date','month'])['Sales','Consumer_Promotion', 'AandP', 'Trade_Promotion', 'JBP', 'Distributor_Margins','Loyalty_Schemes', 'Other', 'Video', 'Search_Only', 'Display_Only', 'facebook', 'instagram', 'messenger'].sum().reset_index()
        df8 = df7[['month', 'date','Sales', 'Consumer_Promotion', 'AandP', 'Trade_Promotion', 'JBP', 'Distributor_Margins',
                'Loyalty_Schemes', 'Other', 'Video', 'Search_Only', 'Display_Only', 'facebook', 'instagram', 'messenger']]
        df8 = pd.melt(df8, id_vars=['date', 'month','Sales'], var_name='Investment_Types', value_name='value')
        df8 = df8.groupby(['date','month','Sales'])['value'].sum().reset_index()    
        df8['ROI'] = df8['Sales']/(df8['value'])
        ROI_value = df8['ROI'].values.tolist()
        ROI_month = df8['month'].values.tolist()
    

    # ROI for promotion types  chart5
    if request.method == "POST":
        df13 = df1_1.groupby(['year','month','Brand_name'])['Sales','Consumer_Promotion', 'AandP', 'Trade_Promotion', 'JBP', 'Distributor_Margins','Loyalty_Schemes', 'Other', 'Video', 'Search_Only', 'Display_Only', 'facebook', 'instagram', 'messenger'].sum().reset_index()
        df13 = df13[['month', 'year','Brand_name','Sales', 'Consumer_Promotion', 'AandP', 'Trade_Promotion', 'JBP', 'Distributor_Margins',
                    'Loyalty_Schemes', 'Other', 'Video', 'Search_Only', 'Display_Only', 'facebook', 'instagram', 'messenger']]
        df13 = pd.melt(df13, id_vars=['year', 'month','Sales','Brand_name'], var_name='Investment_Types', value_name='value')
        df13=df13[df13!=0].dropna()
        df13['ROI'] = df13['Sales']/(df13['value'])
        ROI_Investment_value = df13['ROI'].values.tolist()
        ROI_Investment_Types = df13['Investment_Types'].values.tolist()

    else:
        df13 = df1_1.groupby(['date','month'])['Sales','Consumer_Promotion', 'AandP', 'Trade_Promotion', 'JBP', 'Distributor_Margins','Loyalty_Schemes', 'Other', 'Video', 'Search_Only', 'Display_Only', 'facebook', 'instagram', 'messenger'].sum().reset_index()
        df13 = df13[['month', 'date','Sales', 'Consumer_Promotion', 'AandP', 'Trade_Promotion', 'JBP', 'Distributor_Margins',
                'Loyalty_Schemes', 'Other', 'Video', 'Search_Only', 'Display_Only', 'facebook', 'instagram', 'messenger']]
        df13 = pd.melt(df13, id_vars=['date', 'month','Sales'], var_name='Investment_Types', value_name='value')
        df13=df13[df13!=0].dropna()
        df13['ROI'] = df13['Sales']/(df13['value'])
        ROI_Investment_value = df13['ROI'].values.tolist()
        ROI_Investment_Types = df13['Investment_Types'].values.tolist()
        


    # ROI with contribution

    # NoMonths=3
    # bigcf ='Foods'
    # brandf ='Brd00001'
    

    # dfprep=DataPreprocessing(bigcf,brandf)
    # df2,seconddiff,finaldf=test2(dfprep)
    # results=VARmodel(df2)
    # dfe_forecast=forecastData(results,df2,NoMonths,dfprep)
    # invertsale1=invert_transformation(dfprep,df2,second_diff=seconddiff)
    # invertsale1=np.exp(invertsale1)
    # invertSale=invert_transformation(dfprep,dfe_forecast,second_diff=seconddiff)
    # invertSale=np.exp(invertSale) 
 
    # #invert sale has only forecast data
    # #finaldf has the actual data
    # #appending the both dataframes togather to chart 1
    # #takes only last 12 rows for the plot as in line 146
    # fulldfForecast1=finaldf.append(invertSale)

    # #keeping a copy for later purpose
    # fulldfForecast1_2=fulldfForecast1.copy()
    
    # fulldfForecast1['date'] = fulldfForecast1.index
    # fulldfForecast1['date']=fulldfForecast1['date'].dt.strftime('%Y/%b/%d')
    # fulldfForecast1['Sales2']=fulldfForecast1['Sales']
    # fulldfForecast1=fulldfForecast1.tail(12)

    # A=fulldfForecast1.iloc[:-NoMonths]
    # A['Date']=A.index
    # A['Date']=A['Date'].dt.strftime('%Y/%b/%d')

    # B=fulldfForecast1.tail(NoMonths)
    # B['Date']=B.index
    # B['Date']=B['Date'].dt.strftime('%Y/%b/%d')

    # Sale_Date = fulldfForecast1['date'].values.tolist()
    # Sale_Amount =fulldfForecast1['Sales'].values.tolist()
    # Sale_AmountP =fulldfForecast1['Sales2'].values.tolist()

    # Sale_Amount1 =A['Sales'].values.tolist()
    # Sale_Amount2 =B['Sales'].values.tolist()

    # Sale_Date1 = A['Date'].values.tolist()
    # Sale_Date2 = B['Date'].values.tolist()
    # #contribution chart 
    
    # x=fulldfForecast1_2.shape[0]
    # elasticity=impulseResponse(results,x,fulldfForecast1_2)
    # contribution=Contribution(elasticity,fulldfForecast1_2)
    # contribution2=contribution.copy()
    
    # df_tt=ROI(contribution2,elasticity,3,2019,"Jan")
    # Investment_type=df_tt['Investment Type'].values.tolist()
    # ROI1=df_tt['ROI'].values.tolist()






    # get values for cart1 (total sales)
    total_sales_cart = df1_1['Sales'].sum()/1000000
    total_sales_cart = round(total_sales_cart, 2)
    
    # get values for cart2 (total investment)
    df3_1 = df1_1[['date', 'Consumer_Promotion', 'AandP', 'Trade_Promotion', 'JBP', 'Distributor_Margins', 'Loyalty_Schemes',
             'Other', 'Video', 'Search_Only', 'Display_Only', 'facebook', 'instagram', 'messenger']]
    df3_1 = pd.melt(df3_1, id_vars=['date'], var_name='Investment_Types', value_name='value')
    df3_1 = df3_1.groupby(['date'])['value'].sum().reset_index()
    df3_1['Date'] = pd.to_datetime(df3_1['date'])
    investment_Amount_cart = df3_1['value'].sum()/1000000
    investment_Amount_cart=round(investment_Amount_cart, 2)

    #get values for cart3 (total sales/ total investments)
    if request.method == "POST":

        df6_1 = df1_1[['month', 'date','bigc','Brand_name','Sales', 'Consumer_Promotion', 'AandP', 'Trade_Promotion', 'JBP', 'Distributor_Margins',
             'Loyalty_Schemes', 'Other', 'Video', 'Search_Only', 'Display_Only', 'facebook', 'instagram', 'messenger']]
        df6_1 = pd.melt(df6_1, id_vars=['date', 'month','bigc','Brand_name','Sales'], var_name='Investment_Types', value_name='value')
        df6_1 = df6_1.groupby(['date','month','bigc','Brand_name','Sales'])['value'].sum().reset_index()
        df6_1['ROI'] = df6_1['Sales']/(df6_1['value'])
        ROI_value_cart = round(df6_1['ROI'].sum(),4)
    else:
        
        df6_1 = df1_1.groupby(['date','month'])['Sales','Consumer_Promotion', 'AandP', 'Trade_Promotion', 'JBP', 'Distributor_Margins','Loyalty_Schemes', 'Other', 'Video', 'Search_Only', 'Display_Only', 'facebook', 'instagram', 'messenger'].sum().reset_index()
        df8_1 = df6_1[['month', 'date','Sales', 'Consumer_Promotion', 'AandP', 'Trade_Promotion', 'JBP', 'Distributor_Margins',
                'Loyalty_Schemes', 'Other', 'Video', 'Search_Only', 'Display_Only', 'facebook', 'instagram', 'messenger']]
        df8_1 = pd.melt(df8_1, id_vars=['date', 'month','Sales'], var_name='Investment_Types', value_name='value')
        df8_1 = df8_1.groupby(['date','month','Sales'])['value'].sum().reset_index()
        df8_1['ROI'] = df8_1['Sales']/(df8_1['value'])
        ROI_value_cart = round(df8_1['ROI'].sum(),4)
    

    context = {'years':years,'months':months,'bigcs':bigcs,
                'Fbrands':Fbrands,'Bbrands':Bbrands,'HCbrands':HCbrands,'SCbrands':SCbrands,
                'yearf':yearf, 'monthf':monthf,'bigcf':bigcf,'brandf':branf,
                'Sale_Date':Sale_Date ,'Sale_Amount':Sale_Amount,
                'investment_Amount':investment_Amount, 'investment_month':investment_month,
                'investment_Amount_A_P':investment_Amount_A_P,'investment_month_A_P':investment_month_A_P
                ,'investment_Amount_Consumer_Promotion':investment_Amount_Consumer_Promotion
                ,'investment_Amount_Display_Only':investment_Amount_Display_Only
                ,'investment_Amount_Distributor_Margins':investment_Amount_Distributor_Margins
                ,'investment_Amount_JBP':investment_Amount_JBP
                ,'investment_Amount_Loyalty_Schemes':investment_Amount_Loyalty_Schemes
                ,'investment_Amount_Search_Only':investment_Amount_Search_Only
                ,'investment_Amount_Trade_Promotion':investment_Amount_Trade_Promotion
                ,'investment_Amount_Video':investment_Amount_Video
                ,'investment_Amount_facebook':investment_Amount_facebook
                ,'investment_Amount_instagram':investment_Amount_instagram
                ,'investment_Amount_messenger':investment_Amount_messenger
                ,'investment_Amount_Consumer_Promotion':investment_Amount_Consumer_Promotion
                ,'total_sales_cart': total_sales_cart,'investment_Amount_cart':investment_Amount_cart,
                'ROI_value':ROI_value,'ROI_month':ROI_month, 'ROI_value_cart':ROI_value_cart
                ,'ROI_Investment_value':ROI_Investment_value,'ROI_Investment_Types':ROI_Investment_Types
                #  ,'Investment_type':Investment_type,'ROI1':ROI1
                }

    #get values for cart4 (sales growth)
    #get previous month
    if request.method == "POST":
        current_month = list(calendar.month_abbr).index(monthf)
        previous_month = current_month-1
        previous_month_abb = calendar.month_abbr[previous_month]
        current_year = yearf

        if previous_month == 0:
            previous_month = 12
            previous_month_abb = calendar.month_abbr[previous_month]
            current_year = int(yearf)-1
            current_year = str(current_year)
            
        df_total_sales_for_previous_month = df[(df.bigc == bigcf)&(df.Brand_name == branf)&(df.year == current_year)&(df.month == previous_month_abb)]
        previous_total_sales = df_total_sales_for_previous_month['Sales'].sum()/1000000
        sales_growth_cart = (total_sales_cart - previous_total_sales)/previous_total_sales *100
        sales_growth_cart = round(sales_growth_cart, 2)
     
        context.update({'sales_growth_cart': sales_growth_cart})

    else:
        pass
    
    return render(request,'comparision.html',context)

