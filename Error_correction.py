from Basic_functions import *
from Reading import read_invoice
import Verify_payments

def verify_jeanettes_accounting(year,payments,check_bank=True,check_entries=True):
    df = pandas.read_excel('Paying in sheets/Cash and cheques '+str(year)+'.xlsx')

    #Part 1: check payments in bank match amounts given by Jeanette
    if check_bank==True:
        print('The following is a list of payments in the cash and cheques sheet compared with payments into RBS and Santander:','\n'*3) 
        unaccounted_for = payments['Cash + Cheques'][:]
        error_margin = 50 #20 is an arbitrary number
        for i in df.index:
            if df['Bank'][i]=='Total':
                date = "/".join(str(df['Date'][i-1]).split(' ')[0].split('-')[::-1])
                total = df['Resident'][i]
                jeanette_payment = [date,'',total]

                if total>0: #Some of the payments were paid out to staff so won't be found in the bank statements
                    payment = min(unaccounted_for, key=lambda x: error(x,jeanette_payment) )
                    if error(payment,jeanette_payment)<error_margin:
                         print([date,total], ' '*(30-len(str(jeanette_payment))), payment)
                         unaccounted_for.remove(payment) #Remove payment from unaccounted for list if its sufficiently close to one of Jeanette's payments
                    else:
                        print('\nThere is no corresponding bank payment for the following payment:',jeanette_payment,'\n')

        print('\n'*4,'The following payments are unaccounted for:\n')
        for payment in [payment for payment in unaccounted_for if datetime(year,1,1) < datetime.strptime(payment[0], "%d/%m/%Y") < datetime(year+1,1,1)]: print(payment)

    #Part 2: Check invoice numbers and payment amounts match those given by Jeanette
    if check_entries==True:
        if check_bank==True: print('\n'*5)
        print('Here are the payments in the cash and checks sheet which contain errors:','\n'*2)
        for i in df.index:
            if df['Bank'][i]=='Santander' or df['Bank'][i]=='RBS':
                date = "/".join(str(df['Date'][i]).split(' ')[0].split('-')[::-1])
                resident = str(df['Resident'][i])
                amount = df['Amount'][i]
                if math.isnan(df['Invoice number'][i])==False:
                    invoice_number = '00'+str(int(df['Invoice number'][i]))
                    invoice = read_invoice(find_invoices(invoice_number)[0])
                    if resident!=invoice[1] or amount!=invoice[2]:
                        print('Payment in sheet      =', [date,resident,amount,invoice_number])
                        print('Corresponding invoice =', invoice,'\n')


def line_up_dates(resident,verbose=False):
    dates_by_filename={}
    for filename in find_invoices(resident):
        if 'OBSOLETE' not in filename:
            dates_by_filename.update({filename : []})
        
            document = Document(filename)
            for paragraph in document.tables[0].cell(0,0).paragraphs:                
                if paragraph.text.count("From")>0:

                    date = [datetime.strptime(paragraph.text.split(' ')[1],'%d/%m/%y'), datetime.strptime(paragraph.text.split(' ')[3],'%d/%m/%y')]
                    dates_by_filename.update({filename : dates_by_filename[filename]+[date]})

                    if verbose==True: #Check dates are all formatted correctly
                        if paragraph.text.count("Adj")>0: color.write(filename+'\n'+paragraph.text+'\n',"STRING")
                        else: print(paragraph.text)

    if verbose==True: print()
    #dates = [date for filename in dates_by_filename for date in dates_by_filename[filename]]
    for filename1 in dates_by_filename:
        for date1 in dates_by_filename[filename1]:
            for filename2 in dates_by_filename:
                for date2 in dates_by_filename[filename2]:
                    
                    if date1!=date2 and (date2[0] < date1[0] < date2[1] or date2[0] < date1[1] < date2[1]):
                        print('From ' + date1[0].strftime('%d/%m/%y') + ' to ' + date1[1].strftime('%d/%m/%y') + '\n' + filename1)
                        print('From ' + date2[0].strftime('%d/%m/%y') + ' to ' + date2[1].strftime('%d/%m/%y') + '\n' + filename2,'\n\n')



if __name__ == "__main__":

    name = 'Eleanor Cronin'
    resident = Verify_payments.residents[name]
    resident.debts = [debt for debt in resident.debts if datetime.strptime(debt[0],'%d/%m/%Y')>datetime(2019,12,1)]

    line_up_dates(name)#,True)

##    print(name + ' has the following payments:')
##    resident.print_payments()
##    print('\nand the following debts:')
##    resident.print_debts()
##    print('\nTotal owed by ' + name + ' is:',resident.total_owed())
