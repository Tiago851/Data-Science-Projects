############################
'''
Web App for Cryptocurrency Data Science outputs and analysis
'''
############################

#Libraries and modules
import pandas as pd 
import streamlit as st
from PIL import Image
from bs4 import BeautifulSoup
import requests
import json
import matplotlib.pyplot as plt

#Page and sidebar basic configuration
st.set_page_config(layout = 'wide')
col1 = st.sidebar
col2, col3 = st.beta_columns(2)

#Sidebar setting
with col1:
	col1.title('Input Options')

	#Currency selection
	def selec_curr():
		currency = st.sidebar.selectbox('Price currency', ('BTC','ETH','USD'))

		if currency == 'BTC':
			currency = 0
		elif currency == 'ETH':
			currency = 1
		else:
			currency = 2

		return currency

	#Currency call
	currency = selec_curr()

	#Number of coins
	numbr_coins = st.sidebar.slider('Number of cryptocurrencies',1,100, value = 100)

	#Change percentage
	perct_change = st.sidebar.selectbox('Change percentage', ('24 h','7 d'))

#Column 2 setting - Where the Data frames will be displayed 
with col2:
	#Header
	image = Image.open('bitc.jpg')
	st.image(image, width = 500)
	st.title('Top Cryptocurrencies')

	st.markdown('''
		This app retrieves cryptocurrencies prices for the top 20 assets by market cap. Data from **CoinMarketCap**.
		''')

	expander_bar = st.beta_expander('''About''')
	expander_bar.markdown('''
		* **Main Python libraries**: pandas, streamlit, bs4, matplotlib, json
		* **Data Source**: [CoinMarketCap](https://coinmarketcap.com/)
		* **Scrapper**: Based on the article [Web Scraping Crypto Prices With Python](https://towardsdatascience.com/web-scraping-crypto-prices-with-python-41072ea5b5bf) 
		''')

	st.header('Price data of selected Cryptocurrencies')

	#Retreiving data from the web
	@st.cache
	def scrapper():

		#API call & json modules	
		request = requests.get('https://coinmarketcap.com/')
		soup = BeautifulSoup(request.content, 'html.parser')
		data = soup.find('script', id = '__NEXT_DATA__', type = "application/json")
		coin_base = json.loads(data.contents[0])
		listings = coin_base['props']['initialState']['cryptocurrency']['listingLatest']['data']
		coin = {}

		for i in listings:
			coin[str(i['id'])] = i['slug']

		coin_name = []
		coin_price = []
		coin_symbol = []
		volume_24h = []
		market_cap = []
		price_change_24h = []
		price_change_7d = []

		for i in listings:
			coin_name.append(i['slug'])
			coin_symbol.append(i['symbol'])
			market_cap.append(i['quotes'][currency]['marketCap'])
			volume_24h.append(i['quotes'][currency]['volume24h'])
			price_change_24h.append(i['quotes'][currency]['percentChange24h'])
			price_change_7d.append(i['quotes'][currency]['percentChange7d'])

			#price
			coin_price.append(i['quotes'][currency]['price'])

		df = pd.DataFrame(columns = ['Name','Price','Symbol','Market Cap','Volume 24 h','24 h %','7d %'])
		df['Name'] = coin_name
		df['Price'] = coin_price
		df['Symbol'] = coin_symbol
		df['Market Cap'] = market_cap
		df['Volume 24 h'] = volume_24h
		df['24 h %'] = price_change_24h
		df['7d %'] = price_change_7d

		return df

	df = scrapper()
	
	#Number of lines to be shown, selected by the user
	df_selected = df[:numbr_coins]

	if perct_change == '24 h':
		df_selected = df_selected.drop(['7d %'], axis = 1, inplace = False)
	else:
		df_selected = df_selected.drop(['24 h %'], axis = 1, inplace = False)

	st.write(df_selected)


#Column 3 setting - Graphic
with col3:
	st.title('Bar Plot for the percentage change')
	st.subheader('Sorted values by the percentage of change selected')

	if perct_change == '24 h':
		st.write('**24 hours**')

		#DF adaptation for the plot
		df_changed = pd.concat([df_selected['Symbol'],df_selected['24 h %']], axis = 1)
		df_changed = df_changed.sort_values(by = ['24 h %'])
		df_changed = df_changed.set_index(df_changed['Symbol'])
		df_changed['positive_change'] = df_changed['24 h %'] > 0
		
		#plotting
		plt.figure(figsize = (5,20))
		plt.subplots_adjust(top = 1, bottom = 0)
		df_changed['24 h %'].plot(kind = 'barh', color = df_changed['positive_change'].map({True: 'b',False: 'r'}))

	else:
		st.write('**7 days**')

		#DF adaptation for the plot
		df_changed = pd.concat([df_selected['Symbol'],df_selected['7d %']], axis = 1)
		df_changed = df_changed.sort_values(by = ['7d %'])
		df_changed = df_changed.set_index(df_changed['Symbol'])
		df_changed['positive_change'] = df_changed['7d %'] > 0
		
		#plotting
		plt.figure(figsize = (5,20))
		plt.subplots_adjust(top = 1, bottom = 0)
		df_changed['7d %'].plot(kind = 'barh', color = df_changed['positive_change'].map({True: 'b',False: 'r'}))

	st.pyplot(plt)