"""class for static methods around the TagLink table"""

from app import db
import app.models.taglink as taglink_model
import app.repositories.tags as tag_rep

from typing import List



def add_taglink(tag_id:int, recipe_id:int)->taglink_model.TagLink:
    """
    Adds a tag link to the database
    @returns the created tag link
    """
    new_taglink = taglink_model.TagLink(tag_id,recipe_id)
    db.session.add(new_taglink)
    db.session.commit()
    return new_taglink

def get_recipe_tags(recipeid: int) -> List[str]:
    """returns list of all tags

    Args:
        recipeid (int): valid recipe id

    Returns:
        List[str]: list of all tags (empty if none)
    """

    taglinks = taglink_model.TagLink.query.filter_by(recipe_id=recipeid).all()
    tags = map(lambda taglink: tag_rep.id_to_tag(taglink.tag_id), taglinks)
    return map(lambda tag: tag.name, tags)