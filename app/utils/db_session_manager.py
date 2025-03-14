from app.config import db


class DBSessionManager:

    @staticmethod
    def commit():
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        finally:
            db.session.close()
