import re
import csv

table = open("Ion_Channels_Table.csv", 'a')
table.write("Hit Name" + "," + "Accession" + "," + "E-value" + "," + "Description" + ",\n")

def hit_name (file):
    name_match = re.findall('hits name="(.*)" acc', file)
    return name_match
    
def acc (file):
    acc_match = re.findall('" acc="(.*)" bias', file)
    return acc_match        
    
def evalue(file):
    evalue_match = re.findall('" evalue="(.*)" flags', file)
    return evalue_match 

def description (file):
    desc_match = re.findall('" desc="(.*)" evalue', file)
    return desc_match


i = 1

while (i <= 346):
    xml = open('file%i.txt' %i, 'r')
    my_file = xml.read()
    
    hm = hit_name (my_file)
    ac = acc (my_file)
    ev = evalue (my_file)
    des = description (my_file)
    l = len(hm)
    j = 0
    while j < l:
        table.write(hm[j] + "," + ac[j] + "," + ev[j] + "," + des[j] + ",\n")
        j = j + 1
    xml.close()
    i = i + 1

