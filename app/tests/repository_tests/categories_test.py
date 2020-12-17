"""Proto-test-suite for the category repository"""

from app.repositories.categories import add_category,delete_category,name_to_category


def run_all_tests() -> None:
    """runs the suite
    """
    print("Running tests on category repository")
    all_names_added()
    add_remove_consistancy()
    print("Tests on category repository ended")


def all_names_added() -> None:
    """
    Check that added categories can be retrieved consistantly
    """
    #setup
    names=["123","63!9_","HeLLo?"]
    categories=[]
    #core
    for name in names:
        try:
            categories.append(add_category(name))
        except ValueError:
            delete_category(name)
            categories.append(add_category(name))

            print("test was likely improperly cleaned up last time")
    #test
    for ind,name in enumerate(names):
        assert name_to_category(name) == categories[ind]
    #cleanup
    for name in names:
        delete_category(name)

def add_remove_consistancy() -> None:
    """
    Check that adding and removing a category cancel each other
    """
    #setup
    name="Gkslaj;kj"
    #core
    add_category(name)
    delete_category(name)
    #test
    assert name_to_category(name) is None
    #cleanup