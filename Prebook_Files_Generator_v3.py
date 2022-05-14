"""
This project is an automatization of the process of creating the Pre-Books reports for all the countries in our SSC in Poznan.

The aim was to create a simple UI asking the user which country he/she needs the report for, detect the data source files and create the report.
This script has been prepared to handle most of the expected exceptions as missing data or incomplete reports. 

This app allows for only one user to create multiple reports in a matter of minutes, with little margin for errors while the only
demanding the correct data to be uploaded in the same folder where the app is located. It should perform in any folder provided that the
correct files are there.

"""

#Imports
import tkinter
from tkinter import *
from tkinter import messagebox
import pandas as pd
import datetime
import os

pd.options.mode.chained_assignment = None

#Redirecting the working directory to our current working directory 
dname = os.path.dirname(os.path.abspath(__file__))
os.chdir(dname)

#List of countries with environments/invoice sequences 
countries = {'Portugal': ['ILI  PB', 'TLI  PB', 'TLI  SN'],
             'France': ['I01  01', 'T01  01'],
             'UK': ['ICM  CM', 'TEA  EA'],
             'Netherlands': ['ICH  CH', 'TCH  CH', 'ICH  EY'],
             'Nordics': ['I31  31', 'I32  32', 'I33  33', 'I34  34', 'T31  31', 'T32  32', 'T33  33', 'T34  34'],
             'Belgium': ['TDA  EF', 'ICB  EF'],
             'Italy': ['TIG  IG', 'IIG  IG'],
             'Poland': ['TPA  PA', 'IPA  PA', 'TSS  SS'],
             'GERMANY & Austria': ['ISB  SB', 'ISD  SD', 'TSC  SD', 'ISE  SE'],
             'Spain': ['ITS  TS', 'TTS  TH', 'TTS  TS', 'TTS  OX']}

def get_countries(inv_seq):
    #Get the name of the country through the invoice sequence 
    return next((k for k, v in countries.items() if inv_seq[:7] in v), 'N/A')#List of countries with environments/invoice sequences 

def process_dates(data):
    #Transform the date format into a readable one
    return datetime.datetime.strptime(str(data), '%Y%m%d')

def overdues(date):
    #Function from the template example files
    return 'Overdue' if date < datetime.datetime.today() else 'Not overdue'

def age_of_invoice(date):
    #Calculates the days since the aof link was sent
    return abs(datetime.datetime.today() - date).days

def create_warning(text):
    #Generic function to return warnings to the user
    root = Tk()
    root.withdraw()
    root.geometry("300x200")
    w = Label(root, text ='teste', font = "50") 
    w.pack()
    messagebox.showwarning('Warning', text)
    root.destroy()

def check_for_files():

    list_of_files = []

    for root, dirs, files in os.walk(os.getcwd()):
            for file in files:
                if file[-5:] == '.xlsx' and file[0] == 'D':
                    list_of_files.append(file)
    
    if len(list_of_files) < 4:
        create_warning('The number of files is not enough, you need to provide data for both the transportation and the industrial environments for Approvals and Pre-books. The program will not continue.')
        return None, False
    else:
        return list_of_files, True

#From this point below until the main class, all of these functions are for the Pop Up window
opt = []

def chkbox_checked():
    for ix, item in enumerate(cb):
        opt[ix]=(cb_v[ix].get())
    return opt

def select_all():
    for i in cb:
        i.select()

def deselectall():
    for i in cb:
        i.deselect()

root = tkinter.Tk()  
root.title('Selection')

cb = []
cb_v = []

for ix, text in enumerate(countries.keys()):
    cb_v.append(tkinter.StringVar())
    off_value=0  #whatever you want it to be when the checkbutton is off
    cb.append(tkinter.Checkbutton(root, text=text, onvalue=text,offvalue=off_value,
                             variable=cb_v[ix],
                             command=chkbox_checked))
    cb[ix].grid(row=ix, column=0, sticky='w')
    opt.append(off_value)
    cb[-1].deselect() #uncheck the boxes initially.
