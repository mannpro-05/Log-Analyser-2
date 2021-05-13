from modules.models import User
from modules import bcrypt,db
print("-------------------Admin Account Creation---------------------------------------------------------------")
username = input('Enter username: ')
email = input('Enter email ID: ')
while True:
    password = input('Password: ')
    cpassword = input('Confirm Password: ')

    if password == cpassword and (len(password)!=0):
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username ,email=email, password=hashed_password, admin=1)
        db.session.add(user)
        db.session.commit()
        print("Your Username is: "+ username + " Your emailID is: "+email)
        break
    else:
        print('Please enter the password again!!!')
