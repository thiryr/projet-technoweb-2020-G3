from app import db
from app.models.category import Category

class CategoryRepository:

    @staticmethod
    def name_to_id(category_name: str) -> int:
        """
        Returns the id associated with a category name, None if it doesn't exist
        """
        return Category.query.filter_by(name=category_name).first().id


    @staticmethod
    def add_category(name:str):
        """
        Adds a category to the table
        """

        if CategoryRepository.name_to_id(name) != None:
            raise ValueError("Tried to add an already-existing category")

        new_cat = Category(name)
        
        db.session.add(new_cat)
        
        db.session.commit()
    
