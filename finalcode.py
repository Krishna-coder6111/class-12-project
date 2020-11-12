'''Bank Management Code
Using csv files for portability and sql table as backup records which are encrypted'''

# importing libraries
try:
    import csv
    import os
    import time
    import mysql.connector
    from cryptography.fernet import Fernet
    import pickle
except Exception as e:
    print(e,'Error has occurred.')


# initialising variables
user = 'e'
accountno = 0
main = mainl = maini = 0
user = ''
encrypt_message = ''
highrate = 13.23
head = ['Acc No.', 'Name', 'Age', 'Sex', 'DOB', "Father's Name", 'Address', 'Salary',
        'Email', 'Phone', 'Occupation', 'Pancard', 'Aadhaarcard', 'Acc Type', 'Balance']
loanheader = ['Account No.', 'Auto Loan', 'Health Loan',
              'Home Loan', 'Student Loan', 'Mortgage Loan']

# preset sample data
l = [[10000000, 'Raju Kishan', 40, 'M', '20-09-1980', 'Kishan Ramkumar', '#45 5th Cross Chamarahalli Main Road, Bangalore', 3500000, 
    'raju@com_pany.com', 9836722667, 'Project CEO at Ex_company', 74632893, 112887335464, 'Current', 2000000],
     [10000001, 'Krish Sanghul', 22, 'M', '12-12-1998', 'Ampershire Sanghul', '12, 12th A rd, 12th block Koramangala,Bangalore',
      323434, 'krish12@company.com', 2112212121, 'Software engineer', 21212121, 121212121221, 'Current', 121],
     [10000002, 'Nomi Ranja', 30, 'F', '31-01-1990', 'Ranja Dondini', '$ Hibily apartment, Lake Side, Bangalore',
      2300000, 'nomi@com.com', 9183826453, 'CEO of company_comp', 75643892, 253417890354, 'Savings', 1000000],
     [10000003, 'Shinde Shingle', 18, 'F', '12-12-2002', 'Andashire Shingle', '#21,Palm view , Bangalore', 23343454, 
     'Shinde18@company.com', 3434343434, 'Architecture', 23232323, 454545454545, 'Current', 10000]]

loan = [[10000000, 24000, 60000, 110000, 130000, 44000],
        [10000001, 25000, 50000, 100000, 120000, 45000],
        [10000002, 26000, 49000, 100001, 121000, 46000],
        [10000003, 34000, 45000, 500000, 230000, 210000]]

insurance = [[10000000, 7000, 7010, 7100, 7101],
             [10000001, 7623, 7878, 7908, 7153],
             [10000002, 7645, 7099, 7123, 7000],
             [10000003, 7100, 7200, 7300, 7456]]


# encryption and key generation for mysql data encryption
def generate():
    if os.path.exists('secret.key'):
        pass
    else:
        key = Fernet.generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(key)


generate()

# Loads the secret key for the encoding and decoding purposes
def load():      
    return open("secret.key", "rb").read()

# Encryption 
def encrypt(text):      
    key = load()
    encode = text.encode()
    f = Fernet(key)
    global encrypt_message
    encrypt_message = f.encrypt(encode)
    return encrypt_message

# Decryption 
def decryptor(encrypted_text):
    key = load()
    f = Fernet(key)
    decrypted = f.decrypt(encrypted_text)
    return decrypted.decode()


# mysql initialisation
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sql123",
)
mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE IF NOT EXISTS piggybank")

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sql123",
    database="piggybank"
)
mycursor = mydb.cursor()


# creating a list from csv reader object without delimiters
def csvlist(reading):
    nelist = []
    for i in reading:
        if i == []:
            continue
        else:
            nelist += [i]
    return nelist


# replacing list element
def replacelist(lst, search, element):
    for i in range(len(lst)):
        if lst[i] == search:
            lst[i] = element
            break
    return lst