label = Label(root, width=10)
label.grid(row=ix+1, column=0, sticky='w')
Button(root, text = 'Select all', command = select_all).grid(row = 12, column = 0)
Button(root, text = 'Deselect all', command = deselectall).grid(row = 13, column = 0)
Button(root, text = 'Submit', command= root.destroy).grid(row = 14, column = 0)
root.mainloop()

#Clearing the list of all unwanted items
list_of_countries = chkbox_checked()
list_of_countries  = list(set(list_of_countries))

if '0' in list_of_countries:
    list_of_countries.remove('0')


list_of_files, ok = check_for_files()

#### Main Class #### 
class Excel_Files():
    
    def __init__(self):
        
        #Creating the main files that separates pre-books and approvals
        self.dfs = {'Pre-books': [], 'Approvals': []}
        
        for file in list_of_files:

            df = pd.read_excel(file)

            #Looking for the overall dataframe
            if df.columns[0] == 'Country':
                self.all_invoices_df = df
            
            elif (df.columns[0] == 'From date'):
                
                df = df[df['Waiting'] == 'SIG ']

                #Assigning the country to each invoice
                df['Country'] = df['Barcode'].apply(get_countries)

                #Transform the AOF ID into string for better copy & paste to the system
                df['AOFid'] = df['AOFid'].apply(lambda x: f'00{str(x)}')

                #Re-arrange the table
                df['ENVSOC'] = df['Barcode'].apply(lambda x: x[:7])
                df['TYPE'] = df['Barcode'].apply(lambda x: x[7:12])
                df['INDEX'] = df['Barcode'].apply(lambda x: x[12:])

                    
                self.dfs['Approvals'].append(df)

            else:
                #Assigning the country to each invoice
                df['Country'] = df['ENVSOC'].apply(get_countries)

                #Transform the AOF ID into string for better copy & paste to the system
                df['AOFID'] = df['AOFID'].apply(lambda x: f'00{str(x)}')

                df = df.drop(['DATE','CPIECE'], axis = 1)
                df = df[df['STATUS'].isin(['6','3','D','0','L'])]
                self.dfs['Pre-books'].append(df)

    def join_tables(self):
        
        
        if len(self.dfs['Pre-books']) >= 1:
            self.dfs['Pre-books'] = pd.concat(self.dfs['Pre-books'], axis = 0)
        
        else:
            try:
                self.dfs['Pre-books'] = self.dfs['Pre-books'][0]
            except IndexError:
                create_warning('Some data might be missing. Prebook values seem to be none.')
            finally:
                self.dfs['Pre-books'] = pd.DataFrame(columns=['Overdue','Pre-book date','Invoice due date','ENVSOC', 
                                       'TYPE', 'INDEX', 'STATUS', 'DREG', 'JOUR', 'NOEF', 'LEADER',
                                       'NOFO', 'FAMFOU', 'LFOU', 'CMONT', 'DEVI', 'REF2', 'USER', 'DDAT',
                                       'IDAT', 'DECH', 'CERR', 'CDEM', 'USEREG', 'LPAYS', 'ISO2', 'NOCD',
                                       'CTVA001', 'CTVA002', 'CTVA003', 'CTVA004', 'CTRANS', 'MODR', 'FBAP',
                                       'TYAC', 'CD1/CDEM', 'AOFID', 'Country'])

        if len(self.dfs['Approvals']) >= 1:
            self.dfs['Approvals'] = pd.concat(self.dfs['Approvals'], axis = 0)
        
        else:
            try:
                self.dfs['Approvals'] = self.dfs['Approvals'][0]
            except IndexError:
                create_warning('Some data might be missing. Approval values seem to be none.')
            finally:
                self.dfs['Approvals'] = pd.DataFrame(columns=['Overdue','From date', 'Waiting', 'Barcode', 'AOFid', 'Jour', 'Regist number',
                                        'Cpiece', 'Supplier', 'Supplier name', 'Amount', 'Currency', 'User',
                                        'Reason', 'Date of scan', 'Due Date', 'Country','ENVSOC', 'TYPE', 'INDEX'])

    def calculate_dates(self):
        
        self.join_tables()
        #This function takes the string data from the columns and creates a new column with dates
        #To mirror the final report, the tables need to be re-arranged
        
        #Pre-books
        self.dfs['Pre-books']['Pre-book date'] = self.dfs['Pre-books']['DREG'].apply(process_dates)
        self.dfs['Pre-books']['Invoice due date'] = self.dfs['Pre-books']['DECH'].apply(process_dates)
        self.dfs['Pre-books']['Overdue'] = self.dfs['Pre-books']['Invoice due date'].apply(overdues)

        self.dfs['Pre-books'] = self.dfs['Pre-books'][['Overdue','Pre-book date','Invoice due date','ENVSOC', 
                                       'TYPE', 'INDEX', 'STATUS', 'DREG', 'JOUR', 'NOEF', 'LEADER',
                                       'NOFO', 'FAMFOU', 'LFOU', 'CMONT', 'DEVI', 'REF2', 'USER', 'DDAT',
                                       'IDAT', 'DECH', 'CERR', 'CDEM', 'USEREG', 'LPAYS', 'ISO2', 'NOCD',
                                       'CTVA001', 'CTVA002', 'CTVA003', 'CTVA004', 'CTRANS', 'MODR', 'FBAP',
                                       'TYAC', 'CD1/CDEM', 'AOFID', 'Country']]

        #Approvals
        self.dfs['Approvals']['From date'] = self.dfs['Approvals']['From date'].apply(process_dates)
        self.dfs['Approvals']['Due Date'] = self.dfs['Approvals']['Due Date'].apply(process_dates)

        self.dfs['Approvals']['Overdue'] = self.dfs['Approvals']['Due Date'].apply(overdues)
 
        self.dfs['Approvals'] = self.dfs['Approvals'][['Overdue','From date', 'Waiting', 'Barcode', 'AOFid', 'Jour', 'Regist number',
                                        'Cpiece', 'Supplier', 'Supplier name', 'Amount', 'Currency', 'User',
                                        'Reason', 'Date of scan', 'Due Date', 'Country','ENVSOC', 'TYPE', 'INDEX']]

        return
    
    def aof_holders(self):
        
        self.calculate_dates()
        
        #To create the dataframe for the aof holders, we need to concatenate the pre-books and approvals df's and create new columns to filter later
        
        self.dfs['Pre-books'].rename(columns = {'STATUS': 'Waiting', 'NOFO': 'Supplier', 
                                                'NOFO': 'Supplier', 
                                                'LFOU': 'Supplier name',
                                                'CERR': 'Reason',
                                                'CDEM': 'User',
                                                'AOFID': 'AOFid'}, inplace = True)

        df_aof_holders_pbk = self.dfs['Pre-books'][['ENVSOC', 'TYPE', 'INDEX', 'Waiting', 'Supplier', 'Supplier name', 'Reason', 'User', 'AOFid', 'Country']]
        df_aof_holders_pbk['Date of AOF sending'] = self.dfs['Pre-books']['Pre-book date']


        df_aof_holders_app = self.dfs['Approvals'][['ENVSOC', 'TYPE', 'INDEX', 'Waiting', 'Supplier', 'Supplier name', 'Reason', 'User', 'AOFid', 'Country']]
        df_aof_holders_app['Date of AOF sending'] = self.dfs['Approvals']['From date']
        
        self.aof_holder = pd.concat([df_aof_holders_pbk,df_aof_holders_app])
        
        self.aof_holder['Days since link was sent'] = self.aof_holder['Date of AOF sending'].apply(age_of_invoice)
        
        return

    def sum_up_table(self, country):
        #This function will make a sum up of all invoices for that specific country, including the ones in fresh + suspended
        try:
            #First thing is to remove spaces and replace some countrie's names to link correctly with the each dictionary key
            self.all_invoices_df['Country'] = self.all_invoices_df['Country'].apply(lambda x: x.replace(" ",""))
            self.all_invoices_df['Country'][self.all_invoices_df['Country'].isin(['Sweden', 'Finland', 'Denmark', 'Norway'])] = 'Nordics'
            self.all_invoices_df['Country'][self.all_invoices_df['Country'].isin(['GERMANY', 'Austria'])] = 'GERMANY & Austria'

            #Adding Poland which is absent from the dataframe, assuming values as 0 because true data is unknown
            poland = {'Country': 'Poland'}

            for item in self.all_invoices_df.columns[1:]:
                poland[item] = 0

            self.all_invoices_df.append(poland, ignore_index = True)

            #Calculating the variables for the table
            invoices_in_fresh = sum(self.all_invoices_df[self.all_invoices_df['Country'] == country]['Fresh'])
            invoices_in_suspended = sum(self.all_invoices_df[self.all_invoices_df['Country'] == country]['Suspended'])
            
        except AttributeError:
            create_warning('You did not provide the file with the number of fresh invoices and invoices in suspended. These values will be considered as 0.')
            invoices_in_fresh = 0
            invoices_in_suspended = 0
            
        finally:
            invoices_waiting_for_response = len(self.dfs['Pre-books'][(self.dfs['Pre-books']['Country'] == country) & (self.dfs['Pre-books']['Waiting'].isin(['6','D']))])
            invoices_waiting_SSC_action = len(self.dfs['Pre-books'][(self.dfs['Pre-books']['Country'] == country) & (self.dfs['Pre-books']['Waiting'] == '3')])

            total_invoices_to_be_booked = invoices_in_fresh + invoices_in_suspended + invoices_waiting_for_response + invoices_waiting_SSC_action

            status_L = len(self.dfs['Pre-books'][(self.dfs['Pre-books']['Country'] == country) & (self.dfs['Pre-books']['Waiting'] == 'L')])
            status_0 = len(self.dfs['Pre-books'][(self.dfs['Pre-books']['Country'] == country) & (self.dfs['Pre-books']['Waiting'] == '0')])
            litigations = status_0 + status_L

            status_5 = len(self.dfs['Approvals'][self.dfs['Approvals']['Country'] == country])

            #Finally creating the Sum Up dataframe

            self.final_sum_up = pd.DataFrame([invoices_in_fresh, invoices_in_suspended, invoices_waiting_for_response, invoices_waiting_SSC_action,
                                        total_invoices_to_be_booked,
                                        "",
                                        status_L,
                                        status_0,
                                        litigations,
                                        "",
                                        status_5], index = ['Total number of fresh scanned invoice (Status 1)',
                                                            'Total number of suspended invoices (Status 2)',
                                                            'Invoices waiting for respond (Status 6 and D)',
                                                            'Invoices responded waiting for SSC action (Status 3)',
                                                            'Total of invoices to book',
                                                            "",
                                                            'Pre-booking Litigation (Status L)',
                                                            'Litigation (Status 0)',
                                                            'Total invoices to be reviewed',
                                                            "",
                                                            'Total Number of invoices pending approval (Status 5)'], columns = [country])

        return self.final_sum_up
        
    def create_excel_files(self):
        
        self.aof_holders()
        
        #Finally we print the Excel files with the data processed

        length = len(list_of_countries)

        for i in range(length):
        
            file_title =  f'{list_of_countries[i]}_{str(datetime.datetime.today())[:10]}.xlsx'

            final_file = pd.ExcelWriter(file_title, engine = 'xlsxwriter', 
                                        date_format = 'YYYY-MM-DD')

            self.sum_up_table(list_of_countries[i]).to_excel(final_file, sheet_name = 'Sum Up')
            self.dfs['Pre-books'][self.dfs['Pre-books']['Country'] == list_of_countries[i]].to_excel(final_file, sheet_name = 'Pre-books', index = False)
            self.dfs['Approvals'][self.dfs['Approvals']['Country'] == list_of_countries[i]].to_excel(final_file, sheet_name = 'Approvals', index = False)
            self.aof_holder[(self.aof_holder['Days since link was sent'] > 15) & (self.aof_holder['Country'] == list_of_countries[i])].sort_values('Days since link was sent', ascending = False).to_excel(final_file, sheet_name = 'AOF Holders', index = False)
            
            final_file.save()
            final_file.close()
        
        if length != 0:
            create_warning('All actions completed.')

#Execute the program
if __name__ == '__main__' and ok:
    Excel_Files().create_excel_files()