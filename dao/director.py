from config import Config
from dao.model.director import Director


class DirectorDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, bid):
        return self.session.query(Director).get(bid)

    def get_all(self, filters):
        page = filters.get('page')

        if page is not None:
            result = self.session.query(Director).paginate(int(page), Config.ITEMS_PER_PAGE, Config.MAX_PAGE).items
            return result

        return self.session.query(Director).all()

    def create(self, director_d):
        ent = Director(**director_d)
        self.session.add(ent)
        self.session.commit()
        return ent

    def delete(self, rid):
        director = self.get_one(rid)
        self.session.delete(director)
        self.session.commit()

    def update(self, director_d):
        director = self.get_one(director_d.get("id"))
        director.name = director_d.get("name")

        self.session.add(director)
        self.session.commit()
