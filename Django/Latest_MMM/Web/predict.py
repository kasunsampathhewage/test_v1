import pandas as pd
import numpy as np
from numpy import sqrt,log,diff,mean
import datetime as dt
import joblib

import importlib

from statsmodels.tsa.api import VAR
from statsmodels.tsa.stattools import adfuller
from pandas.core.common import SettingWithCopyWarning

import warnings
warnings.filterwarnings("ignore", category=SettingWithCopyWarning)


def getBigcAndBrand(bigcValue=None,brandValue=None):
    
    dataset = pd.read_csv(r"C:\Users\Methma-Zkewed\Desktop\MMM dataset\MMM V2\DatasetV6.csv")
    dataset.drop('Unnamed: 0', inplace=True, axis=1)
    dataset['date'].apply(pd.to_datetime)
    dataset.fillna(dataset.mean())
    
    if((brandValue is None) and (bigcValue is None)):
        dataset = dataset.reset_index()
        return (dataset)
    
    elif((brandValue is not None) and (bigcValue is None)):
        brandDF = dataset.set_index("Brand_name")
        brandDF = brandDF.loc[brandValue]
        return (brandDF)
    
    elif((brandValue is None) and (bigcValue is not None)):
        bigcDF = dataset.set_index("bigc")
        bigcDF = bigcDF.loc[bigcValue]
        return (bigcDF)
    
    elif((brandValue is not None) and (bigcValue is not None)):
        bigcDF = dataset.set_index("bigc")
        bigcDF = bigcDF.loc[bigcValue]
        brandDF = bigcDF.reset_index()
        BothDf = brandDF.set_index("Brand_name")
        BothDf = BothDf.loc[brandValue]
        return (BothDf)

def DataPreprocessing(bigc,brand):
    print(bigc)
    print(brand)
    df = getBigcAndBrand(bigc,brand)
    print(df.columns)
    #df['date'].apply(pd.to_datetime)
    #df['Year'] = pd.DatetimeIndex(df['date']).year
    #df['Month'] = pd.DatetimeIndex(df['date']).month
    df['date']=pd.to_datetime(df['date'],format='%m/%d/%Y')
    df=df.set_index(df['date'])
    df=df.sort_index()
    #print("mean1 is")
    #mean1=df.mean
    #print(mean1)
    df2 = df[['Sales', 'Consumer_Promotion', 'AandP',
       'Trade_Promotion', 'JBP', 'Distributor_Margins', 'Loyalty_Schemes',
        'Video', 'facebook', 'Search_Only', 'instagram', 'messenger','Display_Only']]
    li1=[]
    for cols in df2:
        if df2[cols].sum()==0:
            li1.append(cols)

    print(li1)
    df2=df2.drop([x for x in li1],axis=1)
    print("++++++++++++++++++++++++++++++++++++++++++++++++")
    #df3 = df.fillna(df.mean())
    df3=df2.mask(df2==0).fillna(df2.mean())
    #df3 = df[['Year', 'Month']].astype(int).astype(str)
    #NewDate = df3["Year"] + "M" + df3["Month"]
    #from statsmodels.tsa.base.datetools import dates_from_str
    #NewDate = dates_from_str(NewDate)
    
    df3.to_csv(r'C:\Users\Methma-Zkewed\Desktop\MMM dataset\MMM V2\testdf22.csv')
    
    return df3



def adfuller_test(series, signif=0.05, name='', verbose=False):
    """Perform ADFuller to test for Stationarity of given series and print report"""
    r = adfuller(series, autolag='AIC')
    output = {'test_statistic':round(r[0], 4), 'pvalue':round(r[1], 4), 'n_lags':round(r[2], 4), 'n_obs':r[3]}
    p_value = output['pvalue'] 
    def adjust(val, length= 6): return str(val).ljust(length)

    # Print Summary
   # print(f'    Augmented Dickey-Fuller Test on "{name}"', "\n   ", '-'*47)
   # print(f' Null Hypothesis: Data has unit root. Non-Stationary.')
   # print(f' Significance Level    = {signif}')
   # print(f' Test Statistic        = {output["test_statistic"]}')
   # print(f' No. Lags Chosen       = {output["n_lags"]}')

     
    for key,val in r[4].items():
        print(f' Critical value {adjust(key)} = {round(val, 3)}')
    
    if p_value <= signif:
        #print(f" => P-Value = {p_value}. Rejecting Null Hypothesis.")
        #print(f" => Series is Stationary.")
        string=name+" Series is Stationary."
    else:
        #print(f" => P-Value = {p_value}. Weak evidence to reject the Null Hypothesis.")
        #print(f" => Series is Non-Stationary.")
        string=name+" Series is Non-Stationary."
    
    return string

