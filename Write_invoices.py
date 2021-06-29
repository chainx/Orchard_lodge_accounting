from Dependencies import *

def combine_payments(info):
    payments=[]
    temp=[info[0][0],[]]
    for n in range(len(info)):
        if info[n][0]==temp[0]: temp[1].append([info[n][1].replace('-',''),info[n][2],info[n][3]])
        if info[n][0]!=temp[0] or n==len(info)-1:
            total=0
            for payment in temp[1]: total+=float(payment[0])
            temp.append(str(total))
            payments.append(temp)
            temp=[info[n][0],[[info[n][1].replace('-',''),info[n][2],info[n][3]]]]
            if n==len(info)-1: #Phillip wycherly only has one payment
                temp.append(temp[1][0][0])
                payments.append(temp)
    return payments
            

def write_inovices(payments,date,year):
    file = open('Invoices/Invoice number.txt', 'r') #Get invoice number
    invoice_number = file.readline()
    file.close()

    for resident in payments: #Payments should be a dictionary indexed by resident name
        document = Document('Invoices/INVOICE TEMPLATE.DOCX')

        for paragraph in document.paragraphs:
            if paragraph.text.count("INVOICE NUMB")==1: paragraph.text=paragraph.text.replace("INVOICE NUMB",invoice_number)
            if paragraph.text.count("DATE TODAY")==1: paragraph.text=paragraph.text.replace("DATE TODAY",date)
            if paragraph.text.count("NAME OF RECIPIENT")==1: paragraph.text=paragraph.text.replace("NAME OF RECIPIENT",resident[0])

        count=0
        for payment in resident[1]:            
            paragraph = document.tables[0].cell(0,0).paragraphs[7+count]
            reason=''
            if payment[2]!='' and payment[2]!='MA': reason=' ('+payment[2]+')'
            paragraph.text='From ' + payment[1] + reason
            
            paragraph =  document.tables[0].cell(0,1).paragraphs[8+count]
            paragraph.text=chr(163)+"{:.2f}".format(float(payment[0])) #Write number with two decimal places
            count+=1

        for paragraph in document.tables[0].cell(1,1).paragraphs:
            if paragraph.text.count('TOTAL')==1: paragraph.text=paragraph.text.replace('TOTAL',"{:.2f}".format(float(resident[2])))

        document.save('Invoices/'+year+'/'+str(N)+'. '+date+'/'+invoice_number+' - '+resident[0]+'.docx')
        invoice_number = "%05d" % (int(invoice_number)+1,)
        
    file = open('Invoices/Invoice number.txt', 'w') #Update invoice number
    file.write(invoice_number)
    file.close()

#==============================================================================================================================================================================

#Calculate today's date
now = datetime.now()
year = now.strftime("%Y")
date= now.strftime("%d")+' '+now.strftime("%B")+' '+now.strftime("%Y")


#==============================================================================================================================================================================

#GOALS:
#    -ADD FUNCTIONALITY FOR AUTOMATICALLY MOVING THE FILES FROM THE DOWNLOADS FOLDER AND RENAMING THEM
#    -CREATE ERROR CORRECTION FOR MULTIPLE INVOICES PER RESIDENT (FOR INSTANCE P WYCHERLY IN 04/21)

N=len(glob.glob('Remittance advice/'+year+'/*.csv')) 
statement=''
for file in glob.glob('Remittance advice/'+year+'/*.csv'):
    if int(file.split('/')[2].split('.')[0])==N: statement=file #file.split('/')[1].split('.')[0] is the file number

#==============================================================================================================================================================================


info=read_sefton_file(statement) #Read Sefton's csv file        
payments=combine_payments(info) #Collect payments for each resident for invoicing

payment_date = payments[len(payments)-1][1][0][1] #P. W is last and never has anomalies so is useful for getting the date

#Private residents



for resident in payments:
    print(resident[0])
    for payment in resident[1]: print(payment)
    print('Total for client is '+resident[2]+'\n')

safety_check=input('Do you want to continue? (y/n)  ')
if safety_check=='y':
    os.makedirs('Invoices/'+year+'/'+str(N)+'. '+date) #Create new folder
    write_inovices(payments,date,year) #Write invoices
else: print('\n'*3+'Invoice writing aborted!')
