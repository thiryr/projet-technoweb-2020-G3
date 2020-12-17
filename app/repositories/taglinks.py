"""class for static methods around the TagLink table"""

from app import db
import app.models.taglink as taglink_model



def add_taglink(tag_id:int, recipe_id:int)->taglink_model.TagLink:
    """
    Adds a tag link to the database
    @returns the created tag link
    """
    new_taglink = taglink_model.TagLink(tag_id,recipe_id)
    db.session.add(new_taglink)
    db.session.commit()
    return new_taglink