"""class for static methods around the TagLink table"""

from app import db
from app.models.taglink import TagLink



def add_taglink(tag_id:int, recipe_id:int)->TagLink:
    """
    Adds a tag link to the database
    @returns the created tag link
    """
    new_taglink = TagLink(tag_id,recipe_id)
    db.session.add(new_taglink)
    db.session.commit()
    return new_taglink