"""class for static methods around the Category table"""

from app import db
import app.models.category as category_model


    
def name_to_category(category_name: str) -> category_model.Category:
    """
    Returns the id associated with a category name, None if it doesn't exist
    """
    return category_model.Category.query.filter_by(name=category_name).first()

def add_category(name:str) -> category_model.Category:
    """
    Adds a category to the table
    @returns the new category
    """
    if name_to_category(name) is not None:
        raise ValueError(f"Tried to add an already-existing category, {name}")
    new_cat = category_model.Category(name)
    
    db.session.add(new_cat)
    
    db.session.commit()
    return new_cat
    
    

def delete_category(name:str) -> None:
    """
    delete a category to the table
    """
    cat = name_to_category(name)
    if cat is None:
        print("WARNING: Tried to delete a non-existant category")
        return
    db.session.delete(cat)
    db.session.commit()
