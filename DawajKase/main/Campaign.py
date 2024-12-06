class Campaign:
    def __init__(self, id, title, description, 
                 targetMoneyAmount, currentMoneyAmount, startDate, endDate,
                 status, imageURL, organizerID, categoryID,
                 creationDate, modifyDate):
        self.id = id
        self.title = title
        self.description = description
        self.targetMoneyAmount = targetMoneyAmount
        self.currentMoneyAmount = currentMoneyAmount
        self.startDate = startDate
        self.endDate = endDate
        self.status = status
        self.imageURL = imageURL
        self.organizerID = organizerID
        self.categoryID = categoryID
        self.creationDate = creationDate
        self.modifyDate = modifyDate
    
    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'targetMoneyAmount': self.targetMoneyAmount,
            'currentMoneyAmount': self.currentMoneyAmount,
            'startDate': self.startDate,
            'endDate': self.endDate,
            'status': self.status,
            'imageURL': self.imageURL,
            'organizerID': self.organizerID,
            'categoryID': self.categoryID,
            'creationDate': self.creationDate,
            'modifyDate': self.modifyDate
        }