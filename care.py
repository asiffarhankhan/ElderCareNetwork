import os
import json
from random import randint
import time

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
		ct['rating'] = 2.5

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
		rt['caretaking_requests'] = []
		rt['rating'] = 2.5 

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
		option = int(input("\n\nPLEASE CHOOSE YOUR LOGIN TYPE: \n\n\t1. Caretaker Login \t 2. Recipient Login \n\nEnter Here: "))

		if option == 1:

			self.ct_id = input('\nPlease Enter your User ID here : ')

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

			self.rt_id = input('\nPlease Enter your User ID here : ')

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
					
					if i['City'] == self.ct_data['City'] and i['caretaker_alloted'] == 'none':
						print(' Name: '+i['Name'],'\n Age: '+str(i['Age']),'\n Gender: '+i['Gender'],'\n Public ID: '+i['public_id']+'\n Rating: '+str(i['rating'])+'\n')
						break

				else:
					print("\n\nNo available recipients at the moment! Please check back later!\n")
					print("You will be redirected to your profile in 10 seconds")
					time.sleep(10)
					self.CareTaker()

				public_id = input('Enter the public_id of a recipient that you\'d like to serve: ')

				for i in self.data['recipients']:
					if i['public_id'] == public_id and i['public_id'] not in self.ct_data['recipients']:
						print("\n\n{} will be informed about your interest in his caretaking, Please wait for his approval. Thank you for your service\n\n".format(i['Name']))
						i["caretaking_requests"].append(self.ct_data['public_id'])

						with open('register.json','w') as file:
							json.dump(self.data, file, indent=3, sort_keys=True)
						
						print("You will be redirected to your profile in 10 seconds")
						time.sleep(10)
						self.CareTaker()

					else:
						print("\n\nError No such user found!")
						print("You will be redirected to your profile in 10 seconds")
						time.sleep(10)
						self.CareTaker()

			else:
				print("\n\n\tYou have reached the maximum allowed number of service available per user!")


	def Recipient(self):

		os.system('clear')
		if len(self.rt_data['caretaking_requests']) > 0:
			print("\n\n(*)You have pending request(s) available from a caretaker to serve you. Please approve or discard the request(s): \n")
			
			for c in self.rt_data['caretaking_requests']:
				for d in self.data['caretakers']:
			
					if c == d['public_id']:
						print('\nName: '+d['Name'],'\n Age: '+str(d['Age']),'\n Gender: '+d['Gender'],'\n Public ID: '+d['public_id']+'\n Rating: '+str(d['rating'])+'\n')
						r = input('Do you approve of Mr. {} as your caretaker ? (y/n): '.format(d['Name']))
						if r == 'y' or r == 'Y':
							if self.rt_data['funds'] >= 10000:
								print("Deducting Rs 10000 from you funds...")
								time.sleep(2)
								d['earnings'] = 10000
								self.rt_data['funds'] -= 10000
								print("Rs 10000 successfully Detucted from your funds!")
								time.sleep(2)
								d['recipients'].append(self.rt_data['public_id'])
								self.rt_data['caretaker_alloted'] = d['public_id']
								self.rt_data['caretaking_requests'] = []
								
								with open('register.json','w') as file:
									json.dump(self.data, file, indent=3, sort_keys=True)
							
								os.system('clear')
							else:

								a = int(input("\n\nPlease deposit funds to continue, enter the amount 10000 or above: "))
								self.rt_data['funds'] += a
								input("Rs {}\\- has been added in your funds, Please press Enter".format(a))
								with open('register.json','w') as file:
									json.dump(self.data, file, indent=3, sort_keys=True)
									self.Recipient()

						elif r == 'n' or r == 'N':
							print("\nThanks for your response!")
							self.rt_data['caretaking_requests'] = []

							with open('register.json','w') as file:
									json.dump(self.data, file, indent=3, sort_keys=True)
									self.Recipient()

		print("\n\nWelcome {} You have successfully been logged in. \n\nPlease Select a service : \n".format(self.rt_data['Name']))
		option = int(input('\t1. Choose a CareTaker\n\n\t2. Deposit Fund\n\nEnter Here: '))

		if option == 1:

			if self.rt_data['funds']>=10000:
				os.system('clear')
				print('\nFollowing are the caretakers willing to serve in your area:\n')

				for i in self.data['caretakers']:
					if i['City'] == self.rt_data['City'] and len(i['recipients']) < 4:
						print(' Name: '+i['Name'],'\n Age: '+str(i['Age']),'\n Gender: '+i['Gender'],'\n Public ID: '+i['public_id']+'\n')
				
				public_id = input('\nEnter the public_id of the care taker you are interested to hire: ')

				for i in self.data['caretakers']:
					if i['public_id'] == public_id:
						i['recipients'].append(self.rt_data['public_id'])
						print("Deducting Rs 10000 from you funds...")
						time.sleep(2)
						i['earnings'] = 10000
						self.rt_data['funds'] -= 10000
						print("Rs 10000 successfully Detucted from your funds!")
						time.sleep(2)
						self.rt_data['caretaker_alloted'] = i['public_id']

						with open('register.json','w') as file:
							json.dump(self.data, file, indent=3, sort_keys=True)
				

						print("\n\nCongratulation! {} have been alloted as your caretaker!\n\n".format(i['Name']))

			else:
				input("\n\tYou are required to deposit funds amounting to 10000 or above before choosing a caretaker. Press Enter to go back\n")

				self.Recipient()

		elif option == 2:

			funds = int(input("\n\nPease Enter an amount to deposit: Rs. "))
			self.rt_data['funds'] = funds
			input("Rs {}\\- has been added in your funds, Please press Enter".format(funds))
			with open('register.json','w') as file:
				json.dump(self.data, file, indent=3, sort_keys=True)
			self.Recipient()


if __name__ == '__main__':

	os.system('clear')
	option = int(input("\n\nWELCOME TO CAREALL! PLEASE SELECT ONE OF THE OPTIONS FROM BELOW TO PROCEED: \n\n\t1. Register \t 2. Login \n\nEnter Here: "))

	if option == 1:
		register()
	else:
		login()
