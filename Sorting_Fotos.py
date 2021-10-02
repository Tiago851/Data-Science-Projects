"""
Recently I made a backup of all the photos on my cellphone to a folder in my computer. I noticed that
most of the files had a pattern in the name that could be filtered and sorted with a simple Python
script.

The aim was to sort the files this way: Year > Month > Day

Each photo was renamed with the day of the month it was taken. In case several photos were taken on the same day,
the script is prepared to handle it and it has instructions to add the hour of the photo (format hourminutesecond)

"""

#Modules
import os
import shutil

#Original location of the photos
main_path = r'C:\Users\Utilizador\Desktop\Fotos'

#Main loop
for file in os.listdir(main_path):
    
    #Storing the original file name
    original_file_name = file
    
    if os.path.splitext(file)[1] in ['.jpg','.jpeg']:
        
        if file[:4] == 'IMG-':
            file = file[4:]
        
        #Important variables for each photo
        year = file[:4]
        month = file[4:6]
        day =  file[6:8]

        if year in ['2019','2020','2021']:
            
            #Days of the month
            d = {'01': 'Janeiro', 
             '02': 'Fevereiro', 
             '03': 'Março', 
             '04': 'Abril',
             '05': 'Maio',
             '06': 'Junho',
             '07': 'Julho',
             '08': 'Agosto',
             '09': 'Setembro',
             '10': 'Outubro',
             '11': 'Novembro',
             '12': 'Dezembro'}
            
            #Redefining the month for concatenation
            month = d[month]

            #Destination directory for each photo
            dst_path = f'C:\\Users\\Utilizador\Desktop\\Fotos2\\{year}\\{month}'

            #Checking if the above destination directory already exists, creating it in case it doesn't
            if os.path.exists(dst_path) == False:
                
                os.mkdir(dst_path)

            else:
                
                #Source + Destination path for each file
                img_src_path = main_path + '\\' + original_file_name
                img_dst_path = dst_path + '\\' + original_file_name
                
                #Moving the files
                shutil.move(img_src_path, img_dst_path)
                
                #Renaming the photos
                new_name = dst_path + '\\' + day + '.jpg'
                
                #Exception handling for the file name
                try:
                    os.rename(img_dst_path, new_name)
                    
                except FileExistsError:
                    day = file[6:]
                    new_name = dst_path + '\\' + day + '.jpg'
                
                finally:
                    os.rename(img_dst_path, new_name)