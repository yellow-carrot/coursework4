from config import Config
from dao.model.user import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, bid):
        return self.session.query(User).get(bid)

    def get_all(self, filters):
        page = filters.get('page')

        if page is not None:
            result = self.session.query(User).paginate(int(page), Config.ITEMS_PER_PAGE, Config.MAX_PAGE).items
            return result

        return self.session.query(User).all()

    def get_by_name(self, name):
        return self.session.query(User).filter(User.name == name).first()

    def create(self, user_d):
        ent = User(**user_d)
        self.session.add(ent)
        self.session.commit()
        return ent

    def delete(self, rid):
        user = self.get_one(rid)
        self.session.delete(user)
        self.session.commit()

    def update(self, user_d):
        user = self.get_one(user_d.get("id"))
        user.name = user_d.get("name")
        user.password = user_d.get("password")
        user.role = user_d.get("role")

        self.session.add(user)
        self.session.commit()
