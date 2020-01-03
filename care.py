import os
import json
from random import randint

class register:

    def __init__(self):

        os.system('clear')
        option = int(input("\n\nPLEASE ENTER THE CORRESPONDING SERIAL NUMBER TO THE DESIRED SERVICE:\n\n1. I want to register myself as a Care taker\n2. I am willing to be taken care of\n\nYour Choice: "))

        with open('register.json','r') as self.file:
            self.data = json.load(self.file)

        if option == 1:
            self.CareTaker()
        else:
            self.Recipient()
            

    def CareTaker(self):

        """The function registers and saves a user as an available CareTaker for older people to choose from. 
        further preferences can be listed after logging in which will be used to decide the type of service they are available to provide."""

        ct = {}
        ct['Name'] = input("\nNAME :\t")
        ct['Age'] = int(input("AGE  :\t"))
        ct['City'] = input("CITY :\t")
        ct['Gender'] = input("GENDER:\t")
        self.login_id = 'ct_'+str(randint(1000,9999))
        ct['login_id'] = self.login_id

        li = self.data['caretakers']
        li.extend([ct])

        with open('register.json','w') as file:
            json.dump(self.data, file, indent=3, sort_keys=True)

        print("\n\tYour login UserID is: "+self.login_id+'\n\n')
                
    def Recipient(self):

        """The function registers and saves a user as an available recipient for the service and for caretakers to serve them. 
        further preferences can be listed after logging in which will be used to decide the the service most suitable for them."""

        rt = {}
        rt['Name'] = input("\nNAME  :\t")
        rt['Age'] = int(input("AGE   :\t"))
        rt['City'] = input("CITY  :\t")
        rt['Gender'] = input("GENDER:\t")
        self.login_id = 'rt_'+str(randint(1000,9999))
        rt['login_id'] = self.login_id
        li = self.data['recipients']
        li.extend([rt])

        with open('register.json','w') as file:
            json.dump(self.data, file, indent=3, sort_keys=True)

        print("\n\tYour login UserID is: "+self.login_id+'\n\n')


class login:

    def __init__(self):
        
        with open('register.json','r') as self.file:
            self.data = json.load(self.file)

        os.system('clear')
        option = int(input("\n\nPLEASE CHOOSE YOUR LOGIN TYPE: \n\n1. Caretaker Login \t 2. Recipient Login \n\nEnter Here: "))

        if option == 1:
            self.CareTaker()
        else:
            self.Recipient()


    def CareTaker(self):
        
        self.ct_id = input('\n\nPlease Enter your User ID here : ')

        for i in self.data['caretakers']:
            if i['login_id'] == self.ct_id:
                ct_data = i

        print("\n\nWelcome {} You have successfully been logged in. \nPlease Select a service : \n\n".format(ct_data['Name']))

    def Recipient(self):

        self.rt_id = input('\n\nPlease Enter your User ID here : ')

        for i in self.data['recipients']:
            if i['login_id'] == self.rt_id:
                rt_data = i

        print("\n\nWelcome {} You have successfully been logged in. \nPlease Select a service : \n\n".format(rt_data['Name']))

if __name__ == '__main__':

    
    os.system('clear')
    option = int(input("\n\nWELCOME TO CAREALL! PLEASE SELECT ONE OF THE OPTIONS FROM BELOW TO PROCEED: \n\n\t1. Register \t 2. Login \n\nEnter Here: "))

    if option == 1:
        register()
    else:
        login()
