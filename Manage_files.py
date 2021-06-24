from Dependencies import *

def correct_invoice_number(invoice_number):
    file = open('Invoices/Invoice number.txt', 'w') #Update invoice number
    file.write(invoice_number) #For example '00843'
    file.close()

def copy_debts(year_range):
    for res in residents: #Create folder for resident if there isn't already one
        if res.name.lower() not in [folder.lower() for folder in os.listdir('Invoices/Invoices sorted by resident')]:
            os.makedirs('Invoices/Invoices sorted by resident/'+res.name)

    print('Copying starting')
    for year in year_range:
        for folder_name in os.listdir('Invoices/'+year):
            for filename in os.listdir('Invoices/'+year+'/'+folder_name):
                matched = False
                for res in residents:                   
                    if res.name in filename:
                        copyfile('Invoices/'+year+'/'+folder_name+'/'+filename, 'Invoices/Invoices sorted by resident/'+res.name+'/'+filename )
                        matched = True
                if matched==False: print(filename,'was not matched with any residents')
    print('Copying finished')   

