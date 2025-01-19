from app import db

class Category(db.Model):
        __tablename__ = 'categories'

        id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
        name = db.Column(db.String(100), nullable=False, unique=True)
        subcategories = db.relationship('Subcategory', backref='category', lazy=True, cascade="all, delete-orphan")
        
        def __repr__(self):
            return f"Category('{self.id}', '{self.name}')"


class Subcategory(db.Model):
        __tablename__ = 'subcategories'

        id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
        name = db.Column(db.String(100), nullable=False)
        category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)

        def __repr__(self):
            return f"Subcategory('{self.id}', '{self.name}', '{self.category_id}')"
