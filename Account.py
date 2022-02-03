import pickle
import datetime

date_format_string = "%d/%m/%Y"

# Transaction Class that stores details about each transaction
class Transaction(object):
	# Contructor, take in the date, amount and a small description
	def __init__(self,transaction_date, transaction_amount, transaction_description, transaction_category):
		#self.transaction_date = transaction_date
		self.transaction_date = datetime.datetime.strptime(transaction_date,date_format_string)
		self.transaction_amount = float(transaction_amount)
		self.transaction_description = transaction_description
		self.transaction_category = transaction_category

# Account class. Account has-a list of transactions associated with it
class Account(object):

	# Constructor, takes in account details
	def __init__(self,account_name, account_number, opening_balance, opening_date, bsb):
		# populate fields
		self.account_name = account_name
		self.account_number = account_number
		self.bsb = bsb
		self.opening_date = opening_date
		self.balance = float(opening_balance)
		# create a new transaction to add to the list
		new_transaction = Transaction(self.opening_date,self.balance, transaction_description="Opening Balance", transaction_category="OPENING BALANCE")
		# list for storing Transaction objects
		self.transactions = []
		self.transactions.append(new_transaction)

	# code to handle a withdrawal from the account
	def make_withdrawal(self,date, amount, description, category):
		self.balance = self.balance + float(amount)
		new_transaction = Transaction(date, amount, description, category)
		self.transactions.append(new_transaction)
		print(f"Withdrew {amount} from account {self.account_number}")

	# code to handle a deposit to the account
	def make_deposit(self,date, amount, description, category):
		self.balance = self.balance + float(amount)
		new_transaction = Transaction(date, amount, description, category)
		self.transactions.append(new_transaction)
		print(f"Deposited {amount} to account {self.account_number}")

	# prints out the details of the account and transactions using a for loop
	def print_details(self):
		print(f"\n\nDetails for {self.account_name} : {self.account_number} : {self.bsb}")
		print(f"\nBalance: {self.balance}")
		print("\n--------------------------------------------------------------------------")
		for transaction in self.transactions:
			date = transaction.transaction_date.strftime("%d/%m/%Y")
			print(f"{date} :  {transaction.transaction_amount: >10} : {transaction.transaction_description: <35} : {transaction.transaction_category: <30}")
		print("--------------------------------------------------------------------------\n")

# Ledger class which stores accounts
class Ledger(object):
	
	def __init__(self,account):
		# list of accounts in the ledger
		self.accounts = []
		self.accounts.append(account)

# Function to open a new acccount
def open_account():
	
	account_name = input("Please enter the Account holder's name: ")
	account_number = input("Please enter the Account Number: ")
	opening_balance = input("Please enter the opening balance: ")
	bsb = input("Please enter the BSB: ")
	opening_date = input("Please enter the Opening Date: ")
	# create a new account
	new_account = Account(account_name, account_number, opening_balance, opening_date, bsb)
	# add the new account to the ledger
	new_ledger = Ledger(new_account)
	# return the ledger
	return new_ledger

# Function to make a deposit
def make_deposit(ledger):
	# Check if the ledger is empty
	if ledger == None:
		print("No account in Ledger!")
		return
	else:
		# capture depoist information
		account_number = input("Please enter the account number: ")
		deposit_amount = input("Please enter the deposit amount: ")
		deposit_description = input("Please enter the desposit description: ")
		deposit_category = input("Please enter the deposit category: ")
		deposit_date = input("Please enter the deposit date: ")
		# search for account
		for account in ledger.accounts:
			# if an account is found, make the deposit
			if(account.account_number == account_number):
				account.make_deposit(deposit_date, deposit_amount, deposit_description, deposit_category.upper())

# Function to make a withdrawal
def make_withdrawal(ledger):
	# Check if the ledger is empty
	if ledger == None:
		print("No account in Ledger!")
		return
	else:
		# capture withdrawal information
		account_number = input("Please enter the account number: ")
		withdrawal_amount = input("Please enter the withdrawal amount: ")
		withdrawal_description = input("Please enter the withdrawal description: ")
		withdrawal_category = input("Please enter the withdrawal category: ")
		withdrawal_date = input("Please enter the withdrawal date: ")
		# search for account
		for account in ledger.accounts:
			# if the account exists make the withdrawal
			if(account.account_number == account_number):
				account.make_withdrawal(withdrawal_date, withdrawal_amount, withdrawal_description, withdrawal_category.upper())

# Function to print the account details
def print_ledger_details(ledger):
	# check to see if the ledger is empty
	if ledger == None:
		print("No account in Ledger!")
		return
	else:
		# capture account number and search the ledger
		account_number = input("Please enter the account number: ")
		for account in ledger.accounts:
			if(account.account_number == account_number):
				account.print_details()

