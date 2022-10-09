import hashlib, csv, sqlite3

data_map = {0: "personal_details", 1: "sickness_details", 2: "drug_prescription", 3: "lab_test_prescription"}

#defines the privileges distribution of data among users
data_sensitivity = {
    5: {0: [1, 1], 1: [1, 1], 2: [1, 1], 3: [1, 1]},
    4: {0: [1, 0], 1: [1, 0], 2: [1, 1], 3: [1, 1]},
    3: {0: [1, 0], 1: [1, 0], 2: [0, 0], 3: [1, 1]},
    2: {0: [1, 0], 1: [1, 0], 2: [1, 1], 3: [0, 0]},
    1: {0: [1, 1], 1: [1, 0], 2: [1, 0], 3: [1, 0]},
}

conn = sqlite3.connect('data.db')

def select_execute(sql, params):
    global conn
    c = conn.cursor()
    c.execute(sql, params)
    res = c.fetchall()
    conn.commit()
    return res


def update_execute(sql, params):
    global conn
    c = conn.cursor()
    c.execute(sql, params)
    conn.commit()

def insert_execute(sql,params):
    global conn
    c = conn.cursor()
    c.execute(sql, params)
    conn.commit()

def get_prev_phrases(level):
    view = []
    edit = []
    for i in data_sensitivity[level]:
        if data_sensitivity[level][i][0] == 1:
            view.append(data_map[i])
        if data_sensitivity[level][i][1] == 1:
            edit.append(data_map[i])
    return view, edit


def session(user):
    ui_map = {'personal_details': "Personal Details: ", 'sickness_details': "Sickness Details: ",
              'drug_prescription': "Drug Prescriptions: ", 'lab_test_prescription': "Lab Test prescriptions: "}
    privilege = user.privilege
    view, edit = get_prev_phrases(int(privilege))
    view_str = ','.join(view)
    while (True):
        if (int(privilege) == 5):
            interface = "0-Logout\n1-Get a specific visit details\n2-Get All Visit Details\n3-Add a visit details\n"
        else:
            interface = "0-Logout\n1-Get a specific visit details\n2-Get All Visit Details\n"

        mode = int(input(interface))
        if (mode == 1):
            visit_id = int(input("Enter Visit Id: "))
            if (int(privilege) == 1):
                sql = """select """ + view_str + """ from details where visit_id=? and username='""" + user.username + """';"""
            else:
                sql = """select """ + view_str + """ from details where visit_id=?;"""
            params = [visit_id]
            records = select_execute(sql, params)
            if (len(records) == 0):
                print("No Records")
                continue
            for i in range(len(view)):
                print(ui_map[view[i]], end=' ')
                print(records[0][i])

            print("---------------------------")
            print("Edit details: ")
            for i in range(len(edit)):
                print(i + 1, "-", ui_map[edit[i]], end=' | ')
            print()
            print("0-Exit")
            field = int(input())
            if (field not in range(1, len(edit) + 1) and field !=0):
                print("Please try again. You entered wrong details")
                continue
            if (field==0):
                continue
            data = input("Enter new data: ")
            sql = """update details set """ + edit[field - 1] + """=? where visit_id=?"""
            params = [data, visit_id]
            update_execute(sql, params)
        elif (mode == 2):
            if (int(privilege) == 1):
                sql = """select * from details where username='""" + user.username + """';"""
            else:
                sql = """select * from details;"""
            records = select_execute(sql, [])
            if (len(records) == 0):
                print("No Records")
                continue
            for record in records:
                print("Visit id:", record[0])
                for i in range(len(view)):
                    print(ui_map[view[i]], end=' ')
                    print(record[i + 2])
                print("---------------")
        elif (mode == 0):
            print("Logging out from the system")
            return
        elif (int(privilege) == 5 and mode ==3):
            username = input("Enter username: ")
            if username not in User.getAllUsers('config.csv'):
                print("User doesn't exist in the system. Try again")
                continue
            personal_details = input("Enter personal details: ")
            sickness_details = input("Enter sickness details: ")
            drug_prescription = input("Enter drug details: ")
            lab_test_prescription = input("Enter lab test prescription details: ")
            sql = """insert into details (username,personal_details,sickness_details,drug_prescription,lab_test_prescription)
            values (?,?,?,?,?);"""
            params = [username,personal_details,sickness_details,drug_prescription,lab_test_prescription]
            insert_execute(sql,params)
        else:
            print("Invalid input")
            continue


class User:

    def __init__(self, username, password, user_type, privilege):
        self.username = username
        self.password = password
        self.user_type = user_type
        self.privilege = privilege

    @staticmethod
    def getAllUsers(filepath):
        users = {}
        with open(filepath, 'r') as file:
            csvreader = csv.reader(file, delimiter=',')
            for row in list(csvreader)[1:]:
                temp_user = User(row[0], row[1], row[2], row[3])
                users[row[0]] = temp_user

        return users

    @staticmethod
    def login(username, password, users):
        if username not in users:
            return False
        for _ in range(3):
            if (users[username].password == hashlib.md5(password.encode()).hexdigest()):
                return users[username]
            return False

    @staticmethod
    def register(username, password, user_type, privilege):
        password = hashlib.md5(password.encode()).hexdigest()
        record = '\n' + username + ',' + password + ',' + user_type + ',' + str(privilege)
        with open('config.csv', 'a') as f:
            f.write(record)
        return True

while True:
    users = User.getAllUsers('config.csv')
    print("Data management system")
    type = int(input("1-User Registration\n2-User Login\n3-Exit\n"))

    if (type == 2):
        print("User Login")
        username = input("Enter user name: ")
        password = input("Enter password: ")

        user = User.login(username, password, users)

        for i in range(2):
            if (user != False):
                print("Welcome ", user.username)
                session(user)
                break
            else:
                print("Wrong credentials. You have", (3 - i - 1), "tries")
                username = input("Enter user name: ")
                password = input("Enter password: ")
                user = User.login(username, password, users)

        if (user == False):
            exit("You have entered wrong credentials 3 times.")
    elif (type == 1):
        print("User Registration")
        user_types = {1: "STAFF", 2: "PATIENT"}
        flag = False
        for i in range(3):
            username = input("Enter username: ")
            if username in users:
                print("Username exists. Enter a different username")
                continue
            password = input("Enter password: ")
            user_type = int(input("Select User Type\n1-STAFF\n2-PATIENT\n"))
            if user_type == 1:
                privilege = int(input("Enter privilege level: "))
            else:
                privilege = 1
            code = input("Enter verification code: ")
            codes = {0: 'p001', 1: 'ph019', 3: 'lb001', 4: 'nur019', 5: 'dr100'}
            if privilege not in codes or user_type not in user_types:
                print("Invalid argument. Please try again")
                continue
            if codes[privilege] != code:
                print("Invalid verification code")
                continue
            flag = User.register(username, password, user_types[user_type], privilege)
            break
        if (flag == True):
            print("User Registration Complete")
        else:
            exit("You have entered wrong details 3 times.")
    elif (type == 3):
        break
    else:
        print("Invalid input")

conn.close()