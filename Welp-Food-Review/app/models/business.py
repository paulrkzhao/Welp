from .db_operations import db_operations
from base64 import b64encode
class Business:
    def __init__(self, id, businessName, address, phone, email, website, description, hoursOfOp, password, rating, photo, categories):
        self.db_ops = db_operations()
        self.id = id
        self.businessName = businessName
        self.address = address
        self.phone = phone
        self.email = email
        self.password = password
        self.description = description
        self.rating = rating
        self.website = website
        self.hoursOfOp = hoursOfOp
        self.photo = photo
        self.categories = categories
        self.card = {"businessName":self.businessName, "address":self.address, "phone":self.phone, "email":self.email, "description":self.description, "password":self.password, "rating":self.rating, "website":self.website, "hoursOfOp":self.hoursOfOp, "photo":self.photo, "id":self.id, "categories":self.categories}

    @staticmethod
    def getBusinessByEmail(email):
        db_ops = db_operations()
        if not db_ops.exists("Businesses", "Email", email):
            return None
    
        business_row = db_ops.get_row("Businesses", "Email", email)
        return business_row

    def getPhoto(self):
        if self.photo:
            return self.photo
        
        with open("app/static/images/defaultStore.png", "rb") as file:
            blob_data = file.read()
            return blob_data 
        return None

    def setPhoto(self, newPhoto):
        
        data = self.convertToBinaryData(newPhoto)
        query = """UPDATE Businesses SET BusinessPhoto = %s WHERE BusinessID = %s"""
        params = (data, self.id)
        self.db_ops.send_query(query, params)

    
    def convertToBinaryData(self, filename):
        # Convert digital data to binary format
        with open(filename, 'rb') as file:
            binaryData = file.read()
        return binaryData

    @staticmethod
    def getBusinessByID(ID):
        db_ops = db_operations()
        if not db_ops.exists("Businesses", "BusinessID", ID):
            return None
    
        business_row = db_ops.get_row("Businesses", "BusinessID", ID)
        return business_row

    def checkPassword(self, password):
        return self.password == password
    
    @staticmethod
    def createNew(businessName, address, phone, password, email, description):
        db_ops = db_operations()
        query = f"INSERT INTO Businesses (BusinessName, Address, Phone, Password, Email, Description) VALUES ('{businessName}', '{address}', '{phone}', '{password}', '{email}', '{description}');"
        db_ops.send_query(query)

    @staticmethod
    def getAll():
        db_ops = db_operations()
        return db_ops.get_all("Businesses")

    @staticmethod
    def search(query):
        db_ops = db_operations()
        # Perform your search logic based on the query using self.db_ops
        # For example, searching for businesses with a matching name
        search_query = f"SELECT * FROM Businesses WHERE BusinessName LIKE '%{query}%'"
        results = db_ops.get_all_query(search_query)


        return results

    @staticmethod
    def getReviews(id):
        db_ops = db_operations()

        reviews = db_ops.get_row("ReviewsDetails", "BusinessID", id, mult = True)
        return reviews
    
    def updateRating(self, updated):
        
        query = f"UPDATE Businesses SET Rating = {float(updated)} WHERE BusinessID = {self.id}"
        self.db_ops.send_query(query)

    def printer(self):
        print(self.card)

    def updateDetails(self, businessName, address, phone, email, description, category_id):
        
        self.businessName = businessName
        self.address = address
        self.phone = phone
        self.email = email
        self.description = description

        query = """
        UPDATE Businesses
        SET businessName = %s, address = %s, phone = %s, email = %s, description = %s, categoryID= %s
        WHERE BusinessID = %s;
        """

        params = (businessName, address, phone, email, description, category_id, self.id)

        self.db_ops.send_query(query, params)

    def delete(self):
        db_ops = db_operations()
        query = "DELETE FROM Businesses WHERE BusinessID = %s"
        db_ops.send_query(query, (self.id,))

