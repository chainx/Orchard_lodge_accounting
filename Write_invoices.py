from Dependencies import *

def order_debts(debts):
    residents={}
    for debt in debts:
        if debt[0] not in residents: #debt[0] is the resident's name
            residents[debt[0]] = resident(debt[0],'')
        residents[debt[0]].debts.append(debt[1:]) #[1:] to cut redundant name entry        

    for res in residents: #Calculate invoice total
        for debt in residents[res].debts:
            residents[res].invoice_total+=float(debt[0])
        residents[res].invoice_total = "{:.2f}".format(residents[res].invoice_total)
        
    return residents
            

def write_inovices(residents,date,year,file_number):
    file = open(path+'Invoices/Invoice number.txt', 'r') #Get invoice number
    invoice_number = file.readline()
    file.close()

    for res in residents:
        document = Document(path+'Invoices/INVOICE TEMPLATE.DOCX')

        for paragraph in document.paragraphs:
            if paragraph.text.count("INVOICE NUMB")==1: paragraph.text=paragraph.text.replace("INVOICE NUMB",invoice_number)
            if paragraph.text.count("DATE TODAY")==1: paragraph.text=paragraph.text.replace("DATE TODAY",date)
            if paragraph.text.count("NAME OF RECIPIENT")==1: paragraph.text=paragraph.text.replace("NAME OF RECIPIENT",res)

        count=0
        for debt in residents[res].debts:            
            paragraph = document.tables[0].cell(0,0).paragraphs[7+count]

            reason=''
            if debt[2]!='' and debt[2]!='MA': reason=' ('+debt[2]+')'
            paragraph.text='From ' + debt[1] + reason
            
            paragraph =  document.tables[0].cell(0,1).paragraphs[8+count]
            paragraph.text=chr(163)+str(debt[0])
            count+=1

        for paragraph in document.tables[0].cell(1,1).paragraphs:
            if paragraph.text.count('TOTAL')==1: paragraph.text=paragraph.text.replace('TOTAL',res.invoice_total)

        document.save(path+'Invoices/'+year+'/'+str(file_number)+'. '+date+'/'+invoice_number+' - '+res+'.docx')
        invoice_number = "%05d" % (int(invoice_number)+1,)
        
    file = open(path+'Invoices/Invoice number.txt', 'w') #Update invoice number
    file.write(invoice_number)
    file.close()


#==============================================================================================================================================================================

path = '/media/mike/E8/Orchard lodge accounting/'

if __name__ == "__main__":

    #Calculate today's date
    now = datetime.now()
    year = now.strftime("%Y")
    date = now.strftime("%d %B %Y")

    if 'report_export.csv' in os.listdir('/home/mike/Downloads'):

        (debts,debt_date) = read_sefton_file("/home/mike/Downloads/report_export.csv")

        dates = [datetime.strptime(date,'%d/%m/%Y').strftime('%d %B') for date in debt_date.split(' to ')]
        file_number = int(len(os.listdir(path+"Remittance advice/"+year))/2) + 1
        filename = str(file_number) + '. ' + dates[0] + ' - ' + dates[1]


    #Private residents
    file = open(path+'Source code/Data/Private_residents.pkl','rb')
    private_residents = pickle.load(file)
    file.close()
    for res in private_residents:
        debts.append([res[0],res[1],debt_date,''])


    residents = order_debts(debts) #Orders debts by resident and calculates the total

    
    #Printing invoices for manual error check
    for res in residents:
        print(res)
        for debt in residents[res].debts: print(debt)
        print('Total for client is '+residents[res].invoice_total+'\n')


    #Checking before proceding to write invoices
    safety_check=input('Do you want to continue? (y/n)  ')
    if safety_check=='y':
        os.makedirs(path+'Invoices/'+year+'/'+str(file_number)+'. '+date) #Create new folder
        write_inovices(debts,date,year,file_number)                       #Write invoices
        shutil.move("/home/mike/Downloads/report_export.csv", path+'Remittance advice/'+year+'/'+filename+'.csv')
        shutil.move("/home/mike/Downloads/ActiveReports.PDF", path+'Remittance advice/'+year+'/'+filename+'.PDF')
        
    else: print('\n'*3+'Invoice writing aborted!')
