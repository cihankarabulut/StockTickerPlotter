import streamlit as st
import pandas as pd
import json as json
import requests
import plotly.express as px

def main():
   
    st.title('TDI Milestone: Stock Ticker Plotter')
    st.markdown('A simple app to plot monthly closing prices for a selected stock.')

    
    
    
    with st.sidebar:
        st.title('Select')
        link = '[List of all stock symbols](https://stockanalysis.com/stocks/)'
        st.markdown(link, unsafe_allow_html=True)   
        ticker = st.text_input("Stock Symbol (e.g. IBM):")
    
    Year = []
    Month = []
        
    if ticker != "":        
        df = load_data(ticker)     
        Year=sorted(df['Year'].unique())
        Month=['January', 'February', 'March', 'April', 'May', 'June', 'July', 
               'August', 'September', 'October', 'November', 'December']
        selectedyear = st.sidebar.selectbox("Year", Year)
        selectedmonth = st.sidebar.selectbox("Month", Month)
        chosendf = df[(df['Year']==selectedyear) & (df['Month']==selectedmonth)]
        fig = px.line(chosendf, x="date", y="close", title= ticker,markers=True)
        st.plotly_chart(fig, use_container_width=True)    
    else:
        pass
  

@st.cache
def load_data(symbol):
      
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}.SHZ&outputsize=full&apikey=U4KW25U3T0YN3NK0'
    r = requests.get(url)
    result = r.json()
    data = result['Time Series (Daily)']
    df = pd.DataFrame.from_dict(data, orient = 'index')
    df = df.reset_index()
    df = df.rename(index=str, columns={"index": "date", "1. open": "open", "2. high": "high", "3. low": "low", "4. close": "close","5. volume":"volume"})
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by=['date'])
    df.open = df.open.astype(float)
    df.close = df.close.astype(float)
    df.high = df.high.astype(float)
    df.low = df.low.astype(float)
    df.volume = df.volume.astype(int)
    df['Month'] = df['date'].dt.month_name()
    df['Year'] = df['date'].dt.year
    return df
    
    

if __name__ == '__main__':
    main()