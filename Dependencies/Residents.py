from datetime import datetime

def error(payment1,payment2): #Used for lining up payments
    time_difference = abs((datetime.strptime(payment1[0],'%d/%m/%Y')-datetime.strptime(payment2[0],'%d/%m/%Y')).days)
    amount_difference = abs(float(payment1[2]) - float(payment2[2]))
    return time_difference + amount_difference



class resident:
    def __init__(self,name,title,filters=[]): 
        self.name = name
        self.title = title

        self.filters = filters

        self.debts = []
        self.payments = []

    def print_debts(self):
        for debt in self.debts: print(debt)

    def print_payments(self):
        for payment in self.payments: print(payment)

    def total_owed(self):
        total = 0
        for debt in self.debts: total+=float(debt[2])
        for payment in self.payments: total-=float(payment[2])
        print("{:.2f}".format(total))

    def order_debts_and_payments(self):
        self.debts = sorted(self.debts, key = lambda x: datetime.strptime(x[0],'%d/%m/%Y'))
        self.payments = sorted(self.payments, key = lambda x: datetime.strptime(x[0],'%d/%m/%Y'))

    def manual_check(self,debt,payment,matches): #Check debt and payment match and if so update the resident's debts and payments
        print('Debt =   ',debt, '\nPayment =', payment)
        match=input('Do these match? (y/n)  ')
        if match=='y':
            matches.append([debt,payment])
            self.payments.remove(payment)
            self.debts.remove(debt)
        print()

    def line_up_debts_and_payments(self):
        matches=[] #Store matched debts and payments
        error_margin = 30

        for debt in self.debts[:]: #A copy is used so that removing debts doesn't cause issues in the iteration

            for payment in self.payments[:]: #First search Jeanette's sheet for matching payments
                if len(payment)==4 and debt[-1]==payment[-1]: self.manual_check(debt,payment,matches) 
                        
            #Try to find matching payment by looking for payments sufficiently close in date to the debt
            if self.payments!=[]:
                payment = min(self.payments, key=lambda x: error(x,debt) )
                if error(payment,debt)<error_margin: self.manual_check(debt,payment,matches)
                        
        print('\nThe following debts remain unpaid:\n')
        for debt in self.debts: print(debt)
        print('\nAnd the following payments remain unaccounted for:\n')
        for payment in self.payments: print(payment)