def first_diff(df):  
    #takes the log and do the differencing to the training data set.
    #returns the log diffed training data set. This is used to train the model
    #input parameter df means the df_train returned from preprocessing() function above
    
    X_train_log = np.log(df)
    df_differenced = X_train_log.diff().dropna()
    return df_differenced


def testADF(df_train):
    
   # df_train = dataSplit()
    p=[]
    for name,column in df_train.iteritems():
        string=adfuller_test(column, name=column.name)
    
        print('\n')
        print(string)
        t=p.append(string)
        print(p)
    return p

def stationary(r):
    Stationary1df=pd.DataFrame(r,columns={'name'})
    new= Stationary1df["name"].str.split(" ", n = 3, expand = True)
    Stationary1df['feature']=new[0]
    Stationary1df['stationarity']=new[3]
    
    return Stationary1df

def test2 (data):
    print("++++++++++++++++++DAta+++++++++")
    print(data)
    firststring=testADF(data)
    stationaritydf1=stationary(firststring)
    print("***************first time stationarity**************************")
    print(stationaritydf1)
    if stationaritydf1['name'].str.contains("Non").any():
        firstdiffdf=first_diff(data)
        print("firstdif===================================")
        print(firstdiffdf)
        secondstring=testADF(firstdiffdf)
        stationaritydf2=stationary(secondstring)
        finaldf=data
        print("********************2nd time**********************************")
        print(stationaritydf2)
        if stationaritydf2['name'].str.contains("Non").any():
            df=firstdiffdf.diff().dropna()
            #check for the stationarity again
            r1=testADF(df)
            df2=stationary(r1)
            finaldf=data
            print(df2)
            if df2['name'].str.contains("Non").any():
                df2.loc[df2['stationarity'] == "Non-Stationary.", '2nd stationary'] = 'True'
                df2.loc[df2['stationarity'] != "Non-Stationary.", '2nd stationary'] = 'false' 
                print("***********df2**********")
                print(df2)
                dfr=df2.loc[df2['2nd stationary']=="True"]
                print("***************************dfr*****")
                print(dfr)
                columnlist=dfr['feature'].tolist()
                print(columnlist)
                a = [x for x in columnlist if x != "Sales"]
                print("********a******")
                print(a)
                seconddiff=True
                df=df.drop([x for x in a],axis=1)
                print(df.columns)
                finaldf=data.drop([x for x in a],axis=1)
                print("first df")
                print(df)
            else:
                df=firstdiffdf.diff().dropna()
                seconddiff=True
                finaldf=data
                print("first2 df")
                print(df)
        
        else:
            df=firstdiffdf
            seconddiff=False
            finaldf=data
            print("first3 df")
            print(df)
    else:
        df=data
        seconddiff=False
        finaldf=data
    
    
    
    return df,seconddiff,finaldf



def VARmodel(df_differenced):
    # Where the model runs. returns the model results
    # input parameters are the dataframe after differencing from first_diff() function and x = number of future months
    model = VAR(df_differenced)
    results = model.fit(maxlags=1)
    
    return results


