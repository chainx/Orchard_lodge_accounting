from Dependencies import *

def line_up_statements(data,new_data):
    join_point=0 #data[:join_point-1] represents the the earlier payments in new_data
    while new_data[join_point] in data or join_point==len(new_data): join_point+=1

    ammended_data = new_data[:join_point-1]+data #Earlier payments are further into the list
    manual_error_check(data,new_data,join_point,ammended_data)
    return ammended_data

def manual_error_check(data,new_data,join_point,ammended_data):
    N=6   #Number of payments around the join point to print for manual error check    
    n=N   #Ensures that N isn't large enough to cause list index errors later (and scales it down if so)
    while join_point-n<0 or join_point+n>len(new_data): n-=1

    data_type = 'main'
    new_data_type = 'downloaded'
    if datetime.strptime(data[0][0], "%d/%m/%Y") > datetime.strptime(new_data[0][0], "%d/%m/%Y"):
        data_type = 'downloaded'
        new_data_type = 'main'

    print('The ammended data set runs from '+data[::-1][0][0]+' to '+new_data[0][0])
    print('\nHere around some payments near the join in the '+new_data_type+' data\n')
    for i in range(2*n-1):
        if i==n-1:
            color.write(new_data[join_point-n+i],"STRING") #Print with green colour
            print()
        else: print(new_data[join_point-n+i])

    print(3*'\n' + 'Here around some payments near the join in the '+data_type+' data\n')
    color.write(data[0],"STRING") #Print with green colour
    print()
    for i in range(1,n): print(data[i])

    duplicates=[] #Find duplicate payments
    for i in range(len(ammended_data)):
        for j in range(len(ammended_data)):
            if ammended_data[i]==ammended_data[j] and i!=j and ammended_data[i] not in duplicates: duplicates.append(ammended_data[i])
    if len(duplicates)>0:
        print(3*'\n' + 'The followings payments are duplicates in the data set\n')
        for payment in duplicates: print(payment)
        print()


def merge_statements(main_filename,downloaded_filename,san_or_rbs):
    data = read_data(main_filename)
    new_data = read_bank_statement(downloaded_filename,san_or_rbs)

    ammended_data = []
    if data[0] in new_data: ammended_data = line_up_statements(data,new_data) #Determine which data contains newer entries
    elif new_data[0] in data : ammended_data = line_up_statements(new_data,data)
    else: print("Error, the two data sets don't overlap")

    safety_check=input('Update bank statement? (y/n)  ')
    if safety_check=='y': write_data(ammended_data,main_filename)

    safety_check=input('Remove obsolete file? (y/n)  ')
    if safety_check=='y': os.remove(downloaded_filename)



if __name__ == "__main__":
    
    for filename in os.listdir('/home/mike/Downloads'):
        if 'KISSMTAORCHARD' in filename:
            print('Merging RBS statements:')
            merge_statements('RBS statement.csv','/home/mike/Downloads/'+filename,'rbs')
        print('\n\n\n')
        if 'Statements0' in filename:
            print('Merging Santander statements:')
            merge_statements('Santander statement.csv','/home/mike/Downloads/'+filename,'san')


