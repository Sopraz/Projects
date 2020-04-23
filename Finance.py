""" Finance """
import bs4,os
import pandas as pd
import numpy as np
import pandas_datareader.data as web
import matplotlib.pyplot as plt
from matplotlib import style
import datetime as dt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
os.chdir('/Users/mamane/Desktop/Cotations des actions') """ 'Cotations des actions' is the folder where all the files that can be generated for this program are put' """
from datapackage import Package
import openpyxl



"""This program is my first project, created after 1 month and a half the first day of my python journey. It aims to facilitate getting the asset prices of some stocks which come from the CAC40, the Dow Jones, or even the Nasdaq ."""
"""You need Internet for this program to be able to get the stock prices"""


class Stock_prices:
    name_of_assets = {'AI.PA':'Air liquide','AAPL':'Apple.Inc','AF.PA':'Air France','TEP.PA':'Teleperformance','RXL.PA':'Rexel','MSFT':'Microsoft','AMZN':'Amazon','SU.PA':'Shneider Electric','MDM.PA':'Maison du Monde','^FCHI':'CAC 40','^DJI':'Dow Jones industrial Average','KEY.PA':'KEYRUS','CAPLI.PA':'Groupe Capelli'}

    def __init__(self,name_of_the_asset,debut,fin): #Indiquer le nom de l'action plus la date voulues du debut des cotations a la fin
        self.name = name_of_the_asset
        self.date_premiere_cotation = debut
        self.date_derniere_cotation = fin
        self.nom = self.name+' from '+str(self.date_premiere_cotation)+' to '+str(self.date_derniere_cotation)

    def __repr__(self):
        return f"Asset = {Stock_prices.name_of_assets[self.name]}"

    def get_to_portfolio(self): #Bring the Assets in a DataFrame
        try:
            self.datas = web.DataReader(name = self.name, data_source = 'yahoo',start = self.date_premiere_cotation,end = self.date_derniere_cotation)
        except:
            print("The asset is not include in our Data Base, however you can add it using its Yahoo Sigle and it's name in the dictionnary : 'name of the Asset' by modifying the programm...")
            return
        return self.datas

    def save_stockprices_to_csv(self): #Explicite :)
        cotation = Stock_prices.get_to_portfolio(self)
        fiche_cota = cotation.to_csv(self.name+' from '+str(self.date_premiere_cotation)+' to '+str(self.date_derniere_cotation)+'.csv')

    def Taux_var(self):
        datas = Stock_prices.get_to_portfolio(self)
        var = ((datas.iloc[:,3][-1] - datas.iloc[:,3][0])/datas.iloc[:,3][0])*100
        return var

    def Taux_var_max(self):
        datas = Stock_prices.get_to_portfolio(self)
        var = ((datas.iloc[:,3].max() - datas.iloc[:,3].min())/datas.iloc[:,3].min())*100
        return var

    def save_stockprices_to_excel(self): #Explicite :)
        cotation = Stock_prices.get_to_portfolio(self)
        fiche_cota = cotation.to_excel(self.nom+'.xlsx')
    """ Pb: ufunc 'add' did not contain a loop with signature matching types (dtype('<U32'), dtype('<U32')) -> dtype('<U32')"""
    # def save_to_text_file(self):
    #     cotation = Assets.get_to_portfolio(self)
    #
    #     with open(self.nom,mode = 'w') as f:
    #         for i in range (1,len(cotation)-1):
    #             f.write(cotation.iloc[i].values+'\n')
    # def average_prices(self):
    #     cotation = Stock_prices.get_to_portfolio(self)
    #     for i in cotation

    # def get_to_portfolio_averageSP_month(self):
    #     cotation = Stock_prices.get_to_portfolio(self)
    #     for i in cotation.index
    #




class Draw_curve(Stock_prices):
    def __init__(self,name_of_the_asset,debut,fin):
        Stock_prices.__init__(self,name_of_the_asset,debut,fin)

    def simple_line(self,grid = True,parameters=['Adj Close']):#,fill_area = True):
        mystocks = Stock_prices.get_to_portfolio(self)
        plt.figure(figsize = (12.2,4.5))
        plt.title(label = "Courbe de l'action "+self.name)
        for i in parameters:
            plt.plot(mystocks.index,mystocks[i],label = 'Adj Close')
        plt.legend(parameters)
        plt.xlabel('dates')
        plt.ylabel('coations')
        if grid :
            plt.grid(True)
        # if fill_area :
        #     plt.fill_between(self.date_premiere_cotation,self.date_derniere_cotation,'b')
        plt.savefig(fname ='cotations of '+self.nom+'.png' )


# if __name__ == "__main__":
#     Teleperformance = Draw_curve("TEP.PA", dt.datetime(2000,1,1),dt.datetime(2019,12,31))
#     Teleperformance.save_stockprices_to_excel()
#     Teleperformance.simple_line()


class Economics_indices:
    "You need Internet to get the package of indices"""
    Gini_Indices = {}
    package = Package('https://datahub.io/core/gini-index/datapackage.json')
    for resource in package.resources:
        if resource.descriptor['datahub']['type'] == 'derived/csv':
            for i in resource.read():
                # print(i)
                if i[0] not in Gini_Indices:
                    Gini_Indices[i[0]]= {}
                Gini_Indices[i[0]][i[2]] = str(i[3])
    def Get_gini_indice(self,country,year):
        if country not in Economics_indices.Gini_Indices.keys():
            print('I am afraid this country does not exist ...')
            return
        try:
            print('Gini indice of',country,'in',year,':', Economics_indices.Gini_Indices[country][year])
        except KeyError:
            print('The year provided for this country is not in the DataBase')
            print('List of years available for this country')
            for i in Economics_indices.Gini_Indices[country]:
                print(i)

    def Get_PIB(self,country,rank = False): #PIB from 2018, from an excel file
        os.chdir('/Users/mamane/Desktop/New/Datas')
        wb = openpyxl.load_workbook('GDP 2018.xlsx')
        sheet1 = wb[wb.active.title]
        dico = {}
        list = ['A','B','D','E']
        for column in list:
            dico[sheet1[column+'4'].value] = []
            for row in range(6,210):
                dico[sheet1[column+'4'].value].append(sheet1[column+str(row)].value)

        Df_GDP = pd.DataFrame(dico,index = dico['Sigle'])
        Df_GDP = Df_GDP.drop(Df_GDP.columns[0],axis = 'columns')
        os.chdir('/Users/mamane/Desktop/Cotations des actions')
        Data = Df_GDP.loc[country]
        print('Country :',Data[1],'\nPIB :',str(Data[2]),'millions of US dollars')
        if rank:
            print('Rank :',Data[0])





"""Idee, calculer l'integrale en dessous de la courbe correspondante """
