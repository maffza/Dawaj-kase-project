class Comment:
    def __init__(self, id, commentText, creationDate, modifyDate, username):
        self.id = id
        self.commentText = commentText
        self.creationDate = creationDate 
        self.modifyDate = modifyDate
        self.username = username
    
    def to_json(self):
        return {
            'id': self.id,
            'commentText': self.commentText,
            'creationDate': self.creationDate,
            'modifyDate': self.modifyDate,
            'username': self.username
        }