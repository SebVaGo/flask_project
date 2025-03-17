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

class AltDBSessionManager:
    def __init__(self):
        self.session = db.session

    def __enter__(self):
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type is None:
                self.session.commit()

            else:
                self.session.rollback()
        except Exception as e:
            self.session.rollback()
            raise e
        finally:
            self.session.close()
