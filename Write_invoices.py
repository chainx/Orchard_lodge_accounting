from Dependencies import *

path = '/media/mike/E8/Orchard lodge accounting/'

def combine_debts(info):
    debts=[]
    temp=[info[0][0],[]]
    for n in range(len(info)):
        if info[n][0]==temp[0]: temp[1].append([info[n][1].replace('-',''),info[n][2],info[n][3]])
        
        if info[n][0]!=temp[0] or n==len(info)-1:
            total=0
            for payment in temp[1]: total+=float(payment[0])
            temp.append("{:.2f}".format(total))
            debts.append(temp)
            
            temp=[info[n][0],[[info[n][1].replace('-',''),info[n][2],info[n][3]]]]
            
            if n==len(info)-1: #Phillip wycherly only has one payment
                temp.append(temp[1][0][0])
                debts.append(temp)
    return debts
            

def write_inovices(debts,date,year,file_number):
    file = open(path+'Invoices/Invoice number.txt', 'r') #Get invoice number
    invoice_number = file.readline()
    file.close()

    for resident in debts: #debts should be a dictionary indexed by resident name
        document = Document(path+'Invoices/INVOICE TEMPLATE.DOCX')

        for paragraph in document.paragraphs:
            if paragraph.text.count("INVOICE NUMB")==1: paragraph.text=paragraph.text.replace("INVOICE NUMB",invoice_number)
            if paragraph.text.count("DATE TODAY")==1: paragraph.text=paragraph.text.replace("DATE TODAY",date)
            if paragraph.text.count("NAME OF RECIPIENT")==1: paragraph.text=paragraph.text.replace("NAME OF RECIPIENT",resident[0])

        count=0
        for debt in resident[1]:            
            paragraph = document.tables[0].cell(0,0).paragraphs[7+count]

            reason=''
            if debt[2]!='' and debt[2]!='MA': reason=' ('+debt[2]+')'
            paragraph.text='From ' + debt[1] + reason
            
            paragraph =  document.tables[0].cell(0,1).paragraphs[8+count]
            paragraph.text=chr(163)+str(debt[0])
            count+=1

        for paragraph in document.tables[0].cell(1,1).paragraphs:
            if paragraph.text.count('TOTAL')==1: paragraph.text=paragraph.text.replace('TOTAL',str(resident[2]))

        document.save(path+'Invoices/'+year+'/'+str(file_number)+'. '+date+'/'+invoice_number+' - '+resident[0]+'.docx')
        invoice_number = "%05d" % (int(invoice_number)+1,)
        
    file = open(path+'Invoices/Invoice number.txt', 'w') #Update invoice number
    file.write(invoice_number)
    file.close()


#==============================================================================================================================================================================

if __name__ == "__main__":

    #Calculate today's date
    now = datetime.now()
    year = now.strftime("%Y")
    date = now.strftime("%d %B %Y")

    if 'report_export.csv' in os.listdir('/home/mike/Downloads'):

        (debts,debt_date) = read_sefton_file("/home/mike/Downloads/report_export.csv")

        dates = [datetime.strptime(date,'%d/%m/%Y').strftime('%d %B') for date in debt_date.split(' to ')]
        file_number = int(len(os.listdir("/media/mike/E8/Orchard lodge accounting/Remittance advice/"+year))/2) + 1
        filename = str(file_number) + '. ' + dates[0] + ' - ' + dates[1]
        

    debts = combine_debts(debts) #Combines debts for the same resident and calculates the total

    #Private residents
    debts.append( ['Mrs Barbara Kelleher', [['2200', debt_date, '']], '2200'] )
    debts.append( ['Mrs Everlyn Bailey', [['2160', debt_date, '']], '2160'] )
    debts.append( ['Mrs Eleanor Cronin', [['2200', debt_date, '']], '2200'] )
    debts.append( ['Mrs Veronica Curley', [['2200', debt_date, '']], '2200'] )
    debts.append( ['Mr Ronald Taylor', [['2200', debt_date, '']], '2200'] )


    #Printing invoices for manual error check
    for resident in debts:
        print(resident[0])
        for payment in resident[1]: print(payment)
        print('Total for client is '+resident[2]+'\n')


    #Checking before proceding to write invoices
    safety_check=input('Do you want to continue? (y/n)  ')
    if safety_check=='y':
        os.makedirs(path+'Invoices/'+year+'/'+str(file_number)+'. '+date) #Create new folder
        write_inovices(debts,date,year,file_number)                       #Write invoices
        shutil.move("/home/mike/Downloads/report_export.csv", path+'Remittance advice/'+year+'/'+filename+'.csv')
        shutil.move("/home/mike/Downloads/ActiveReports.PDF", path+'Remittance advice/'+year+'/'+filename+'.PDF')
        
    else: print('\n'*3+'Invoice writing aborted!')
