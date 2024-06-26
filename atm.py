import hashlib
from  AtmSDB import Database 
import random
import smtplib
import ssl
import click
import getpass
import time
import pygame 
import pyttsx3 
import speech_recognition as sr 
import os

class Atm:

    def __init__(self):
        self.db = Database()
        self.salt = "your_salt_value"
        pygame.init()
        engine = pyttsx3.init('sapi5')
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)

    # function for sending OTP to user
    def send_otp_email(self,email):
        port = 587
        smtp_server = "smtp.gmail.com"
        sender_email = "jejurkarom24@gmail.com"
        receiver_email = email
        # receiver_email = "vikaswagh8007@gmail.com" vikas sir email .
        password = "jwja vacj yatc ioaq"
        self.otp = ''.join([str(random.randint(0, 9)) for i in range(4)])
        subject = "Your OTP"
        text = " This is your One Time Password"
        message = f"Subject: {subject}\n\n{self.otp}{text}"
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls(context=context)
            server.ehlo() 
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
        print("OTP sent Successfully on your registered email")
        self.db.execute_query("update user set OTP = %s where Email = %s", (self.otp, email))

    # Function for clearing screen  
    def clrscr(self):
        click.clear()

    # Function for creating account 
    def create_account(self):
        sound_effect = pygame.mixer.Sound("Registration_page.mp3")
        sound_effect.play()

        self.clrscr()
        max_id = self.db.fetch_query("SELECT MAX(ID) FROM user")[0]
        atm_id = max_id + 1
        print("Wel-come to ATM system")
        print("Creating your account....")
        print("-"*30,"Registration Page","-"*30)
        name = input("Enter your name: ")
        balance = int(input("Enter your balance: "))
        email = input("Enter your email address: ")
        self.question = input("Enter your security question : ")
        self.answer = input("Enter answeer to your security question : ")
        while True:
            pin1 = int(input("Enter your pin: "))
            pin2 = int(input("Enter your pin again: "))
            if pin1 == pin2:
                hashed_pin = self.hash_pin(pin1)
                print("Pin set successfully")
                break
            else:
                print("Pins do not match")
        print("Your account created successfully with ID:", atm_id)
        self.db.execute_query("INSERT INTO user (ID, Name, Balance, Pin, Email, SecQuestion, SecAnswer) VALUES (%s, %s, %s, %s, %s, %s, %s)", (atm_id, name, balance, hashed_pin, email, self.question, self.answer))

    # Function for hashing the pin
    def hash_pin(self, pin):
        pin_with_salt = str(pin) + self.salt
        hashed_pin = hashlib.sha256(pin_with_salt.encode()).hexdigest()
        return hashed_pin

    #Login function
    def login(self):
        self.clrscr()
        print("-"*20," Login Page ","-"*20)
        sound_effect = pygame.mixer.Sound("Login_page.mp3")
        sound_effect.play()        
        atm_id = int(input("Enter your ID: "))
        account = self.db.fetch_query("SELECT * FROM user WHERE ID = %s", (atm_id,))
        if account:
            name = account[1]
            balance = account[2]
            pin = account[3]
            email = account[4]
            print(name, "Logged in")
            while True:
                entered_pin = int(input("Enter your pin: "))
                hashed_pin = self.hash_pin(entered_pin)
                if hashed_pin == pin:
                    while True:
                        self.send_otp_email(email)
                        entered_otp = input("Enter your OTP  :")
                        if entered_otp == self.otp:
                            self.show_menu(balance, atm_id, name,email)
                            break
                        else:
                            print("wrong otp entered \nPlease try again")
                    break
                else:
                    print("Incorrect pin")
        else:
            print("ID not found. Verify your ID")

    def show_menu(self, balance, atm_id, name,email):
        # self.clrscr()
        sound_effect = pygame.mixer.Sound("Logded_s.mp3")
        sound_effect.play()
        print("*"*20," Welcome to ATM System ","*"*20);print()
        print(f"Account Holder {name}  is Active");print()
        while True:
            print("+------------------------ Menu -------------------------+")
            print("| 1. Withdrawal             |   2. Deposit              |")
            print("| 3. Check balance          |   4. Transfer Money       |")
            print("| 5. Deactivate Account     |   6. Transaction History  |")
            print("| 7. Logout                 |                           |")
            print("+-------------------------------------------------------+")
            print()
            choice = int(input(f"{name}, how can I assist you today? \nChoose an option from the menu: "))
            if choice == 1:
                self.withdraw(balance, atm_id, email)
            elif choice == 2:
                self.deposit(balance, atm_id,email)
            elif choice == 3:
                self.check_balance(atm_id)
            elif choice == 4:
                self.Transfer_money(atm_id,balance,email)
            elif choice == 5:
                self.deactivate_account(atm_id,email)
                break
            elif choice == 6:
                self.Transaction_history(atm_id)
            elif choice == 7:
                self.Logout(name)
                break
            else:
                print("Wrong choice")

    def withdraw(self, balance, atm_id, email):
        self.bal = balance
        self.w_amount = int(input("Enter amount: "))
        if self.w_amount <= self.bal:
            self.bal = self.bal-self.w_amount
            withdraw_time = time.strftime("%Y-%m-%d %H:%M:%S")
            self.db.execute_query("UPDATE user SET Balance = %s WHERE ID = %s", (self.bal, atm_id))
            self.db.execute_query("Insert into transaction (UserID,Time,Transaction_type,Transaction_amt) values(%s,%s,%s,%s)",(atm_id,withdraw_time,"withdraw",self.w_amount))
            print("Withdrawal of", self.w_amount, "successfully done")
            self.send_task_notification(email,"Withdrawal")
        else:
            print("Insufficient balance")

    def deposit(self, balance, atm_id,email):
        self.d_amount = int(input("Enter amount you want to deposit: "))
        balance += self.d_amount
        deposit_time = time.strftime("%Y-%m-%d %H:%M:%S")
        self.db.execute_query("UPDATE user SET Balance = %s WHERE ID = %s", (balance, atm_id))
        self.db.execute_query("Insert into transaction (UserID,Time,Transaction_type,Transaction_amt) values(%s,%s,%s,%s)",(atm_id,deposit_time,"Deposit",self.d_amount))
        print("Amount of", self.d_amount, "successfully deposited")
        self.send_task_notification(email,"Deposit")

    def check_balance(self,atm_id):
        result = self.db.fetch_query(f"SELECT Balance from user where ID = {atm_id}")
        new_result = list(result)
        print(f"Your balance is: {new_result}")
    
    def Transfer_money(self,atm_id,balance,email):
        receiver_id = int(input("Enter ID of person whome you want to send money : "))
        account = self.db.fetch_query(f"SELECT * FROM user WHERE ID = {receiver_id}")
        if account:
            name = account[1]
            id = account[0]
            receiver_bal = account[2]
            print(f"You are transsferring money to {name}\nwhoes ID is : {id}")
            self.t_amount = int(input("Enter amount: "))
            self.bal = balance
            if self.t_amount <= self.bal:
                #sender
                self.bal = self.bal-self.t_amount
                self.db.execute_query("update user set Balance = %s where ID = %s",(self.bal,atm_id))
                #receiver
                receiver_bal += self.t_amount
                self.db.execute_query("update user set Balance = %s where ID = %s",(receiver_bal,receiver_id))
                self.transfer_time = time.strftime("%Y-%m-%d %H:%M:%S")
                #Transaction Time
                self.db.execute_query("Insert into transaction (UserID,Time,Transaction_type,Transaction_amt) values(%s,%s,%s,%s)",(atm_id,self.transfer_time,"Transfer",self.t_amount))
                self.send_task_notification(email,"Money Transfer")
                print("Money transfered successfully")
            else:
                print("Insufficient balance")
        else:
            print("Entered Id Is not present")
            time.sleep(5)
        # self.clrscr()

    def deactivate_account(self,atm_id,email):
        self.clrscr()
        account = self.db.fetch_query("SELECT * FROM user WHERE ID = %s", (atm_id,))
        # deactivation_time = time.strftime("%Y-%m-%d %H:%M:%S")
        if account:
            pin = account[3]
            while True:
                entered_pin = int(input("Enter your pin: "))
                hashed_pin = self.hash_pin(entered_pin)
                if hashed_pin == pin:
                    self.db.execute_query("DELETE FROM user WHERE ID = %s", (atm_id,))
                    print("Account Deactivated successfully")
                    self.send_task_notification(email,"Deactivate")
                    break
                else:
                    print("Incorrect pin")

    def Transaction_history(self,atm_id):
        self.history = self.db.fetch_all_query(f"Select * from transaction where UserID = {atm_id}")
        for i in self.history:
            self.tid = i[0]
            self.time = i[1]
            self.t_type = i[2]
            self.t_amount = i[3] 
            print(f"Your transaction Id is : {self.tid}")
            print(f"Your time of transaction was : {self.time}")
            print(f"Your transaction type was : {self.t_type}")
            print(f"Your Transaction Amount was : {self.t_amount}")
            print("_"*60)

    def Logout(self, name):
        print(name, "Logged out")

    def Updation(self):
        self.clrscr()
        print("-"*20,"Updating your Profile","-"*20)
        self.user_id = int(input("Enter your ID: "))
        account = self.db.fetch_query(f"SELECT * FROM user WHERE ID = {self.user_id}")
        if account:
            name = account[1]
            pin = account[3]
            email = account[4]
            print(name, "Updating Profile\nYour ID is:", self.user_id)
            while True:
                entered_pin = int(input("Enter your pin: "))
                hashed_pin = self.hash_pin(entered_pin)
                if hashed_pin == pin:
                    while True:
                        print("1.Name\n2.Pin\n3.Email\n4.Back")
                        choice =int(input("Enter what you want to update in your profile : "))
                        if choice == 1:
                            update_name = input("Enter your name you want to change : ")
                            self.db.execute_query("Update user set Name = %s Where ID = %s",(update_name,self.user_id))
                            print(f"Name Updated to {update_name} ")
                            print("Name Updation successful")
                            self.send_task_notification(email,"Update Profile")
                        elif choice == 2:
                            update_pin = int(input("Enter your pin you want to change : "))
                            hashed_pin = self.hash_pin(update_pin)
                            self.db.execute_query("Update user set Pin = %s Where ID = %s",(hashed_pin,self.user_id))
                            print("Pin Updated to successfully")
                            self.send_task_notification(email,"Update Profile")
                        elif choice == 3:
                            update_email = input("Enter your name youwant to change : ")
                            self.db.execute_query("Update user set Email = %s Where ID = %s",(update_email,self.user_id))
                            print(f"Email Updated to {update_email} ")
                            print("Email  updation successful")
                            self.send_task_notification(email,"Update Profile")
                        elif choice == 4:
                            break
                        else:
                            print("Wrong choice entered")
                    break
                else:
                    print("Can't Update your profile \nIncorrect pin entered")

    def Reset_pin(self):
        self.r_id = int(input("Enter your ID to reset pin"))
        self.account = self.db.fetch_query(f"select * from user where ID = {self.r_id}")
        if self.account:
            name = self.account[1]
            self.qus = self.account[6]
            self.ans = self.account[7]
            print(f"{name} Resting your Pin")
            for i in range (3, -1,-1 ):
                print(self.qus)
                entered_ans = input("Enter your answer : ")
                if entered_ans == self.ans:
                        pin1 = int(input("Enter your pin: "))
                        pin2 = int(input("Enter your pin again: "))
                        if pin1 == pin2:
                            hashed_pin = self.hash_pin(pin1)
                            print("Pin set successfully")
                            self.db.execute_query("update atmdatabase set Pin = %s where ID = %s",(hashed_pin,self.r_id))
                            break
                        else:
                            print("Pins do not match")
                else:
                    print("Answer to the question is wrong")
                    print(f"{i} chance remain")

    def total_accounts(self):
        # self.clrscr()
        result = self.db.fetch_query("SELECT COUNT(*) FROM user")
        print("Total ID present in the system:", result[0])

    def total_balance(self):
        # self.clrscr()
        result = self.db.fetch_query("SELECT SUM(balance) FROM user")
        print("Total balance of the system:", result[0])

    def administrator(self):
        self.admin_name = "Om Jejurkar"
        self.email = "jejurkarom@gmail.com"
        self.send_otp_email(self.email)
        while True:
            enterd_ad_otp = getpass.getpass("Enter the Administrator's OTP to verify :")
            if enterd_ad_otp == self.otp:
                print()
                print("Wel-come Admin ", self.admin_name)
                print()
                while True:
                    print( "*"*20," Admin Menu ","*"*20)
                    print("1.See Database \n2.Perform task on Database \n3.logout admin")
                    choice = int(input("Enter your choice : "))
                    print()
                    if choice == 1:
                        self.see_database()
                    elif choice == 2:
                        self.Perform_task()
                    elif choice == 3:
                        self.Logout_admin()
                        break
                    else:
                        print("Please enter correct option ")
                break
            else:
                print("Entered Pin is invalid \nPlease Try again ")

    def see_database(self):
        self.clrscr()
        account = self.db.fetch_all_query("SELECT * FROM user")
        for i in account:
            id = i[0]
            name = i[1]
            balance = i[2]
            pin = i[3]
            email = i[4]
            print("ID is        : ", id)
            print("name is      : ", name)
            print("Balance is   : ", balance)
            print("Hashed Pin   : ", pin)
            print("Email is     : ", email)
            print()
    
    def Perform_task(self):
        self.clrscr()
        while True:
            print("1.Insert \n2.Update(under process)\n3.Delete\n4.Back")
            admin_ch = int(input("Enter youur choice: "))
            if admin_ch == 1:
                self.create_account()
                break
            elif admin_ch == 2:
                admin_ch = int(input("Enter the ID you want to update : "))
                column_name = input("Enter what you want to update: ")
                value = input("Entere the changes: ")
                self.db.execute_query(f"UPDATE atmdatabase SET {column_name} = '{value}' where ID = {admin_ch}")
            elif admin_ch == 3:
                atm_id = int(input("Enter your ID: "))
                self.db.execute_query("DELETE FROM atmdatabase WHERE ID = %s", (atm_id,))
                print("Account Deactivated successfully")
                break
            elif admin_ch == 4:
                break
            else:
                print("Wrong option entered\n Please try again")

    def Logout_admin(self):
        admin_name = "Om Jejurkar"
        print(admin_name, "Logged out")

    def send_task_notification(self,email,task):
        port = 587
        smtp_server = "smtp.gmail.com"
        sender_email = "jejurkarom24@gmail.com"
        receiver_email = email
        password = "jwja vacj yatc ioaq"
        subject = "Task Notification"
        if task == "Withdrawal":
            text = f"Successfullly {self.w_amount} rupees money withrawed from your account"
        elif task == "Deposit":
            text = f"Successfullly {self.d_amount} rupees deposited in your account"
        elif task == "Money Transfer":
            text = f"Successfullly {self.t_amount} Transfered from your account"
        elif task == "Update Profile":
            text = "Successfullly updated your profile"
        elif task == "Deactivate":
            text = "Your account deactivated successfully \n Thank you using our system"

        message = f"Subject: {subject}\n\n{text}"
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls(context=context)
            server.ehlo() 
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)

    # @staticmethod
    def show_user_main_menu(self):  
        print()
        print("+-------User Menu-----------+")
        print("|    1.Create Account       |")
        print("|    2.Login                |")
        print("|    3.Upadation            |")
        print("|    4.Reset Pin            |")
        print("+---------------------------+")
    def show_admin_main_menu(self):
        print("+--------Admin Menu---------+")
        print("|    1.Total Accounts       |")
        print("|    2.Total Balance        |")
        print("|    3.Administrator Mode   |")
        print("|    4.Back                 |")
        print("+---------------------------+")
    @staticmethod
    def quit():
        print("Exiting...")
        exit()

    def main(self):
        while True:
            self.clrscr()
            sound_effect = pygame.mixer.Sound("welcome_om.mp3")
            sound_effect.play()
            print()
            print("Please choose your role \n1.User \U0001F464\n2.Admin \U0001F64B")
            choice = int(input("How can we assist you today? Please choose an option from the menu:"))
            if choice == 1 :
                self.show_user_main_menu()
                choice = int(input("Enter what you want to perform : "))
                if choice == 1:
                    self.clrscr()
                    self.create_account()
                elif choice == 2:
                    self.clrscr()
                    self.login()
                elif choice == 3 :
                    self.Updation()
                elif choice == 4 :
                    self.Reset_pin()
                elif choice == 5:
                    break
                else:
                    print("No Option Available ")                
            elif choice == 2:
                a_pin = "906251"
                e_pin = getpass.getpass("Enter admin pin :")
                while True:
                    if a_pin == e_pin:
                        # self.clrscr()
                        self.show_admin_main_menu()
                        choice = int(input("Welcome, Administrator! Indicate your desired task by entering the corresponding number:"))
                        if choice == 1:
                            self.total_accounts()
                        elif choice == 2:
                            self.total_balance()
                        elif choice == 3:
                            self.clrscr()
                            self.administrator()  
                        elif choice == 4:
                            break 
                        else:
                            print("No Option Available") 
                    else:
                        print("Incorrect Pin Entered! Please Enter correct pin to procced")
            else:
                print("Wrong Option selected")

obj = Atm()
obj.main()