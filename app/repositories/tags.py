"""class for static methods around the Tag table"""

from app import db
import app.models.tag as tag_model


def name_to_tag(name: str) -> tag_model.Tag:
    """
    Returns the tag based on the name, None if it doesn't exist
    """
    return tag_model.Tag.query.filter_by(name=name).first()

def id_to_tag(tagid: int) -> tag_model.Tag:
    """
    Returns the tag based on the id, None if it doesn't exist
    """
    return tag_model.Tag.query.get(tagid)

def add_tag(name:str)->tag_model.Tag:
    """
    Adds a tag in the database
    @raises ValueError if the tag already exists
    @returns the created tag
    """
    if name_to_tag(name) is not None:
        raise ValueError("Tried to add an existing tag")
    new_tag = tag_model.Tag(name)
    db.session.add(new_tag)
    db.session.commit()
    return new_tag