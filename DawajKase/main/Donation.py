class Donation:
    def __init__(self, id, amount, message, username, creation_date):
        self.id = id
        self.amount = amount
        self.message = message
        self.username = username
        self.creation_date = creation_date
    
    def to_json(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'message': self.message,
            'username': self.username,
            'creation_date': self.creation_date,
        }