# filling files with preset sample
def defaults():
    # checking if defaults exist
    if os.path.exists('Defaults.dat'):
        with open('Defaults.dat', 'rb') as file:
            if pickle.load(file) == 1:
                pass
    else:
        with open('Defaults.dat', 'wb') as file:
            pickle.dump(1, file)

        # creating database and tables
        mycursor.execute("CREATE TABLE if not exists Personal_info (Account_no BIGINT(255) PRIMARY KEY, Name text(65535) NOT NULL, \
                    Age BIGINT(255) NOT NULL, Sex text(65535), Date_Of_Birth text(65535) NOT NULL, Father_Name text(65535) , \
                    Address text(65535) NOT NULL, Salary float(255,10), \
                Email_Id text(65535) NOT NULL, Phone_Number BIGINT(255) NOT NULL, Occupation text(65535) NOT NULL, PANCARD BIGINT(255), \
                AADHARCARD BIGINT(255), Type_of_acc text(65535), Amt_in_acc float(255,10))")

        # inputting into csv file
        with open('Account.csv', 'w') as account_file:
            writing = csv.writer(account_file)
            writing.writerows(l)
        query = """INSERT INTO Personal_info (Account_no,Name,Age,Sex,Date_Of_Birth,Father_Name,Address,Salary,Email_Id,Phone_Number,Occupation,PANCARD,AADHARCARD,Type_of_acc,Amt_in_acc)
                                        VALUES (%s,%s,%s,%s,%s, %s,%s,%s,%s,%s,%s,%s,%s, %s, %s) """

        # encrypting the list
        for j in l:
            el = []
            for i in range(len(j)):
                if i == 0 or i == 2 or i == 7 or i == 9 or i == 11 or i == 12 or i == 14:
                    el.append(j[i])
                else:
                    el.append(encrypt(j[i]))
            inputt = (el[0], el[1], el[2], el[3], el[4], el[5], el[6],
                      el[7], el[8], el[9], el[10], el[11], el[12], el[13], el[14])
            mycursor.execute(query, inputt)
        mydb.commit()

        # Loan creation of defaults
        query = """Insert into Loans (Account_no, AUTO, HOME, HEALTH, STUDENT_LOAN , MORTGAGE) VALUES (%s,%s,%s,%s,%s,%s)"""
        mycursor.execute("CREATE TABLE if not exists Loans (Account_no BIGINT(20) REFERENCES Personal_info (Account_no), AUTO FLOAT(100,10), HOME FLOAT(100,10), HEALTH FLOAT(100,10), \
                    STUDENT_LOAN FLOAT(100,10), MORTGAGE FLOAT(100,10))")
        mycursor.execute(
            "ALTER TABLE loans ADD FOREIGN KEY (Account_no) REFERENCES Personal_info (Account_no) ON DELETE CASCADE ON UPDATE CASCADE")
        file_check('Loan_avail.csv')
        for i in loan:
            inputl = (float(i[0]), float(i[1]), float(i[2]),
                      float(i[3]), float(i[4]), float(i[5]))
            mycursor.execute(query, inputl)
            mydb.commit()
        file = open("Loan_avail.csv", 'w')
        writing = csv.writer(file)
        writing.writerows(loan)
        file.close()

        # Insurance defaults creation
        mycursor.execute("CREATE TABLE if not exists Insurance(Account_no BIGINT(20) REFERENCES Personal_info (Account_no),Auto FLOAT(100,10), Health FLOAT(100,10), Life FLOAT(100,10), Property FLOAT(100,10) ) ")
        mycursor.execute(
            "ALTER TABLE Insurance ADD FOREIGN KEY (Account_no) REFERENCES Personal_info (Account_no) ON DELETE CASCADE ON UPDATE CASCADE")
        file_check('Insurance.csv')
        query = """Insert into Insurance (Account_no, Auto, Health, Life, Property) VALUES (%s,%s,%s,%s,%s)"""
        file = open("Insurance.csv", 'w')
        writing = csv.writer(file)
        writing.writerows(insurance)
        file.close()
        for i in insurance:
            inputi = (int(i[0]), int(i[1]), int(i[2]), int(i[3]), int(i[4]))
            mycursor.execute(query, inputi)
        mydb.commit()


