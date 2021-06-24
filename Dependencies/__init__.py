import math, os, glob, sys, pickle
from shutil import copyfile

from .Reading import *
from .Residents import *


try: #Allow for colour when printing in IDLE
    color = sys.stdout.shell
except AttributeError:
    raise RuntimeError("Use IDLE")



def c(): print(("\n" * 100)) #Used for clearing the IDLE terminal while troubleshooting

def find(string,filters):
    boolean=False
    for filter_ in filters:
        if filter_ in string: boolean=True
    return boolean

def find_invoices(identifier): #Search for invoices by invoice number or resident name
    filenames=[]
    for year in [folder_name for folder_name in os.listdir('Invoices') if len(folder_name)==4]:
        for folder_name in os.listdir('Invoices/'+year):
                for filename in os.listdir('Invoices/'+year+'/'+folder_name):
                    if str(identifier) in filename: filenames.append('Invoices/'+year+'/'+folder_name+'/'+filename)
    return filenames

def write_data(data,filename):
    userfile = open(filename, 'w')
    userfile.write('Date, Description, Value\n')
    for payment in data: userfile.write(payment[0]+','+payment[1]+','+payment[2]+'\n')
    userfile.close()
