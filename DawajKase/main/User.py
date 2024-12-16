class User:
    def __init__(self, id, firstName, lastName, email, pfpURL, role):
        self.id = id
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.pfpURL = pfpURL
        self.role = role
    
    def to_json(self):
        return {
            'id': self.id,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'email': self.email,
            'pfpURL': self.pfpURL,
            'role': self.role
        }

    def validate_user(self):
        # put validation logic here like fields lengths etc.
        pass
        