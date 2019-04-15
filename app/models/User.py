from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
class User:


    def __init__(self, db, _id = None, username = None, email = None, password = None):
        self.db = db
        self._id = id
        self.username = username
        self.email = email
        self.password = self.set_password(password)
        self.password_to_check = password
        self.verified = False

    def verify(self):
        if (self.username == None and self.email == None):
            return False
        all = self.db.users.find()

        cursor = self.db.users.find_one({"$or":[{"username":self.username},{"email":self.email}]}, {'email':1,'username':1,'password':1})

        if (cursor == None): return False
        if (self.check_password(cursor['password'])):
            self.email = cursor['email']
            self.username = cursor['username']
            self.password_to_check = None
            self.password = cursor['password']
            self.verified = True
            return True
        return False

    def set_password(self, pw):
        if (pw == None): return None
        return generate_password_hash(pw)

    def check_password(self, pw):
        if (self.password == None): return False
        return check_password_hash(pw,self.password_to_check)

    def create(self):
        size = self.db.users.find( {"$or":[{"username":self.username},{"email":self.email}]}).limit(1).count(with_limit_and_skip=True)
        if (size):
            return False
        self.db.users.insert_one({
            '_id':ObjectId(),
            'username':self.username,
            'email':self.email,
            'password':self.password
        })
        return True;

    @classmethod
    def exists(cls, db, query):
        options = {"_id":0, "value": 1}
        size = db.users.find(query,options).limit(1).count(with_limit_and_skip=True)
        if (size):
            return True
        return False


    @classmethod
    def get_all(cls, db):
        return db.users.find()
