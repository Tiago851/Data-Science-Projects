''''
This project is my version of the solutions for the questions posed in the first project from the course:
    2021 Python for Machine Learning & Data Science Masterclass

The CSV file with the data is provided by the course as well and is available in this repository.
The name of the file is below

If my solution is not correct, the solution from the course is provided below my own solution in string format

'''

#Modules
import pandas as pd

#Reading the CSV file
hotels = pd.read_csv('hotel_booking_data.csv')

#Task 1 - How many rows are there?
len(hotels)


#Task 2 - Is there any missing data? If so, which column has the most missing data?
hotels.isnull().sum()


#Task 3 - Drop the "company" column from the dataset.
hotels = hotels.drop('company', axis = 1)


#Task 4 - What are the top 5 most common country codes in the dataset?
hotels['country'].value_counts()[:5]


#Task 5 - What is the name of the person who paid the highest ADR (average daily rate)? How much was their ADR?
hotels[hotels['adr'] == hotels['adr'].max()]['name']


#Task 6 - The adr is the average daily rate for a person's stay at the hotel. What is the mean adr across all the hotel stays in the dataset?
round(hotels['adr'].mean(),2)


#Task 7 - What is the average (mean) number of nights for a stay across the entire data set? Feel free to round this to 2 decimal points.
round(hotels['stays_in_week_nights'].mean() + hotels['stays_in_weekend_nights'].mean(), 2)


#Task 8 - What is the average total cost for a stay in the dataset? Not average daily cost, but total stay cost. 
# (You will need to calculate total cost your self by using ADR and week day and weeknight stays). 
# Feel free to round this to 2 decimal points.
hotels['Total cost'] = (hotels['stays_in_weekend_nights'] + hotels['stays_in_week_nights']) * hotels['adr']
hotels['Total cost'].mean()


#Task 9 - What are the names and emails of people who made exactly 5 "Special Requests"?
hotels[hotels['total_of_special_requests'] == 5][['name','email']]


#Task 10 - What percentage of hotel stays were classified as "repeat guests"? 
#(Do not base this off the name of the person, but instead of the is_repeated_guest column)
round(len(hotels[hotels['is_repeated_guest'] == 1]) * 100 / len(hotels) ,2) 


#Task 11 - What are the top 5 most common last name in the dataset? 
# Bonus: Can you figure this out in one line of pandas code? Yes!!!
# (For simplicity treat the a title such as MD as a last name, for example Caroline Conley MD can be said to have the last name MD) 
hotels['name'].str.split().apply(lambda x: x[1]).value_counts()[:5]


#Task 12 - What are the names of the people who had booked the most number children and babies for their stay? 
# (Don't worry if they canceled, only consider number of people reported at the time of their reservation)
hotels['total_kids'] = hotels['children'] + hotels['babies']
hotels[['name','adults','total_kids','children']].nlargest(3,'total_kids')


#Task 13 - What are the top 3 most common area code in the phone numbers? (Area code is first 3 digits)
hotels['phone-number'].str.split('-').apply(lambda x: x[0]).value_counts()[:3]


#Task 14 - How many arrivals took place between the 1st and the 15th of the month (inclusive of 1 and 15) ? 
# Bonus: Can you do this in one line of pandas code?
len(hotels[hotels['arrival_date_day_of_month'].between(1,15,inclusive = True)])


#Task 15 - Create a table for counts for each day of the week that people arrived. 
# (E.g. 5000 arrivals were on a Monday, 3000 were on a Tuesday, etc..)
d = {'Januray':1, 'February': 2, 'March': 3, 'April': 4, 'May':5, 'June':6, 'July':7,
    'August':8, 'September':9, 'October': 10, 'November': 11, 'December':12}

hotels['arrival_date_month'] = hotels['arrival_date_month'].map(d)

hotels['Day of the week'] = pd.to_datetime({'day': hotels['arrival_date_day_of_month'],
                                           'month':hotels['arrival_date_month'],
                                           'year':hotels['arrival_date_year']})

hotels['Day of the week'].dt.day_name().value_counts()

'''
def convert(day,month,year):
    return f'{day}-{month}-{year}'

hotels['date']  = np.vectorize(convert)(hotels['arrival_date_day_of_month'],
                                        hotels['arrival_date_month'],
                                        hotels['arrival_date_year'])

hotels['date'] = pd.to_datetime(hotels['date'])

hotels['date'].dt.day_name().value_counts()

'''