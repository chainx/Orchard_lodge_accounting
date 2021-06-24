from Dependencies import *

path_to_invoices = '/media/mike/E8/Orchard lodge accounting/Invoices/'

file = open('Data/Payment_filters.pkl','rb')
Payment_filters = pickle.load(file)
file.close()

def compare_spelling(name,names): #This method doesn't work if there is a misspelling within the first few characters
    total = len(list(name))
    closest_match=['Name',0] #Name, percentage of matching characters
    
    for comparison_name in names:
        count = 0
        for n in range(min(total,len(list(comparison_name)))):
            if list(name)[n] == list(comparison_name)[n]: count+=1 #Check how many characters match

        if float(count/total) > closest_match[1]: closest_match = [comparison_name,float(count/total)]

    return closest_match

def init_residents(year_range):
    residents = []
    names_and_titles = {} #Dictionary with name as key and title as value
    for year in year_range:
        for folder_name in os.listdir(path_to_invoices + year):
            for filename in os.listdir(path_to_invoices + year + '/' + folder_name):

                if len(filename.split(' - '))>2: print('There is an issue with the following filename: ',filename) #Check for errors in formating filename


                name = filename.split(' - ')[1].split('.docx')[0].split(' [OBSOLETE]')[0]
                title = ''
                if name.split()[0] in ['Mr','Mrs', 'Ms', 'Miss']: #If name has a title, split title from name
                    title = name.split()[0]
                    name = ' '.join(name.split()[1:])

                    
                comparison = compare_spelling(name, names_and_titles)
                if 0.7 < comparison[1] < 1: #Check for misspelling, there must be a greater than 70% match between all the individual characters
                    print(name,'  -  ',comparison[0],':  ',str(comparison[1]*100)+'% match between spellings')

                          
                if name not in names_and_titles: names_and_titles.update({name : title})
                if name in names_and_titles and title!='': names_and_titles.update({name : title})  #Update name entry if a title has now been provided        

    for name in names_and_titles: residents.append(resident(name,names_and_titles[name])) #Create resident instances with name and title
    residents = sorted(residents, key=lambda x: x.name.split(" ")[-1]) #Sort alphabetically by last name

    residents.append(resident('Cheques','')) #Add "resident" corresponding to cheque payments
    return residents


def add_debts(year_range):
    for year in year_range:
        for folder_name in os.listdir(path_to_invoices + year):
            for filename in os.listdir(path_to_invoices + year + '/' + folder_name):
                for res in residents:
                    if res.name in filename and '[OBSOLETE]' not in filename: #Don't add obsolete debts
                        res.debts.append( read_invoice(path_to_invoices+year+'/'+folder_name+'/'+filename) )

def add_bank_payments(year_range): #Sort payments from Santander file into resident instances
    unsorted_payments=[]
    
    statement = read_data('Data/Santander statement.csv')
    for payment in statement: #Move through each payment within the date range and check if it contains any of the filters
        if datetime(int(year_range[0]),1,1) < datetime.strptime(payment[0],'%d/%m/%Y') < datetime(int(year_range[-1])+1,1,1): 
            
            matched_residents=[]
            for res in residents: #Check to see if the payment matches the filters of any of the residents
                if find(payment[1],res.filters):
                    res.payments.append(payment)
                    matched_residents.append(res.name)

            #Find payments which don't match any filters
            if matched_residents==[] and float(payment[2])>0: unsorted_payments.append(payment)
            if len(matched_residents)>1: print('This piece of data has been double counted!\n',payment,'\n',matched_residents,'\n')
            
    return unsorted_payments

def add_cash_payments(year_range):
    cash_payments = []
    filters=['miljana','refund','santander']
    data = read_data('Data/RBS statement.csv')
    for payment in data:
        if find(payment[1],filters)==False and float(payment[2])>0 and datetime(int(year_range[0]),1,1) < datetime.strptime(payment[0],'%d/%m/%Y') < datetime(int(year_range[-1])+1,1,1): 
            cash_payments.append(payment)#payments.update( {'Cash + Cheques' : payments['Cash + Cheques']+[payment]} )
    return cash_payments

def add_jeanette_payments(year_range):
    for year in year_range:
        df = pandas.read_excel('Data/Cash and cheques/Cash and cheques ' + year + '.xlsx')
        for i in df.index:
            if df['Bank'][i]=='Santander' or df['Bank'][i]=='RBS':
                date = "/".join(str(df['Date'][i]).split(' ')[0].split('-')[::-1])
                invoice_number = '00'+str(df['Invoice number'][i]).split('.')[0] #Invoice number must be less than 1000
                if math.isnan(df['Invoice number'][i]): invoice_number=''
                payment = [date,str(df['Resident'][i]),df['Amount'][i],invoice_number] 

                
                for res in residents:
                    if res.title+' '+res.name == df['Resident'][i]: res.payments.append(payment)


#==============================================================================           EXECUTE CODE               =============================================================================================================


year_range = ['2019','2020','2021']
residents = init_residents(year_range)

add_debts(year_range)
unsorted_payments = add_bank_payments(year_range)
cash_payments = add_cash_payments(year_range)
add_jeanette_payments(year_range)

for res in residents: res.order_debts_and_payments() #Order debts and payments by date
for payment in residents[-1].payments: print(payment) #Print cheque payments
residents = {resident.name : resident for resident in residents} #Store the resident instances in a dictionary for easy access, must be done after sorting


if __name__ == "__main__":

    residents['Joan Baskeyfield'].line_up_debts_and_payments()
    residents['Joan Baskeyfield'].total_owed()  

##    file = open('Residents.pkl','wb')
##    pickle.dump(residents, file)
##    file.close()
##
##    file = open('Payment_filters.pkl','wb')
##    pickle.dump(Payment_filters, file)
##    file.close()

     
    