# try and except function
def teblock(function, acc_no=None):
    try:
        function(acc_no)
    except Exception as e:
        print(e,'Error has occurred.')
        print('Please try again')
        print()
        function(acc_no)
        print()


# checking if an account has been created in csv files
def acc_check(accountno):
    file_check('Account.csv')
    file_check('Loan_avail.csv')
    file_check('Insurance.csv')
    global main, mainl, maini
    if user.lower() == 'e':
        with open('Account.csv', 'r') as file:
            reading = csv.reader(file)
            reading = csvlist(reading)
            if reading == []:
                main = 0
            else:
                for i in reading:
                    if int(i[0]) == accountno:
                        main = 1        # Check for existence of a record in the file 
                        break
                    else:
                        main = 0
        with open('Loan_avail.csv', 'r') as file:
            reading = csv.reader(file)
            reading = csvlist(reading)
            for i in reading:
                if int(i[0]) == accountno:
                    mainl = 1           # Check for existence of a record in the file
                    break
                else:
                    mainl = 0
        with open('Insurance.csv', 'r') as file:
            reading = csv.reader(file)
            reading = csvlist(reading)
            for i in reading:
                if int(i[0]) == accountno:
                    maini = 1           # Check for existence of a record in the file
                    break
                else:
                    maini = 0    



# checking if csv file exists and if it does not creating one
def file_check(file):
    if os.path.exists(file):
        pass
    else:
        account_file = open(file, 'w')
        account_file.close()


# main function 1: creating a new account in mysql table and csv file
def one_createacc():
    mycursor.execute("CREATE DATABASE IF NOT EXISTS Test")
    mycursor.execute("CREATE TABLE if not exists Personal_info (Account_no BIGINT(255) PRIMARY KEY, Name text(65535) NOT NULL, \
                    Age BIGINT(255) NOT NULL, Sex text(65535), Date_Of_Birth text(65535) NOT NULL, Father_Name text(65535) , \
                    Address text(65535) NOT NULL, Salary float(255,10), \
                Email_Id text(65535) NOT NULL, Phone_Number BIGINT(255) NOT NULL, Occupation text(65535) NOT NULL, PANCARD BIGINT(255), \
                AADHARCARD BIGINT(255), Type_of_acc text(65535), Amt_in_acc float(255,10))")
    ec = 0
    if os.path.exists('Account.csv'):
        file = open('Account.csv', 'r')
        reader = csv.reader(file)
        read = []
        for i in reader:
            read.append(i)
        for j in read:
            if j == []:
                ec += 1
        if ec == len(read):
            acc_no = 10000000       # First account number to be generated in case there are 0 existing records
        else:
            acc_no = (int(csvlist(read)[len(csvlist(read))-1][0]) + 1)  # Sequential order of account number during generation
    else:
        account_file = open('Account.csv', 'w')
        account_file.close()
        acc_no = 10000000

    query = """INSERT INTO Personal_info (Account_no,Name,Age,Sex,Date_Of_Birth,Father_Name,Address,Salary,Email_Id,Phone_Number,Occupation,PANCARD,AADHARCARD,Type_of_acc,Amt_in_acc)
                                    VALUES (%s,%s,%s,%s,%s, %s,%s,%s,%s,%s,%s,%s,%s, %s, %s) """
    Name = input("Enter your name: ")
    Age = int(input("Enter your age: "))
    sex = input('Enter your gender-Male / Female / Other (M/F/O):')
    if sex.lower() == 'm':
        sex = 'Male'
    elif sex.upper() == 'F':
        sex = 'Female'
    elif sex.upper() == 'O':
        sex = 'Other'
    Date_of_Birth = input(
        "Enter your date of birth (Separate it with hyphens): ")
    Father_Name = input("Enter your Father's name: ")
    Address = input('Enter your current address:')
    salary = int(input('Enter your salary : '))
    email_id = input('Enter your email id : ')
    Phone_Number = int(input('Enter your Phone number : '))
    occupation = input('Enter your occupation : ')
    pancard = int(input('Enter the pan card number:'))
    aadhaarcard = int(input('Enter the aadhaar card number:'))
    type_of_acc = input(
        'Enter choice for the type of account-Current or Savings (C/S):')
    if type_of_acc.upper() == 'C':
        type_of_acc = 'Current'
    elif type_of_acc.upper() == 'S':
        type_of_acc = 'Savings'
    deposit = float(
        input('Enter the your starting amount to add into your account (Min>=1000):'))
    print()

    with open('Account.csv', 'a') as account_file:
        # The general row headers' list
        row = [acc_no, Name, Age, sex, Date_of_Birth, Father_Name, Address, salary,
               email_id, Phone_Number, occupation, pancard, aadhaarcard, type_of_acc, deposit]
        writing = csv.writer(account_file)
        writing.writerow(row)
    print('ACCOUNT HAS BEEN MADE . HERE IS YOUR ACCOUNT NUMBER: ', acc_no)
    print()

    # Pre-initialised input command parameters to be inserted into the sql table
    inputt2 = (acc_no, encrypt(Name), Age, encrypt(sex), encrypt(Date_of_Birth), encrypt(Father_Name), encrypt(Address),
               salary, encrypt(email_id), Phone_Number, encrypt(occupation), pancard, aadhaarcard, encrypt(type_of_acc), deposit)
    mycursor.execute(query, inputt2)
    mydb.commit()
    print()


