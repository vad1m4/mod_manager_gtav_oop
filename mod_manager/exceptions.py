# empty_name = "Name cannot be empty!"
# error_name = "Name cannot be an error!"
# invalid_link = "Invalid link!"
# error_link = "Link cannot be an error!"
# select = "Select one entry only!"

class EmptyNameError(Exception):
    """Error when the name is empty"""

class InvalidLinkError(Exception):
    """Error when the link doesn't contain "https://" or "http://" """

class SelectError(Exception):
    """Error when the selection is greater than 1"""