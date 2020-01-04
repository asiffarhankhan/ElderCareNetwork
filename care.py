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
		ct['recipients'] = []
		ct['earnings'] = 0
		ct['public_id'] = str(randint(1000,9999))

		li = self.data['caretakers']
		li.extend([ct])

		with open('register.json','w') as file:
			json.dump(self.data, file, indent=3, sort_keys=True)

		print("\n\tThank you for registering! Your login UserID is: "+self.login_id+'\n\n')

				
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
		rt['caretaker_alloted'] = 'none'
		rt['funds'] = 0
		rt['public_id'] = str(randint(1000,9999))

		li = self.data['recipients']
		li.extend([rt])

		with open('register.json','w') as file:
			json.dump(self.data, file, indent=3, sort_keys=True)

		print("\n\tThank you for registering! Your login UserID is: "+self.login_id+'\n\n')


class login:

	def __init__(self):
		
		with open('register.json','r') as self.file:
			self.data = json.load(self.file)

		os.system('clear')
		option = int(input("\n\nPLEASE CHOOSE YOUR LOGIN TYPE: \n\n1. Caretaker Login \t 2. Recipient Login \n\nEnter Here: "))

		if option == 1:

			self.ct_id = input('\n\nPlease Enter your User ID here : ')

			for i in self.data['caretakers']:
				if i['login_id'] == self.ct_id:
					self.ct_data = i
					self.CareTaker()
					break
			else:
				print("ERROR: Please check your login id and try again!")
				input("\n\nPress any Key: ")
				self.__init__()

		elif option == 2:

			self.rt_id = input('\n\nPlease Enter your User ID here : ')

			for i in self.data['recipients']:
				if i['login_id'] == self.rt_id:
					self.rt_data = i
					self.Recipient()
					break
					
			else:
				print("\nERROR: Please check your login id and try again!")
				input("\n\nPress any Key: ")
				self.__init__()


	def CareTaker(self):
		
		os.system('clear')

		print("\n\nWelcome {} You have successfully been logged in. \n\nPlease Select a service : \n".format(self.ct_data['Name']))
		option = int(input('\t1. Volunteer to serve an elder citizen\n\n\t2. Check Earnings\n\nEnter Here: '))

		if option == 1:

			if len(self.ct_data['recipients']) < 4:
				os.system('clear')
				print('\nFollowing are the elder adults that are looking for a service in your area:\n')
				for i in self.data['recipients']:
					
					if i['City'] == self.ct_data['City']:
						print(' Name: '+i['Name'],'\n Age: '+str(i['Age']),'\n Gender: '+i['Gender'],'\n Public ID: '+i['public_id']+'\n')

			else:
				print("\n\n\tYou have reached the maximum allowed number of service available per user!")


	def Recipient(self):

		os.system('clear')

		print("\n\nWelcome {} You have successfully been logged in. \n\nPlease Select a service : \n".format(self.rt_data['Name']))
		option = int(input('\t1. Choose a CareTaker\n\n\t2. Deposit Fund\n\nEnter Here: '))

		if option == 1:

			if self.rt_data['funds']>=10000:
				os.system('clear')
				print('\nFollowing are the caretakers willing to serve in your area:\n')

				for i in self.data['caretakers']:
					if i['City'] == self.rt_data['City'] and len(i['recipients']) < 4:
						print(' Name: '+i['Name'],'\n Age: '+str(i['Age']),'\n Gender: '+i['Gender'],'\n Public ID: '+i['public_id']+'\n')

			else:
				input("\n\tYou are required to deposit funds amounting to 10000 or above before choosing a caretaker. Press Enter to go back\n")

				self.Recipient()

		elif option == 2:

			funds = int(input("\n\nPease Enter an amount to deposit: Rs. "))
			self.rt_data['funds'] = funds
			input("Rs {}\\- has been added in your funds, Please press Enter".format(funds))
			self.Recipient()


if __name__ == '__main__':

	os.system('clear')
	option = int(input("\n\nWELCOME TO CAREALL! PLEASE SELECT ONE OF THE OPTIONS FROM BELOW TO PROCEED: \n\n\t1. Register \t 2. Login \n\nEnter Here: "))

	if option == 1:
		register()
	else:
		login()
