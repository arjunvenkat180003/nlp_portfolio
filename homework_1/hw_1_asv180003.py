#Arjun Venkat
#asv180003

import sys
import csv
import re
import pickle


#Person class with first name, middle initial, last name, and phone number
class Person:
    def __init__(self, last, first, mi, phone):
        self.last = last
        self.first = first
        self.mi = mi
        self.phone = phone
    
    def display(self):
        print(self.first + " "+self.mi+" "+self.last)
        print(self.phone+"\n")


#check if argument is correct, exit otherwise
if len(sys.argv) != 2:
    print('Error, need an argument')
    exit()
else:
    if sys.argv[1] != 'data/data.csv':
        print('Wrong argument')
        exit()

#function to process the csv and store the employees
def process_file():

    #dictionary to store id with Person
    person_dict = {}

    #open the csv
    with open(sys.argv[1]) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        #skip first line
        next(csv_reader)

        for row in csv_reader:

            #turn first/last names intp capitalized strings
            last = row[0].capitalize()
            first = row[1].capitalize()

            #make mi capital, or 'X' if nonexistent
            mi = row[2]
            if mi == '':
                mi = 'X'
            else:
                mi = mi.capitalize()

            #make sure id is of the proper form
            id = row[3]

            id_m = re.match("[A-Z][A-Z][0-9][0-9][0-9][0-9]", id)

            if not id_m:
                print('ID is two letters followed by 4 digits')

                while not id_m:
                    new_id = input('Enter a valid ID ')
                    id_m = re.match("[A-Z][A-Z]\d{4}", new_id)
                    
                    #make sure id is uniqure
                    if new_id in person_dict:
                        print("ID already exists")
                        id_m = False

                    id = new_id


            #check if phone number is proper
            phone = row[4]

            phone_m = re.match("\d{3}-\d{3}-\d{4}", phone)

            if not phone_m:
                print('Enter phone number in form 123-456-7890')

                while not phone_m:
                    new_phone = input('Enter a valid phone number ')
                    phone_m = re.match("\d{3}-\d{3}-\d{4}", new_phone)
                    phone = new_phone


            #print(first +" "+ mi +" "+last+" "+id+" "+phone)

            #add id + Person to the dictionary
            person_dict[id] = Person(last, first, mi, phone)
    
    return person_dict

#get the dict of persons
person_dict = process_file()

print("Employee list\n")
for id, Person in person_dict.items():
    
    print("Employee id: "+id)
    Person.display()

with open('person.pickle', 'wb') as handle:
    pickle.dump(person_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('person.pickle', 'rb') as handle:
    dict_in = pickle.load(handle)

print("Employee list\n")
for id, Person in dict_in.items():
    
    print("Employee id: "+id)
    Person.display()