# main function 2: depositing money into mysql table and csv file
def two_depositmoney(acc_no):
    if main == 0:
        print("No records of the account", acc_no, "exists")
        print()
    else:
        mycursor.execute(
            "Select * from personal_info where Account_No = '%d' " % (int(acc_no)))
        reading_list = mycursor.fetchone()
        updated_list = []
        depositing = float(input('Enter amount of money to deposit :'))
        print()
        for i in range(len(reading_list)):
            if int(reading_list[0]) == acc_no:
                if type(reading_list[i]) == str:       # Only strings can be encrypted, not integers; hence this condition
                    updated_list.append(
                        decryptor(bytes(reading_list[i], 'utf-8')))
                elif i == len(reading_list) - 1:
                    final_amt = reading_list[i]+depositing      # Deposit amount added to the balance
                    updated_list.append(final_amt)
                    mycursor.execute("UPDATE personal_info SET Amt_in_acc = '%f' WHERE Account_no = '%d'" % (
                        float(final_amt), int(acc_no)))
                    mydb.commit()
                else:
                    updated_list.append(reading_list[i])
        f = open('Account.csv', 'r')
        reading = csv.reader(f)
        reading_list = csvlist(reading)
        for i in range(len(reading_list)):
            if str(updated_list[0]) == str(reading_list[i][0]):
                reading_list[i] = updated_list      # Re-initialisation of the list for rewriting updated info
        f.close()
        with open('Account.csv', 'w') as account_file:
            writing = csv.writer(account_file)
            writing.writerows(reading_list)
        print('OK . MONEY HAS BEEN DEPOSITED')
        print()
    print()


# main function 3: withdrawing money into mysql table and csv file
def three_withdrawmoney(acc_no):
    if main == 0:
        print("No records of the account", acc_no, "exists")
        print()
    else:
        mycursor.execute(
            "Select * from personal_info where Account_No = '%d' " % (int(acc_no)))
        reading_list = mycursor.fetchone()
        updated_list = []
        withdrawal = float(input('Enter amount of money to withdraw :'))
        print()
        for i in range(len(reading_list)):
            if reading_list[len(reading_list)-1] >= withdrawal:
                if int(reading_list[0]) == acc_no:
                    if type(reading_list[i]) == str:
                        updated_list.append(
                            decryptor(bytes(reading_list[i], 'utf-8')))
                    elif i == len(reading_list) - 1:
                        final_amt = reading_list[i] - withdrawal    # Balance after deduction
                        updated_list.append(final_amt)
                        mycursor.execute("UPDATE personal_info SET Amt_in_acc = '%f' WHERE Account_no = '%d'" % (
                            float(final_amt), int(acc_no)))
                        mydb.commit()
                    else:
                        updated_list.append(reading_list[i])
            else:
                print("Insufficient balance. Please check!")
                print()
                break
        f = open('Account.csv', 'r')
        reading = csv.reader(f)
        reading_list = csvlist(reading)
        for i in range(len(reading_list)):
            if str(updated_list[0]) == str(reading_list[i][0]):
                reading_list[i] = updated_list
        f.close()
        with open('Account.csv', 'w') as account_file:
            writing = csv.writer(account_file)
            writing.writerows(reading_list)
        print('OK . MONEY HAS BEEN WITHDRAWN. Check your balance.')
        print()
    print()


