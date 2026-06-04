class BaseRepository:
    def __init__(self, session, model):
        self.session = session
        self.model = model

    def add(self, entity):
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity

    def get(self, entity_id):
        return self.session.get(self.model, entity_id)

    def list(self):
        return self.session.query(self.model).all()

    def delete(self, entity):
        self.session.delete(entity)
        self.session.commit()
