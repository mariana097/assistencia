from app.models.aparelho import Aparelho
from app.repositories.base_repository import BaseRepository


class AparelhoRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session, Aparelho)
