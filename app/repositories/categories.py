"""class for static methods around the Category table"""

from app import db
from app.models.category import Category

class CategoryRepository:

    @staticmethod
    def name_to_category(category_name: str) -> Category:
        """
        Returns the id associated with a category name, None if it doesn't exist
        """
        return Category.query.filter_by(name=category_name).first()


    @staticmethod
    def add_category(name:str) -> Category:
        """
        Adds a category to the table
        @returns the new category
        """

        if CategoryRepository.name_to_category(name) is not None:
            raise ValueError(f"Tried to add an already-existing category, {name}")

        new_cat = Category(name)
        
        db.session.add(new_cat)
        
        db.session.commit()

        return new_cat
        
        
    @staticmethod
    def delete_category(name:str) -> None:
        """
        delete a category to the table
        """

        cat = CategoryRepository.name_to_category(name)

        if cat is None:
            print("WARNING: Tried to delete a non-existant category")
            return

        db.session.delete(cat)
        db.session.commit()
    
