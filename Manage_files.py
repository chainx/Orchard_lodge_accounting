from Dependencies import *

path = '/media/mike/E8/Orchard lodge accounting/'

def correct_invoice_number(invoice_number):
    file = open(path+'Invoices/Invoice number.txt', 'w') #Update invoice number
    file.write(invoice_number) #For example '00843'
    file.close()

def organise_debts(year_range): #Sort the invoices into folders indexed by resident name
    for res in residents: 
        if res.name.lower() not in [folder.lower() for folder in os.listdir(path+'Invoices/Invoices sorted by resident')]:
            os.makedirs(path+'Invoices/Invoices sorted by resident/'+res.name) #Create folder for resident if there isn't already one

    print('Copying starting')
    for year in year_range:
        for folder_name in os.listdir(path+'Invoices/'+year):
            for filename in os.listdir(path+'Invoices/'+year+'/'+folder_name):
                matched = False
                for res in residents:                   
                    if res.name in filename:
                        copyfile(path+'Invoices/'+year+'/'+folder_name+'/'+filename, path+'Invoices/Invoices sorted by resident/'+res.name+'/'+filename )
                        matched = True
                if matched==False: print(filename,'was not matched with any residents')
    print('Copying finished')   
