class User:
    def __init__(self, firstName, email):
        self.firstName = firstName
        self.email = email
    
    def to_json(self):
        return {
            'firstName': self.firstName,
            'email': self.email,
        }

    def validate_user(self):
        # put validation logic here like fields lengths etc.
        pass
        