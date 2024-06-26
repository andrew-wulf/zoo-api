from db import connect_to_db






import bcrypt
 
# Declaring our password
password = b'GeekPassword'
 
# Adding the salt to password
salt = bcrypt.gensalt()
# Hashing the password
hashed = bcrypt.hashpw(password, salt)
 
# printing the salt
print("Salt :")
print(salt)
 
# printing the hashed
print("Hashed")
print(hashed)

print(bcrypt.checkpw(b'abcd', hashed))