# main function 4: calling data for account balance from csv file after checking it with mysql table for corruption and changing data in csv file if there is
def four_balanceenquiry(acno):
    if main == 0:
        print("No records of the account", acno, "exists")
        print()
    else:
        mycursor.execute(
            "Select Amt_in_acc from personal_info where Account_no = '%d'" % (int(acno)))
        amt = mycursor.fetchone()
        with open('Account.csv', 'r') as account_file:
            reading = csv.reader(account_file)
            reading_list = csvlist(reading)
            for i in reading_list:
                if int(i[0]) == acno:
                    if float(i[len(i)-1]) == float(amt[0]):
                        print(
                            "The balance left in your account is Rs.", amt[0])
                        print()
                        break
    print()

# main function 5: calling all data for account number from csv file after checking it with mysql table for corruption and changing data in csv file if there is
def five_showrecord(acc_no):
    file_check('Account.csv')
    if main == 0:
        print("No records of the account", acc_no, "exists")
        print()
    else:
        mycursor.execute(
            "Select * from personal_info where Account_no = '%d'" % (int(acc_no)))
        record = mycursor.fetchall()
        decryptrecord = []
        for i in record:
            if i[0] == acc_no:
                for j in i:
                    if type(j) == str:
                        decryptrecord.append(decryptor(bytes(j, 'utf-8')))
                    else:
                        decryptrecord.append(j)
        count = 0
        with open('Account.csv', 'r') as file:
            reading = csv.reader(file)
            readingrows = csvlist(reading)
            for i in readingrows:
                if i[0] == str(acc_no):
                    for j in range(len(i)):
                        if i[j] == decryptrecord[j]:
                            continue
                        else:
                            count = 1
                            break
        print(decryptrecord[0])
        if count == 1:
            for i in range(len(decryptrecord)):
                print(head[i], ":", decryptrecord[i])
                if i < 4 and readingrows[i][0] == str(decryptrecord[0]):
                    readingrows[i] = decryptrecord
                    with open('Account.csv', 'w') as file:
                        writing = csv.writer(file)
                        writing.writerows(readingrows)
    print()


# displaying file
def displayfile(filename, accountno):
    if filename[-1:-5:-1] == 'vsc.':
        pass
    else:
        filename = filename+'.csv'
    with open(filename, 'r') as account_file:
        reading = csv.reader(account_file)
        for line in reading:
            if line != [] and line[0] == str(accountno):
                for detail in range(len(line)):
                    print(head[detail], line[detail], sep=" : ")
                print()
    print()


# returning total amount after increasing principal with compound interest
def compound_interest(principal, timeaorb, interest):
    if timeaorb.lower() == 'a':
        timeinyrs = 5
    elif timeaorb.lower() == 'b':
        timeinyrs = 8
    print("The amount to be returned is : ",
          principal * (1+(interest/100))*timeinyrs)
    print()
    return (principal * (1+(interest/100))*timeinyrs)
    print()
    print()
    

