class Post:
    def __init__(self, id, title, description, image_url, user_id, campaign_id):
        self.id = id
        self.title = title
        self.description = description
        self.image_url = image_url
        self.user_id = user_id
        self.campaign_id = campaign_id

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'image_url': self.image_url,
            'user_id': self.user_id,
            'campaign_id': self.campaign_id,
        }
