#!/usr/bin/env python
# coding: utf-8

# In[6]:


import pandas as pd
import json

import numpy as np


# In[2]:


#to handle json serialization
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)

        
#extracts scheme plan from scheme name
def plan(x):
    if 'direct' in x.lower():
        return 'DIRECT'
    else:
        return 'REGULAR'

#converts txn type
def txnType(x):
    if 'purchase' in x.lower():
        return 'BUY'
    else:
        return 'SELL'


# In[3]:


def mutual_fund_generator(transaction_path, valuation_path):
    txn=pd.read_excel(transaction_path)
    holdings = pd.read_excel(valuation_path, skiprows=[0])
    
    holdings = holdings.rename(columns={
    'AMC Name': '_amc',
    'Scheme': '_schemeCode',
    'Folio': '_folioNo',
    'Unit Balance': '_units',
    'Current Value(Rs.)': '_nav',
    'Cost Value(Rs.)': '_invested',
    'Type': '_fundType'
    })
    holdings['_registrar'] = "CAMS" #Since this is built for MFs serviced by CAMS
    holdings['_isin'] = '3234' #No reference
    holdings['_amfiCode']='' #No reference
    holdings['_dividendType'] = 'Reinvest' #No reference
    holdings['_mode'] = "DEMAT"
    holdings['_FatcaStatus'] = "Yes" #No reference
    holdings['_closingUnits'] = holdings['_units'] 
    holdings['_lienUnits'] = 0 #No reference
    holdings['_rate'] = holdings['_nav']/holdings['_units'] #No reference, thus rough calculations
    holdings['_lockingUnits'] = 0 #No reference
    
    txn = txn.rename(columns={
    'MF_NAME': '_amc',
    'SCHEME_NAME': '_schemeCode',
    'AMOUNT': '_amount',
    'PRICE': '_nav',
    'TRADE_DATE': '_navDate',
    'TRANSACTION_TYPE': '_type'
})
    txn['_txnId'] = '2345' #No reference
    txn['_registrar'] = "CAMS"
    txn['_schemePlan'] = txn['_schemeCode'].apply(plan)
    txn['_schemeTypes'] = "DEBT_SCHEMES" #No reference
    txn['_schemeCategory'] = "AGGRESSIVE_HYBRID_FUND" #No reference
    txn['_isin'] = '3234' #No reference
    txn['_amfiCode'] = '' #No reference
    txn['_schemeOption'] = 'REINVEST'
    txn= txn.merge(holdings[['_amc', '_fundType']], on='_amc', how='left') #to get fund type
    txn['_ucc'] = '' #No reference
    txn['_closingUnits'] = txn[['_amc', '_navDate', 'UNITS']].groupby('_amc').cumsum() #since only units are reported in this sheet, thus we are doing cumsum to get the closing units, assumpotions is the data is already sorted by _navDate for each MFs group 
    txn['_lienUnits'] = "" #No reference
    txn['_navDate'] = txn['_navDate'].astype('datetime64[ns]').astype(str)
    txn['_type'] = txn['_type'].apply(txnType)
    txn['_orderDate'] = txn['_navDate']
    txn['_executionDate'] = txn['_navDate']
    txn['_lock-inDays'] = 365 #No reference
    txn['_lock-inFlag'] = 1
    txn['_mode'] = "DEMAT"
    txn['narration'] = "" #No reference
    
    mutual_funds = {
      "Account": {
        "Profile": {
          "Holders": {
            "Holder": {
              "_name": holdings['Investor Name'].tolist()[0],
              "_dob": "", #No reference
              "_mobile": "", #No reference
              "_nominee": "", #No reference
              "_dematId": "",
              "_email": "", #No reference
              "_pan": "", #No reference
              "_ckycCompliance": "true" #No reference
            }
          }
        },
        "Summary": {
          "Investment": {
            "Holdings": {
              "Holding": holdings.drop(['Investor Name', 'PAN', 'NAV Date', '_invested'], axis=1).fillna("").to_dict(orient='records')
            }
          },
          "_investmentValue": holdings['_invested'].sum(),
          "_currentValue": holdings['_nav'].sum()
        },
        "Transactions": {
          "Transaction": txn.drop(['INVESTOR_NAME', 'PAN', 'FOLIO_NUMBER', 'PRODUCT_CODE', 'BROKER', 'UNITS', 'DIVIDEND_RATE'],axis=1).fillna("").to_dict(orient='records'),
          "_endDate": txn['_navDate'].max(),
          "_startDate": txn['_navDate'].min()
        },
        "_xmlns": "http://api.rebit.org.in/FISchema/mutual_funds",
        "_xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "_xsi:schemaLocation": "http://api.rebit.org.in/FISchema/mutual_funds ../FISchema/mutual_funds.xsd",
        "_linkedAccRef": "",
        "_maskedAccNumber": "",
        "_version": "1.1",
        "_type": "mutualfunds"
      }
    }
        
    return(json.dumps(mutual_funds, cls=NpEncoder))


