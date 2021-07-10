'''
The main purpose of this project is to dive into the datasets from kaggle.com regarding
the happiness index for 2018 and 2019 and extract as many details as possible for comparison.

This project was entirely my idea and developed without any assistance. 

'''

import streamlit as st
import requests
from bs4 import BeautifulSoup 
import csv
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

st.title('World Happiness Indexes for 2019 & 2020')

st.markdown("""
	This app will give a general analysis of what influences happiness for a list of 150+ countries.
	If you want to see how your country fared between 2019 and 2020, you can enter its name on the left.

	The data was retrieved from [Kaggle](https://www.kaggle.com/mathurinache/world-happiness-report?select=2020.csv)
	and the app was developed in Python using the following libraries:
	* **Pandas**
	* **Streamlit**
	* **csv**
	* **Matplotlib**
	""")

#Sidebar title
st.sidebar.title('Country Selection')

#Filter
user_input = st.sidebar.text_input('Enter your country:', 'Portugal')

#Country Info + Scrapper
expander_bar = st.sidebar.beta_expander(f'About {user_input}')

def scrapper_wiki(user_input):
    
    #API call
    link = f'https://www.countryreports.org/country/{user_input}.htm'
    request = requests.get(link)
    soup = BeautifulSoup(request.content, 'html.parser')
    
    #Location Image
    img = soup.select('img')[2]['src']
    img_link = requests.get(f'https:{img}')
    country_image = open('country.jpg','wb')
    country_image.write(img_link.content)
    country_image.close()

    final_image_format = Image.open('country.jpg').convert('RGB')

    expander_bar.image(final_image_format, use_column_width = True)

    #Country info
    data = soup.find_all('td')
    
    #Output with overall country info - data needs to be cleared off tabs + new lines
    capital = data[1].text
    capital = ''.join(data[1].text.split())
    
    expander_bar.write('**Capital city:** ' + ' '.join(data[1].text.split()))
    expander_bar.write('**Government type:** ' + ' '.join(data[3].text.split()))
    expander_bar.write('**Currency:** ' + ' '.join(data[5].text.split()))
    expander_bar.write('**Population:** ' + ' '.join(data[7].text.split()))
    expander_bar.write('**Total area:** ' + ' '.join(data[9].text.split()))
    expander_bar.write('**Location:** ' + ' '.join(data[11].text.split()))
    expander_bar.write('**Language:** ' + ' '.join(data[13].text.split()))
    expander_bar.write('**GDP - per capita (PPP):** ' + ' '.join(data[17].text.split()))

#Execute scrapper
scrapper_wiki(user_input)
st.sidebar.write('Data from: [Countryreports](https://www.countryreports.org)')

#Wikipedia page
st.sidebar.write(f"More information about [{user_input}](https://en.wikipedia.org/wiki/{user_input})")

#Data frames
with open('2019.csv','r') as f_2019:
	df_2019 = pd.read_csv(f_2019)

with open('2020.csv','r') as f_2020:
	df_2020 = pd.read_csv(f_2020)

#Clearing the DF from 2020 to make it equal to 2019
df_2020.drop(['Standard error of ladder score', 
          'upperwhisker',
          'lowerwhisker',
          'Ladder score in Dystopia', 
          'Logged GDP per capita',
          'Freedom to make life choices',
          'Generosity',
          'Perceptions of corruption',
          'Social support',
          'Healthy life expectancy',
          'Dystopia + residual'], axis = 1, inplace = True)

df_2020['Overall rank'] = range(1,len(df_2020['Country name'])+1,1)

#2018
st.header('Dataframe for 2019')
st.write(df_2019)

#2018
st.header('Dataframe for 2020')
st.write(df_2020)

#Comparison function
def compare():
	byCountry_2019 = df_2019.groupby('Country or region')
	byCountry_2020 = df_2020.groupby('Country name')

	#Rank Comparison
	rank_2019 = byCountry_2019.sum().loc[user_input]['Overall rank']
	rank_2020 = byCountry_2020.sum().loc[user_input]['Overall rank']

	rank_comparison = rank_2019 < rank_2020

	st.header('Rank Comparison')
	if rank_comparison:
		st.write(f'Your country got a bit unhappier from 2019 to 2020 going from {rank_2019} to {rank_2020}. You can see the statistics below!')
	else:
		st.write(f'Great! Seems like life is getting better in {user_input}. You went from {rank_2019} to {rank_2020}. You can see the statistics below!')

	#Extracting variables - 2020
	score20 = byCountry_2020.sum().loc[user_input][0]
	gdp20 = byCountry_2020.sum().loc[user_input][1]
	social20 = byCountry_2020.sum().loc[user_input][2]
	healthy_life20 = byCountry_2020.sum().loc[user_input][3]
	freedom20 = byCountry_2020.sum().loc[user_input][4]
	generosity20 = byCountry_2020.sum().loc[user_input][5]
	corruption20 = byCountry_2020.sum().loc[user_input][6]

	#Extracting variables - 2019
	score19 = byCountry_2019.sum().loc[user_input][1]
	gdp19 = byCountry_2019.sum().loc[user_input][2]
	social19 = byCountry_2019.sum().loc[user_input][3]
	healthy_life19 = byCountry_2019.sum().loc[user_input][4]
	freedom19 = byCountry_2019.sum().loc[user_input][5]
	generosity19 = byCountry_2019.sum().loc[user_input][6]
	corruption19 = byCountry_2019.sum().loc[user_input][7]

	results = pd.DataFrame(columns = ['2019','2020'], index =['Rank',
															  'Score',
															  'Log GDP per capita',
															  'Social support',
															  'Healthy life expectancy',
															  'Freedom to make life choices',
															  'Generosity',
															  'Perceptions of corruption'] )

	#Result variables for both years
	results['2020'] = [rank_2020, score20, gdp20, social20, healthy_life20, freedom20, generosity20, corruption20]
	results['2019'] = [rank_2019, score19, gdp19, social19, healthy_life19, freedom19, generosity19, corruption19]

	results['Variance'] = ['--', score20 - score19, gdp20 - gdp19, social20 - social19, healthy_life20 - healthy_life19,
							freedom20 - freedom19, generosity20 - generosity19, corruption19 - corruption20]

	for i, value in enumerate(results['Variance'][1:]):
		if value < 0:
			results['Variance'][i+1] = 'Negative effect'
		else:
			results['Variance'][i+1] = 'Positive effect'

	st.write(results)