# main function 6: making loan table in mysql table and csv file
def six_loan(acno):
    detailcount = 0
    query = """Insert into Loans (Account_no, AUTO, HOME, HEALTH, STUDENT_LOAN , MORTGAGE) VALUES (%s,%s,%s,%s,%s,%s)"""

    autol = healthl = homel = studentl = mortgagel = 0
    print('''Enter 'l' to avail for an auto loan
Enter 'm' to avail for a health loan
Enter 'n' to avail for a home loan
Enter 'p' to avail for a student loan
Enter 'q' to avail for a mortgage loan
Enter 'z' for none of the above ''')
    print()
    while True:
        loanchoice = int(input("Enter your choice from the above:"))
        print()
        if loanchoice in range(6):
            if loanchoice != 0:
                timer = input("Enter 'a' for repaying the loan in 5 years and enter 'b' \n\
for repaying it in 8 years: ")
                if timer.lower() == 'a' or timer.lower() == 'b':
                    timer = timer.lower()
                else:
                    print("Invalid choice")
                    print(
                        "Default timer is 8 years; to correct it delete and recreate your record")
                    print()
                    timer = 'b'
            if loanchoice.upper() == 'L':
                autol = float(
                    input("Enter the amount to be provided for the auto loan: "))
                autol = compound_interest(autol, timer, highrate)
                detailcount += 1
            elif loanchoice.upper() == 'M':
                healthl = float(
                    input("Enter the amount to be provided for the health loan: "))
                healthl = compound_interest(healthl, timer, highrate)
                detailcount += 1
            elif loanchoice.upper() == 'N':
                homel = float(
                    input("Enter the amount to be provided for the home loan: "))
                homel = compound_interest(homel, timer, highrate)
                detailcount += 1
            elif loanchoice.upper() == 'P':
                studentl = float(
                    input("Enter the amount to be provided for the Student loan: "))
                studentl = compound_interest(studentl, timer, highrate)
                detailcount += 1
            elif loanchoice.upper() == 'Q':
                mortgagel = float(
                    input("Enter the amount to be provided for the mortgage loan: "))
                mortgagel = compound_interest(mortgagel, timer, highrate)
                detailcount += 1
            elif loanchoice.upper() == 'Z':
                break
            else:
                cont = input(
                    "The option doesn't exist... Press 'y to continue and 'n' move on from loans: ")
                if cont.lower() == 'n':
                    break
                else:
                    print('No loan is to be availed; moving on...')
                    break
            print()
    if detailcount >= 1:
        print(detailcount, "loans have been availed as of now.")
        print()
    lrow = [acno, autol, healthl, homel, studentl, mortgagel]
    tablec = tuple(lrow)
    mycursor.execute(query, tablec)
    mydb.commit()

    file = open("Loan_avail.csv", 'a')
    writing = csv.writer(file)
    writing.writerow(lrow)
    file.close()
    print()


# main function 7: making insurance table in mysql table and csv file
def seven_insurance(acc_no):
    query = """Insert into Insurance (Account_no, Auto, Health, Life, Property) VALUES (%s,%s,%s,%s,%s)"""
    autoi = healthi = lifei = propertyi = 0
    print("Fill in the following with Yes or no: ")
    print()
    detailcount = 0
    autoi = input("Do you have an auto insurance? ")
    print()
    if autoi.lower() == 'yes':
        autocode = input("Enter your 4-digit auto code:")
        autoi = autocode
        detailcount += 1
    else:
        autoi = 0
    print()
    healthi = input("Do you have a health insurance? ")
    if healthi.lower() == "yes":
        healthcode = input("Enter the 4-digit health code:")
        healthi = healthcode
        detailcount += 1
    else:
        healthi = 0
    print()
    lifei = input("Do you have life insurance? ")
    if lifei.upper() == "YES":
        lifecode = input("Enter your 4-digit life code:")
        lifei = lifecode
        detailcount += 1
    else:
        lifei = 0
    print()
    propertyi = input("Do you have a property insurance? ")
    if propertyi.upper() == "YES":
        propertycode = input("Enter your 4-digit property code:")
        propertyi = propertycode
        detailcount += 1
    else:
        propertyi = 0
    print()
    if detailcount >= 1:
        print(detailcount, "insurance codes have been updated.")
    print()
    irow = [acc_no, autoi, healthi, lifei, propertyi]
    file = open("Insurance.csv", 'a')
    writing = csv.writer(file)
    writing.writerow(irow)
    file.close()
    tablec = tuple(irow)
    mycursor.execute(query, tablec)
    mydb.commit()
    print()
    print()


