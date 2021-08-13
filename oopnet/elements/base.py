"""
This module contains all the base classes of OOPNET
"""
from traits.api import HasStrictTraits, Str, Either


class NetworkComponent(HasStrictTraits):
    """
    This is OOPNET's base class for all objects having a name (id) in EPANET Input files
    """

    __id = Str
    __comment = Either(None, Str)
    __tag = Either(None, Str)

    @property
    def id(self):
        """
        A unique label used to identify the Network Component. It can consist of a combination of up to 15 numerals or characters. It cannot be the same as the ID for any other node if it is a node, the same counts for links.
        """
        return self.__id

    @id.setter
    def id(self, value):
        self.__id = value

    @property
    def comment(self):
        """
        Property containing a comment on the attribute if it is necessary. The comment is automatically read in from EPANET input files by parsing everything behind a semicolon (;), if a semicolon is not the first character in a line
        """
        return self.__comment

    @comment.setter
    def comment(self, value):
        self.__comment = value

    @property
    def tag(self):
        """
        Associates category labels (tags) with specific nodes and links. An optional text string (with no spaces) used to assign e.g. the node to a category, such as a pressure zone.
        """
        return self.__tag

    @tag.setter
    def tag(self, value):
        self.__tag = value

    def __str__(self):
        return self.id

    def __init__(self, id='', comment=None, tag=None):

        self.id = id
        self.comment = comment
        self.tag = tag
