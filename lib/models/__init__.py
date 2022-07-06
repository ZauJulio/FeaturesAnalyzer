from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Model:

    @classmethod
    def findByUUID(cls, session, uuid):
        return session.query(cls).filter_by(uuid=uuid).all()
