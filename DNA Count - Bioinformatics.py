############################
'''
This project has the objective to get familiar with the Streamlit and Altair packages for Web Data Science 
'''
############################

import altair as alt
import streamlit as st
import pandas as pd
from PIL import Image

#Page Title
image = Image.open('transferir.jpg')

st.image(image, use_column_width = True)

st.write(""" 

	# DNA Nucleotide Count Web APP

	This app counts the DNA nucleotids composition

	***

	""")

#Header and Sequence presentation with random DNA sequence from the internet with length of 500

st.header('Enter DNA Sequence')

sequence_rnd = 'GTAAGTAGCGTAGGCCCGCACGCAAGATAAACTGCTAGGGAACCGCGTTTCCACGACCGGTGCACGATTTAATTTCGCCGACGTGATGACATTCCAGGCAGTGCCTCTGCCGCCGGACCCCTCTCGTGATTGGGTAGCTGGACATGCCCTTGTAAGATATAACAAGAGCCTGCCTGTCTAATGATCTCACGGCGAAAGTCGGGGAGACAGCAGCGGCTGCAGACATTATACCGCAACAACACTAAGGTGAGATAACTCCGTAATTGACTACGCGTTCCTCTAGACCTTACTTGACCGGATACAGTGTCTTTGACACGTTTATGGGTTACAGCAATCACATCCAAGACTGGCTATGCACGAAGCAACTCTTGAGTGTTAAAATGTTGACCCCTGTATTTGGGATGCGGGTAGTAGATGAGTGCAGGGACTCCGAGGTCAAGTACATTACCCTCTCATAGGGGGCGTTCTAGATCACGTTACCACCATATCATTCGAGCATG'

sequence_input = f'>DNA Query\n{sequence_rnd}'

sequence = st.text_area('Sequence Input', sequence_input, height = len(sequence_rnd))

st.write('''***''')

#Output (DNA Nucleotid Count) -- Method 1 of presenting the data // DICTIONARY
st.header('DNA Nucleotide Count')

st.subheader('1. Print dictionary')
def counting_n(seq):
	d = dict([
		('A',seq.count('A')),
		('T',seq.count('T')),
		('G',seq.count('G')),
		('C',seq.count('C')),
		])
	return d

X = counting_n(sequence_rnd)

X

#Output (DNA Nucleotid Count) -- Method 2 // TEXT
st.subheader('2. Print text')

for nucl, numb in X.items():
	st.write(f'There are {numb} of {nucl}')

#Output -- Method 3 // DATA FRAME
st.subheader('3. Data Frame')
df = pd.DataFrame(X.items(), columns = ['nucleotids','count'])
st.write(df)

#Output -- Method 4 // BAR PLOT
st.subheader('4. Bar Chart')

p = alt.Chart(df).mark_bar().encode(
	x = 'nucleotids',
	y = 'count')

#Adjusting the width of the graphic
p = p.properties(width = alt.Step(80))

st.write(p)