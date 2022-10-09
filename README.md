###Continuous assessment - Protection of information based on sensitivity and privilege levels

This programme demonstrates the controlling the access of user data based on the sensitivity 
of data.

In the developed program, there are two types of users which are STAFF and PATIENT. 
Anyone who has a verification code and creates a user account from the respective privilege 
level. The verification codes are as follows.

| Privilege level | Verification Code |
|-----------------|-------------------|
| 5               | p001              |
| 4               | ph019             |
| 3               | lb001             |
| 2               | nur019            |
| 1               | dr100             |

A user account with a particular privilege level cannot be created without the respective user 
verification code. After the creation of a user account, the detail of the user is added to the 
config.csv file. If the username exists, the account creation is avoided by the system.

After creating a user account, a user can log into the system via the credentials. If the provided 
credentials are incorrect, the user will get 3 tries. After 3 attempts, the system will terminate. 

After logging in to the system, a user can view or edit details according to their privilege levels. 
To store those data an SQLite database is used (data.db). The privilege levels have been defined 
as follows with the data sensitivity.

| Privilege Level | Personal Details View \| Edit | Sickness Details View \| Edit | Drug Prescription View \| Edit | Lab Test Prescription View \| Edit |
|-----------------|:-----------------------------:|:-----------------------------:|:------------------------------:|:----------------------------------:|
| 5               |           Yes\| Yes           |           Yes \| Yes          |           Yes \| Yes           |             Yes \| Yes             |
| 4               |            Yes\| No           |            Yes\| No           |           Yes \| Yes           |             Yes \| Yes             |
| 3               |            Yes\| No           |            Yes\| No           |            No \| No            |             Yes \| Yes             |
| 2               |            Yes\| No           |            Yes\| No           |           Yes \| Yes           |              No \| No              |
| 1               |           Yes\| Yes           |            Yes\| No           |            Yes\| No            |              Yes\| No              |

Those privilege levels have been mapped to the data_sensitivity dictionary in the program as 
the following format.
• {privilege_level: {data_type:[view_permission,edit_permission]}}
The program will be as follows.
data_map = {0: "personal_details", 1: "sickness_details", 2: "drug_prescription", 3: 
"lab_test_prescription"}

data_sensitivity = {
 5: {0: [1, 1], 1: [1, 1], 2: [1, 1], 3: [1, 1]},
 4: {0: [1, 0], 1: [1, 0], 2: [1, 1], 3: [1, 1]},
 3: {0: [1, 0], 1: [1, 0], 2: [0, 0], 3: [1, 1]},
 2: {0: [1, 0], 1: [1, 0], 2: [1, 1], 3: [0, 0]},
 1: {0: [1, 1], 1: [1, 0], 2: [1, 0], 3: [1, 0]},
}

Only the user with the privilege level of 5 has the ability to add a record to the database. The 
privilege level of 1 (users with PATIENT user type) can view only their records. But users with 
other privilege levels can view the other users’ details as well. Once a user selects a specific 
record by its visit id, the user has the ability to edit the details according to his privilege level

This program uses an SQLite database to store the data. When doing the CRUD operations 
with the database on the user inputs, prepared statements have been used to prevent SQL 
injection. Most of the invalid user inputs have been handled so that the chance of the system 
providing unexpected outputs with invalid user inputs is less. Passwords have been hashed with 
md5 hashing format. 

Some of the sample data have been added and the credentials of the user account are as follows.

| Username | Password |
|----------|:--------:|
| Nimal    | password |
| Sandun   | password |
| Kamal    | password |
| Dasun    | password |
| Udith    | password |
| Pramod   | password |
| Mahela   | password |
| Pamudu   | password |
