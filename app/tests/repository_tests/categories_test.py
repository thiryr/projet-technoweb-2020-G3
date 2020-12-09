"""Proto-test-suite for the category repository"""

from app.repositories.categories import CategoryRepository


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
            categories.append(CategoryRepository.add_category(name))
        except ValueError:
            CategoryRepository.delete_category(name)
            categories.append(CategoryRepository.add_category(name))

            print("test was likely improperly cleaned up last time")
    #test
    for ind,name in enumerate(names):
        assert CategoryRepository.name_to_category(name) == categories[ind]
    #cleanup
    for name in names:
        CategoryRepository.delete_category(name)

def add_remove_consistancy() -> None:
    """
    Check that adding and removing a category cancel each other
    """
    #setup
    name="Gkslaj;kj"
    #core
    CategoryRepository.add_category(name)
    CategoryRepository.delete_category(name)
    #test
    assert CategoryRepository.name_to_category(name) is None
    #cleanup