from app.config import db

class CategoryModel(db.Model):
    __tablename__ = "categories"
    __table_args__ = {'autoload_with': db.engine} 
