"""class for static methods around the Tag table"""

from app import db
from app.models.tag import Tag


def name_to_tag(name: str) -> Tag:
    """
    Returns the tag based on the name, None if it doesn't exist
    """
    return Tag.query.filter_by(name=name).first()

def id_to_tag(tagid: int) -> Tag:
    """
    Returns the tag based on the id, None if it doesn't exist
    """
    return Tag.query.get(tagid)

def add_tag(name:str)->Tag:
    """
    Adds a tag in the database
    @raises ValueError if the tag already exists
    @returns the created tag
    """
    if name_to_tag(name) is not None:
        raise ValueError("Tried to add an existing tag")
    new_tag = Tag(name)
    db.session.add(new_tag)
    db.session.commit()
    return new_tag