# main function 8: deleting account record in mysql table and csv file
def eight_delete_acc(acno):
    check = 0
    if main == maini == mainl == 0:
        print("No records of the account", acno, "exists")
        print()
    else:
        with open('Account.csv', 'r') as file:
            reading = csv.reader(file)
            readingrows = csvlist(reading)

        with open('Account.csv', 'w') as file:
            file.truncate(0)
            writing = csv.writer(file)
            for linenum in range(len(readingrows)):
                if readingrows[linenum][0] != str(acno):
                    writing.writerow(readingrows[linenum])
                else:
                    check += 1
        if check != 1:
            print("No records of", acno, "is present in the Accounts section")
            print()

        with open('Loan_avail.csv', 'r') as file:
            reading = csv.reader(file)
            readingrows = csvlist(reading)

        with open('Loan_avail.csv', 'w') as file:
            file.truncate(0)
            writing = csv.writer(file)
            for linenum in range(len(readingrows)):
                if readingrows[linenum][0] != str(acno):
                    writing.writerow(readingrows[linenum])
                else:
                    check += 1
        if check != 2:
            print("No records of',acno,'is present in the Loan section")
            print()

        with open('Insurance.csv', 'r') as file:
            reading = csv.reader(file)
            readingrows = csvlist(reading)

        with open('Insurance.csv', 'w') as file:
            file.truncate(0)
            writing = csv.writer(file)
            for linenum in range(len(readingrows)):
                if readingrows[linenum][0] != str(acno):
                    writing.writerow(readingrows[linenum])
                else:
                    check += 1
        if check != 3:
            print("No records of',acno,'is present in the Insurance section")
            print()
        mycursor.execute(
            "Delete from insurance where account_no = '%d'" % int(acno))
        mycursor.execute(
            "Delete from loans where account_no = '%d'" % int(acno))
        mycursor.execute(
            "Delete from personal_info where account_no = '%d'" % int(acno))
        mydb.commit()
        print("The records have been deleted successfully!! ")
    print()
    print()


# main function 9: modifying account record in mysql table and csv file
def nine_modifyaccount(acno):
    if main == 0:
        print("No records of the account", acno, "exists")
        print()
    else:
        with open('Account.csv', 'r') as file:
            reading = csv.reader(file)
            readinglist = csvlist(reading)
            for i in readinglist:
                if int(i[0]) == acno:
                    modifylist = i
        print("Current record: ")
        print()
        displayfile('Account', acno)
        detailcount = 0
        while True:
            ch = int(input('''Enter your choice to modify:
    1.Name , 2.Sex , 3. Father's Name , 4. Address , 5.Salary, 6.Email ID , 7.Phone number 8.Occupation: '''))
            print()
            if ch == 1:
                name = input('Enter your new name :')
                print()
                modifylist = replacelist(modifylist, modifylist[1], name)
                name = encrypt(name)
                name = name.decode("utf-8")
                mycursor.execute(
                    "UPDATE personal_info SET Name = '%s' where Account_no = '%d'" % (name, int(acno)))
                detailcount += 1
            elif ch == 2:
                sex = input('Enter your new sex:')
                modifylist = replacelist(modifylist, modifylist[3], sex)
                sex = encrypt(sex)
                sex = sex.decode("utf-8")
                mycursor.execute(
                    "UPDATE personal_info SET Sex = '%s' where Account_no = '%d'" % (sex, int(acno)))
                detailcount += 1
            elif ch == 3:
                fname = input("Enter your new Father's Name:")
                modifylist = replacelist(modifylist, modifylist[5], fname)
                fname = encrypt(fname)
                fname = fname.decode("utf-8")
                mycursor.execute(
                    "UPDATE personal_info SET Father_Name = '%s' where Account_no = '%d'" % (fname, int(acno)))
                detailcount += 1
            elif ch == 4:
                address = input('Enter your new address:')
                modifylist = replacelist(modifylist, modifylist[6], address)
                address = encrypt(address)
                mycursor.execute("UPDATE personal_info SET Address = '%s' where Account_no = '%d'" % (
                    address, int(acno)))
                detailcount += 1
            elif ch == 5:
                salary = input('Enter your new salary:')
                modifylist = replacelist(modifylist, modifylist[7], salary)
                mycursor.execute("UPDATE personal_info SET Salary = '%s' where Account_no = '%d'" % (
                    float(salary), int(acno)))
                detailcount += 1
            elif ch == 6:
                email_id = input('Enter your new email id :')
                modifylist = replacelist(modifylist, modifylist[8], email_id)
                email_id = encrypt(email_id)
                email_id = email_id.decode("utf-8")
                mycursor.execute("UPDATE personal_info SET Email_Id = '%s' where Account_no = '%d'" % (
                    email_id, int(acno)))
                detailcount += 1
            elif ch == 7:
                phoneno = input('Enter your new phone number:')
                modifylist = replacelist(modifylist, modifylist[9], phoneno)
                mycursor.execute("UPDATE personal_info SET Phone_Number = '%s' where Account_no = '%d'" % (
                    int(phoneno), int(acno)))
                detailcount += 1
            elif ch == 8:
                job = input('Enter your new job:')
                modifylist = replacelist(modifylist, modifylist[10], job)
                job = encrypt(job)
                job = job.decode("utf-8")
                mycursor.execute(
                    "UPDATE personal_info SET Occupation = '%s' where Account_no = '%d'" % ((job), int(acno)))
                detailcount += 1
            else:
                print('Wrong option')
            print()

            cont = input("Enter 'y' to continue and any other key to stop: ")
            print()
            if cont.lower() != 'y':
                break
            if detailcount >= 1:
                print(detailcount, " details have been modified. ")
                print()
        mydb.commit()

        with open('Account.csv', 'w') as account_file:
            account_file.truncate(0)
            writing = csv.writer(account_file)
            if readinglist != []:
                writing.writerows(readinglist)
        print("Final updated record: ")
        displayfile('Account', acno)
        print()
    print()


