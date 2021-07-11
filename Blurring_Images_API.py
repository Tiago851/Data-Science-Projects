'''
Basic script for uploading an Image to our streamlit API and having it blurred with the help
from the library OpenCV

Main point is the introduction to OpenCV 

'''

import streamlit as st
import cv2
from PIL import Image
import numpy as np

st.title('App for blurring images uploaded by the user')

file_upload = st.file_uploader('Choose your image', type = ['png','jpg'])

if file_upload is not None:

	#Original 
	st.header('Original Image')
	img = Image.open(file_upload)
	st.image(img, caption = 'Uploaded image', use_column_width = True)

	#Converting the PIL file into an array for cv2
	img = np.asarray(img)

	#Blurring
	blurred_img = cv2.blur(img, (10,10))
	st.header('Blurred Image')
	st.image(blurred_img, caption = 'Altered Image, ksize = 10,10', use_column_width = True)

else:
	st.write('Nothing was uploaded or found')