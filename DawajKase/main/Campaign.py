from datetime import datetime

class Campaign:
    def __init(eslf):
        pass
    
    def __init__(self, id, title, description, shortDescription,
                 targetMoneyAmount, currentMoneyAmount, startDate, endDate,
                 status, imageURL, organizerID, categoryID,
                 creationDate, modifyDate):
        self.id = id
        self.title = title
        self.description = description
        self.shortDescription = shortDescription
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
            'shortDescription': self.shortDescription,
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
    
    def has_finished(self):
        if isinstance(self.endDate, str):
            end_date = datetime.fromisoformat(self.endDate)
        else:
            end_date = self.endDate

        return datetime.now() > end_date or self.targetMoneyAmount <= self.currentMoneyAmount