defaults()  # readymade records

#main code containing menu-driven part and exception handling
def maincode():
    global user
    while True:
        user = input(
            "Enter 'n' if you don't have an existing account and enter 'e' if you're an existing member: ")
        print()
        if user.lower() == 'n':
            print('''Hello New user!! You will have to create your account before proceeding. 
First fill in your personal details
Next, enter your insurance details
Enter any other key to exit first time procedure ''')
            print()
            try:
                one_createacc()
                print()
            except Exception as e:
                print(e,'Error has occurred.')
                print('Please try again')
                print()
                one_createacc()
                print()
            acno = int(
                input("Enter your newly generated account number to proceed with insurance: "))
            teblock(seven_insurance,acno)
            acc_check(acno)
            if main == 1 and maini == 1:
                print("All details have been initialised; let's move ahead!!")
                print()
                user = 'e'
            print()
        print("Sign in with your account number below: ")
        if user.lower() == 'e':
            accountno = int(input('Enter your account number:'))
            print('''MENU
1. Deposit money into the account           
2. Withdraw money into the account          
3. Balance enquiry
4. Show account holder's information           
5. Availing a loan          
6. Close your account               
7. Modify the information in your account
0. Exit''')
            while True:
                print()
                acc_check(accountno)
                print(main,maini)
                choice = int(input('Enter your choice : '))
                if choice == 0:
                    print('Exitting...')
                    print()
                    break
                elif choice == 1:
                    teblock(two_depositmoney,accountno)
                elif choice == 2:
                    teblock(three_withdrawmoney,accountno)
                elif choice == 3:
                    teblock(four_balanceenquiry,accountno)
                elif choice == 4:
                    teblock(five_showrecord,accountno)
                elif choice == 5:
                    teblock(six_loan,accountno)
                elif choice == 6:
                    teblock(eight_delete_acc,accountno)
                elif choice == 7:
                    teblock(nine_modifyaccount,accountno)
                print()
        else:
            exitl = input("Invalid option; press 'x' to exit and any other key to continue execution : ")
            print()
            if exitl.lower() == 'x':
                break
            print()
        print()
    print()

#try and except block for exception handling of maincode function
try:   
    maincode()
except Exception as e:
    print(e,'Error has occurred.')
    print('Please try again')
    print()
    maincode()
print("Program execution has ended successfully!!!!! ")
