class Tier:
    def __init__(self, id, description, amount, campaignID):
        self.id = id
        self.description = description
        self.amount = amount
        self.campaignID = campaignID

    def to_json(self):
        return {
            'id': self.id,
            'description': self.description,
            'amount': self.amount,
            'campaignID': self.campaignID,
        }
