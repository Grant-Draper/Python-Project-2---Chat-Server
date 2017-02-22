import hashlib, uuid

password = "brainsno"

salt = uuid.uuid4().hex
print("salt", salt)

hashed_password = hashlib.sha512((password + salt).encode("utf-8")).hexdigest()
print("hashed pass", hashed_password)

hashed_pass_nosalt = hashlib.sha512((password).encode("utf-8")).hexdigest()
print("hashed pass, without salt 1", hashed_pass_nosalt)

hashed_pass_nosalt2 = hashlib.sha512((password).encode("utf-8")).hexdigest()
print("hashed pass, without salt 2", hashed_pass_nosalt2)

hashed_pass_nosalt3 = hashlib.sha512((password).encode("utf-8")).hexdigest()
print("hashed pass, without salt 3", hashed_pass_nosalt3)

hashed_pass_nosalt4 = hashlib.sha512((password).encode("utf-8")).hexdigest()
print("hashed pass, without salt 4", hashed_pass_nosalt4)



## SQL code working to find screename, if password matches
"""
select ScreenName
from Users

inner join Passwords
on Users.User_ID=Passwords.User_ID

where Passwords.Password='nofear';
"""



