def forecastData(results,df_diff,x,data):
    #takes the model results, differenced dataframe and number of future months for prediction,full dataset as input parameters
    #returns the dataframe with forecast values of the respective future months
    nobs=x
    lag_order = results.k_ar
    df_differenced=df_diff  

    a=data.index[-1]
    print(a)
    index = pd.date_range(a+pd.DateOffset(months=1), periods=3, freq='M')
    print(index)
    df_forecast=pd.DataFrame(index=index,columns=df_diff.columns)
    df_forecast=df_forecast.head(nobs)
    print("oooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
    print(df_forecast)
    # Input data for forecasting
    print(df_forecast.shape)
    forecast_input = df_differenced.values[-lag_order:]
    print(forecast_input.shape)
    fc = results.forecast(y=forecast_input, steps=nobs)
    print(fc)
    df_forecast2 = pd.DataFrame(fc, index=df_forecast.index, columns=df_forecast.columns)
    print(df_forecast2)
    
    return df_forecast2




def invert_transformation(df_train, df_forecast,second_diff=False):
    #returns a dataframe with forecast data converted back to original scale
    df_fc = df_forecast.copy()
    X_train_log2 = np.log(df_train)
    #df_fc=(pow(10,df_fc))#*1000 #take antilog
    columns = df_train.columns
    for col in columns:        
        # Roll back 2nd Diff
        if second_diff:
            df_fc[col] = (X_train_log2[col].iloc[-1]-X_train_log2[col].iloc[-2])+df_fc[col].cumsum()
            #df_fc[col]=10**df_fc[col]
        # Roll back 1st Diff
        df_fc[col] =X_train_log2[col].iloc[-1] + df_fc[col].cumsum()
   
    return df_fc
        
   

def impulseResponse(results,NoMonths,df_train):
     irf = results.irf(NoMonths)
     irf_arr=irf.irfs

     #print(irf_arr)  
     df=pd.DataFrame(columns=df_train.columns)
        
     for i in irf_arr:
        z1=i[0]
        z1=z1.reshape(1,len(df_train.columns))
        frame = pd.DataFrame(data=z1,columns=df_train.columns)
        df=df.append(frame)
        
     df=df.reset_index()
     #print(df)
     df=df.drop("index",axis=1)
     df=df.iloc[1:]
     dfA=df.to_numpy()
        
     elasticity= pd.DataFrame(dfA,index=df_train.index, columns=df_train.columns)
     print("-------------------------------elasticity-----------------") 
     print(elasticity)
     
     return elasticity



def Contribution(elasticitydf,predictiondf):
    predictiondf.columns=predictiondf.columns+"_pred"
    print("columns----------------")
    print(predictiondf.columns)
    df=elasticitydf.merge(predictiondf,left_index=True, right_index=True)
    columns=elasticitydf.columns
    print("columns2----------------")
    print(df.columns)
    for col in columns:     
                df[col+"_Contribution"] =(df[col]*df[col+"_pred"])
    df.to_csv(r"E:\contribution.csv")         
    return df

def ContributionPercentage(contributiondf):
    columns=contributiondf.columns  
    for col in columns:     
                contributiondf[col+"_Contribution%"] =(contributiondf[col]/contributiondf['Sales_pred'])
    contributiondf.to_csv(r"E:\contribution2.csv") 
    return contributiondf


def contributionVisual(df):
    df['Date_Contribution']=df.index
    df=df.drop('Sales_Contribution',axis=1)
    columnlist=df.columns
    
    sub='Contribution'
    res = [i for i in columnlist if sub in i]
    #print("-------------------------------list---------**")
    #print(res) 
    
    df2=pd.DataFrame(df,columns=res)
  
    return df2 #contribution_plotdf_pivot


###----------------------------------testing--------------------------#
#dfprep=DataPreprocessing("Foods","Brd00001")
#print(dfprep.columns)

#df2,seconddiff,finaldf=test2(dfprep)
#print("))))))))))))))))))))))))))))))))))))))))")
#print(df2)

#results=VARmodel(df2)
#dfe_forecast=forecastData(results,df2,3,dfprep)
#print(dfe_forecast)
#invertSale=invert_transformation(finaldf,dfe_forecast,second_diff=seconddiff)
#print(invertSale)
#invertSale=np.exp(invertSale) 
 

#print("--------------------------------invertsale-----------------")
#print(invertSale) 
#fulldfForecast1=finaldf.append(invertSale)
#print("-------------------------------fullforecast-------------")
#print(fulldfForecast1)
#fulldfForecast1_2=fulldfForecast1.copy()
#fulldfForecast1['date'] = fulldfForecast1.index

#fulldfForecast1=fulldfForecast1.tail(12)
#print("-----------------------------------last---------------")
#print(fulldfForecast1)
#invertSale['date'] = invertSale.index


#Sale_Date = fulldfForecast1['date'].tolist()
#Sale_Amount =fulldfForecast1['Sales'].values.tolist()

#print(Sale_Date)
#print(Sale_Amount)
#print("------------------elasticityeeeee--------------")
#elasticity=impulseResponse(results,35,fulldfForecast1_2)
#print(elasticity)
#print("********************contribution***********************")
#contribution=Contribution(elasticity,fulldfForecast1_2)
#print(contribution)
#contribution2=ContributionPercentage(contribution)
#contribution=contribution.tail(3)
#print(contribution2)
#print("tttttttttttttttttttttttttttttttttttttttttttttttttt")
#print(contribution.columns)
#tt=contributionVisual(contribution)
#print(tt.columns)


#tt['Month']=tt['Date_Contribution'].dt.month_name()
#tt['Month1']=tt['Date_Contribution'].dt.strftime('%Y/%b/%d')
#print(tt)
#tt.to_csv(r"C:\Users\Methma-Zkewed\Desktop\MMM dataset\MMM V2\testcontribution.csv")


#contribution['Date']=contribution.index
#creating the dataframe appropiately to plot the stacked bar chart
#contribution_plot_df=contribution[['Date','Search_Only_Contribution','facebook_Contribution','Instagram_Contribution','Display_Only_Contribution','Distributor_Margins_Contribution','JBP_Contribution','Loyalty_Schemes_Contribution','Trade_Promotion_Contribution']]
#contribution_plotdf_pivot=contribution_plot_df.melt(id_vars=['Date'], var_name='Investment Type', value_name='Contribution Amount')
#contribution_plotdf_pivot=contribution_plotdf_pivot.sort_values('Date')

#AandP =3 #request.POST.get('AandP')
#Consumer_Promotion =4 #request.POST.get('ConsumerPromotion')
#JBP =5 #request.POST.get('JBP')
#facebook =5 #request.POST.get('Facebook')
#instagram =5 #request.POST.get('instagram')
#video =5 #request.POST.get('video')
#Search_Only=5#request.POST.get('Search_Only')
#Display_Only=5#request.POST.get('Search_Only')
#Distributor_Margins=5#request.POST.get('Search_Only')
#Loyalty_Schemes=5#request.POST.get('Search_Only')
#Trade_Promotion=5#request.POST.get('Search_Only')
#messenger=9
#li=['Consumer_Promotion', 'AandP', 'Trade_Promotion', 'JBP','Distributor_Margins', 'Loyalty_Schemes', 'Video', 'facebook','Search_Only', 'instagram', 'messenger', 'Display_Only']

#for i in elasticity.columns.values:
 #   for j in li:
  #      if i==j:
   #         li.remove(i)
#for col in li:
 #   elasticity[col]=0
#print("+++++++++++++++++++++++++++++++++++++eeeeeeee")
#print(elasticity.columns)
#l2=elasticity.columns.tolist()
#l2=[x for x in l2 if x != "Sales"]
#print(l2)
#elasticity=elasticity.tail(3) 
#elasticity_T1=elasticity.head(1)

#elasticity_T1=elasticity_T1.reset_index()
#elasticity_T2=elasticity.iloc[1:]
#elasticity_T2=elasticity_T2.head(1)
#elasticity_T2=elasticity_T2.reset_index()
#elasticity_T3=elasticity.tail(1)

#elasticity_T3=elasticity_T3.reset_index()

#df=fulldfForecast1['Sales'].tail(1)
#Salestot=df.sum()
#print(elasticity_T1)
#print("------------------salestot-------------------")
#print(Salestot)
#st1=abs(Salestot+elasticity_T1['Search_Only']*Search_Only+elasticity_T1['facebook']*facebook+elasticity_T1['instagram']*instagram+elasticity_T1['Display_Only']*Display_Only+elasticity_T1['Distributor_Margins']*Distributor_Margins+elasticity_T1['JBP']*JBP+elasticity_T1['Loyalty_Schemes']*Loyalty_Schemes+elasticity_T1['Trade_Promotion']*Trade_Promotion+elasticity_T1['Consumer_Promotion']*Consumer_Promotion+elasticity_T1['Video']*video+elasticity_T1['AandP']*AandP+elasticity_T1['messenger']*messenger)
#st2=abs(Salestot+elasticity_T2['Search_Only']*Search_Only+elasticity_T2['facebook']*facebook+elasticity_T2['instagram']*instagram+elasticity_T2['Display_Only']*Display_Only+elasticity_T2['Distributor_Margins']*Distributor_Margins+elasticity_T2['JBP']*JBP+elasticity_T2['Loyalty_Schemes']*Loyalty_Schemes+elasticity_T2['Trade_Promotion']*Trade_Promotion+elasticity_T2['Consumer_Promotion']*Consumer_Promotion+elasticity_T2['Video']*video+elasticity_T2['AandP']*AandP+elasticity_T2['messenger']*messenger)
#st3=abs(Salestot+elasticity_T3['Search_Only']*Search_Only+elasticity_T3['facebook']*facebook+elasticity_T3['instagram']*instagram+elasticity_T3['Display_Only']*Display_Only+elasticity_T3['Distributor_Margins']*Distributor_Margins+elasticity_T3['JBP']*JBP+elasticity_T3['Loyalty_Schemes']*Loyalty_Schemes+elasticity_T3['Trade_Promotion']*Trade_Promotion+elasticity_T3['Consumer_Promotion']*Consumer_Promotion+elasticity_T3['Video']*video+elasticity_T3['AandP']*AandP+elasticity_T3['messenger']*messenger)

#a=3
#dfT={'Sales':st1} 
#dfT=pd.DataFrame(dfT)
#dfT2={'Sales':st2}
#dfT2=pd.DataFrame(dfT2)
#dfT3={'Sales':st3}
#dfT3=pd.DataFrame(dfT3)
    

#if a==1:
 #   r=dfT
#elif a==2:
 #   r=dfT.append(dfT2,ignore_index=True)
#elif a==3:
 #   r=dfT.append(dfT2,ignore_index=True)
  #  r=r.append(dfT3,ignore_index=True)
#print(r)

#rr=r['Sales'].tolist()

#df_forecast=pd.DataFrame(data=rr,index=dfe_forecast.tail(a).index,columns=r.columns)

    
#print(df_forecast)

#simulation=fulldfForecast1_2.tail(5).merge(df_forecast,how='left',left_index=True, right_index=True)[['Sales_pred','Sales']]
#print(simulation)


def ROI(df_tt,elasticity,NoMonths,year,month):
    columns=[x for x in elasticity.columns if x != "Sales"]
    for col in columns:     
                df_tt[col+"_ROI"] =(df_tt[col+"_Contribution"]/df_tt[col+"_pred"])
    
    df_tt.to_csv(r"E:\roi.csv")
    columnlist=df_tt.columns
    
    sub='ROI'
    res = [i for i in columnlist if sub in i]
    #print("-------------------------------list---------**")
    #print(res) 
    
    df_tt2=pd.DataFrame(df_tt,columns=res)
    df_tt2['Date']=df_tt2.index
    df_tt2['Year']=df_tt2['Date'].dt.year
    df_tt2['Month']=df_tt2['Date'].dt.strftime("%b")
    df_tt2=df_tt2.iloc[:-NoMonths]
    df_tt2=df_tt2[(df_tt2['Year']==year) & (df_tt2['Month']==month) ]
    
    df_tt2 = pd.melt(df_tt2, id_vars=['Year', 'Month','Date'], var_name='Investment Type', value_name='ROI')

    return df_tt2       

#df_tt=ROI(contribution,elasticity,3,2019,"Jun")
#print(df_tt)
