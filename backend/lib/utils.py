import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def strip_plural(word):
    # Strips common plural forms (simple approach)
    if word.endswith("s"):
        return word[:-1]
    return word


def find_elements_in_array(elements, array):
    # Convert elements and array elements to lowercase for case-insensitive comparison
    elements_lower = [strip_plural(element.lower()) for element in elements]
    array_lower = [strip_plural(item.lower()) for item in array]

    # logging.info("elements:")
    # logging.info(elements_lower)
    # logging.info("Array")
    # logging.info(array_lower)

    # Use lowercase elements for case-insensitive and "plural"-insensitive comparison
    return [element for element in elements_lower if element in array_lower]


def append_without_duplicates(existing_array, elements_to_append):
    # Convert the existing array to a set to remove duplicates
    unique_elements_set = set(existing_array)

    # Iterate through the elements to append
    for element in elements_to_append:
        # Add only if the element is not already in the set
        if element not in unique_elements_set:
            unique_elements_set.add(element)

    # Convert the set back to a list
    updated_array = list(unique_elements_set)

    return updated_array