def display_categories(ledger, account_number):
	found = False
	# search ledger for account number
	target_account = None
	for account in ledger.accounts:
			if account.account_number == account_number:
				target_account = account
				found = True
	if found == True:
		category_summary = {}
		running_total = 0.0
		for transaction in target_account.transactions:
			if transaction.transaction_category not in category_summary:
				#print(f"{transaction.transaction_category}")
				category_summary[transaction.transaction_category] = None
		for transaction in target_account.transactions:
			if transaction.transaction_category in category_summary:
				if category_summary[transaction.transaction_category] == None:
					category_summary[transaction.transaction_category] = transaction.transaction_amount		
				else:
					category_summary[transaction.transaction_category] += transaction.transaction_amount	
		print("\n-----------------------")
		print("Results.")
		print("-------------------------")
		for key, value in category_summary.items():
			print(f"category: {key:<20} total: {value:.1f}")	

		print("------------------------\n")	
	else:
		print(f"\nAccount number {account_number}, not found in ledger\n")
		return



def display_by_category(ledger, account_number):
	# search ledger for account number
	found = False
	# search ledger for account number
	target_account = None
	for account in ledger.accounts:
			if account.account_number == account_number:
				target_account = account
				found = True
	if found == True:
		target_category = input("\nPlease enter category to display: \n").upper()
		category_total = 0.0
		print("----------------------------------------------------------------")
		for transaction in target_account.transactions:
			if transaction.transaction_category == target_category:
				date = transaction.transaction_date.strftime("%d/%m/%Y")
				print(f"{date} : {transaction.transaction_amount: >10} : {transaction.transaction_description: <30} : {transaction.transaction_category:<10}")
				category_total += transaction.transaction_amount
		print("----------------------------------------------------------------")
		print(f"Category Total for {target_category}: {category_total:.2f}\n")
	else:
		print(f"\nAccount number {account_number}, not found in ledger\n")
		return

def display_by_date_range(ledger, account_number):
	found = False

	target_account = None
	for account in ledger.accounts:
			if account.account_number == account_number:
				target_account = account
				found = True
	if found == True:
		date_start = input("Please enter the start date to display: ")
		display_date_start = datetime.datetime.strptime(date_start,date_format_string)
		date_end = input("Please enter the end date to display: ")
		display_date_end = datetime.datetime.strptime(date_end,date_format_string)
		print(f"Showing transactions for {display_date_start} to {display_date_end}:")
		print("-------------------------------------------------------------------")
		for transaction in target_account.transactions:
			if transaction.transaction_date >= display_date_start and transaction.transaction_date <= display_date_end:
				print(f"{transaction.transaction_date} : {transaction.transaction_amount: >10} : {transaction.transaction_category:<20} : {transaction.transaction_description:<10}")

	else:
		print(f"\nAccount number {account_number}, not found in ledger\n")
		return

def display_by_date(ledger, account_number):
	# search ledger for account number
	# search ledger for account number
	found = False
	# search ledger for account number
	target_account = None
	for account in ledger.accounts:
			if account.account_number == account_number:
				target_account = account
				found = True
	if found == True:
		date = input("Please enter the date to display: ")
		display_date = datetime.datetime.strptime(date,date_format_string)
		print(f"Showing transactions for {display_date}:")
		print("-------------------------------------------------------------------")
		for transaction in target_account.transactions:
			if transaction.transaction_date == display_date:
				print(f"{transaction.transaction_date} : {transaction.transaction_amount: >10} : {transaction.transaction_category:<20} : {transaction.transaction_description:<10}")

	else:
		print(f"\nAccount number {account_number}, not found in ledger\n")
		return

def summary(ledger):
	if ledger == None:
		print("No account in Ledger!")
		return

	quit = False

	while quit == False:
		
		print("\nWhat data would you like?")
		print("--------------------------")
		print("1. All categories.")
		print("2. Selected category.")
		print("3. By Date.")
		print("4. By Date Range.")
		print("5. return to main menu.")
		selection = int(input("> "))
		if selection == 1:
			account_number = input("Please enter the account number: ")
			display_categories(ledger, account_number)
		elif selection == 2:
			account_number = input("Please enter the account number: ")
			display_by_category(ledger, account_number)
		elif selection == 3:
			account_number = input("Please enter the account number: ")
			display_by_date(ledger, account_number)
		elif selection == 4:
			account_number = input("Please enter the account number: ")
			display_by_date_range(ledger, account_number)
		else:
			quit = True	

# loop flag set to false
quit_flag = False
# ledger set to initial state
ledger = None
try:
	in_file = open('ledger.txt','rb')
	ledger = pickle.load(in_file)
except FileNotFoundError:
	print("\nNo file found! Starting new.")
# loop until the user selects 5 to quit the program
while quit_flag == False:
	
	print("\nWelcome to the Ledger.")
	print("---------------------.")
	print("1. Open Account")
	print("2. Make Deposit")
	print("3. Make Withdrawal")
	print("4. Print Account Details")
	print("5. Print Summary")
	print("6. Quit Program.")
	selection = int(input("> "))
	if selection == 1:
		ledger = open_account()
	elif selection == 2:
		make_deposit(ledger)
	elif selection == 3:
		make_withdrawal(ledger)
	elif selection == 4:
		print_ledger_details(ledger)
	elif selection == 5:
		summary(ledger)
	else:
		quit_flag = True
		out_file = open('ledger.txt','wb')
		pickle.dump(ledger,out_file)
		print("Goodbye!")