#Dystopia - the most recent year is taken into consideration
def dystopia(user_input):

	last_country = df_2020['Ladder score'].iloc[-1]
	user_position = df_2020.groupby('Country name').sum().loc[user_input]['Ladder score']

	if last_country == user_position:

		st.subheader(user_input)

		st.write("""

			**Dystopia**

			It seems that this country is closest to what is called a **Dystopia**. A Dystopia is an imaginary country 
			that has the world’s least-happy people and the lowest of all six parameters shown below.Since life would 
			be very unpleasant in a country with the world’s lowest incomes, lowest life expectancy, lowest generosity,
			most corruption, least freedom and least social support, it is referred to as “Dystopia,” in contrast to Utopia.
			""")
		st.image(Image.open('desert.jpg'), width = 500)

#Dystopia
dystopia(user_input)

#Comparing Table + Plotting Function
def analysis():

	#Extracting the variables from the function Compare
	variables = compare()

	#Title
	st.header(f'Analysis for {user_input} in 2020.')
	st.subheader('The position of the country in the graphics will show in red.')

	#Score
	#Place in score in 2020 and highlighting in red the position in the graphic
	st.subheader('Score')
	plt.figure(figsize = (8,6))
	n, bins, patches = plt.hist(df_2020['Ladder score'], bins = 15, edgecolor = 'black')
	plt.xlabel('Score')
	plt.ylabel('Frequency')
	plt.title(user_input)

	#I tried to highlight in red where the country's score is located in the histogram
	for i, y in enumerate(bins):
		if df_2020.groupby('Country name').sum().loc[user_input]['Ladder score'] > y:
			patches[i-1].set_fc('b')
			patches[i].set_fc('r')
	
	#Showing the plot
	st.pyplot(plt)

	#GDP
	#Place of the Log GPP in 2020 and highlighting in red the position in the graphic
	st.subheader('Log GDP')
	plt.figure(figsize = (8,6))
	n, bins, patches = plt.hist(df_2020['Explained by: Log GDP per capita'], bins = 20, edgecolor = 'black')
	plt.xlabel('Log GDP per capita')
	plt.ylabel('Frequency')
	plt.title(user_input)

	#Red highlighting
	for i, y in enumerate(bins):
		if df_2020.groupby('Country name').sum().loc[user_input]['Explained by: Log GDP per capita'] > y:
			patches[i-1].set_fc('b')
			patches[i].set_fc('r')

	#Showing the plot
	st.pyplot(plt)

	st.write("""
		This indicator represents the average of the following indicators:
		* **Social support**
		* **Healthy life expectancy**
		* **Freedom to make life choices**
		* **Generosity**
		""")

	#Average of the indicators - 'Social support', 'Healthy life expectancy', 'Freedom to make life choices', 'Generosity'
	avg = df_2020[['Explained by: Social support',
					'Explained by: Healthy life expectancy',
					'Explained by: Freedom to make life choices',
					'Explained by: Generosity']].mean(axis = 1)

	#Same as below but for the selected country
	avg_selected_country = df_2020.groupby('Country name').sum().loc[user_input][['Explained by: Social support',
					'Explained by: Healthy life expectancy',
					'Explained by: Freedom to make life choices',
					'Explained by: Generosity']].mean()	

	plt.figure(figsize = (8,6))
	n, bins, patches = plt.hist(avg, bins = 10, edgecolor = 'black')
	plt.xlabel('Average')
	plt.ylabel('Frequency')
	plt.title(user_input)

	for i, y in enumerate(bins):
		if avg_selected_country > y:
			patches[i-1].set_fc('b')
			patches[i].set_fc('r')

	#Showing the plot
	st.pyplot(plt)

	#Corruption
	st.subheader('Corruption')
	plt.figure(figsize = (8,6))
	n, bins, patches = plt.hist(df_2020['Explained by: Perceptions of corruption'], bins = 20, edgecolor = 'black')
	plt.xlabel('Corruption')
	plt.ylabel('Frequency')
	plt.title(user_input)

	corrupt_position = df_2020.groupby('Country name').sum().loc[user_input][6]

	#Red highlighting
	for i, y in enumerate(bins):
		if df_2020.groupby('Country name').sum().loc[user_input]['Explained by: Perceptions of corruption'] > y:
			patches[i-1].set_fc('b')
			patches[i].set_fc('r')

	#Showing the plot
	st.pyplot(plt)

#Button to execute the functions above
if st.button('Analysis'):
	#Execute function
	analysis()