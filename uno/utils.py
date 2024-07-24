from __future__ import annotations
import secrets
import string

class Color:
    # Basic text colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'

    # Light text colors
    LIGHT_BLACK = '\033[90m'
    LIGHT_RED = '\033[91m'
    LIGHT_GREEN = '\033[92m'
    LIGHT_YELLOW = '\033[93m'
    LIGHT_BLUE = '\033[94m'
    LIGHT_MAGENTA = '\033[95m'
    LIGHT_CYAN = '\033[96m'
    LIGHT_WHITE = '\033[97m'

    # Extended 256 text colors
    ORANGE = '\033[38;5;208m'
    PINK = '\033[38;5;213m'
    VIOLET = '\033[38;5;177m'
    LIGHT_GRAY = '\033[38;5;250m'
    DARK_GRAY = '\033[38;5;240m'
    BRIGHT_GREEN = '\033[38;5;10m'
    BRIGHT_PINK = '\033[38;5;13m'
    BRIGHT_CYAN = '\033[38;5;14m'
    BRIGHT_ORANGE = '\033[38;5;214m'

    # Background colors
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'

    # Light background colors
    BG_LIGHT_BLACK = '\033[100m'
    BG_LIGHT_RED = '\033[101m'
    BG_LIGHT_GREEN = '\033[102m'
    BG_LIGHT_YELLOW = '\033[103m'
    BG_LIGHT_BLUE = '\033[104m'
    BG_LIGHT_MAGENTA = '\033[105m'
    BG_LIGHT_CYAN = '\033[106m'
    BG_LIGHT_WHITE = '\033[107m'

    # Styles
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'
    HIDDEN = '\033[8m'
    STRIKETHROUGH = '\033[9m'

    # Reset
    RESET = '\033[0m'

class UIDObject:
    """Base class for objects with unique identifiers."""

    _objects = {}

    def __init__(self):
        self.__uid = self._generate_8_char_alphanumeric_uid()
        self._objects[self.uid] = self

    @classmethod
    def iterate(cls, iterate_type:UIDObject):
        """Yield UID and object for all instances of the given type."""
        for uid, obj in cls._objects.items():
            if isinstance(obj, iterate_type):
                yield uid, obj


    @classmethod
    def register(cls, uid:str, new_object:UIDObject):
        """Register new UID object"""
        cls._objects[uid] = new_object

    @classmethod
    def get(cls, uid:str):
        """Get an object by its UID."""
        if uid in cls._objects:
            return cls._objects[uid]
        else:
            raise ValueError(f"No object found with UID: {uid}")

    @classmethod
    def remove(cls, uid:str):
        """Remove an object by its UID."""
        if uid in cls._objects:
            del cls._objects[uid]
        else:
            raise ValueError(f"No object found with UID: {uid}")

    @staticmethod
    def _generate_8_char_alphanumeric_uid():
        """Generate an 8-character alphanumeric UID."""
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(8))

    @property
    def uid(self):
        """Return the UID of the object."""
        return self.__uid


class ComponentManager:
    """Manager class for handling component registration and global UIDObject pool."""

    _components = {}

    @classmethod
    def register_component(cls, component_id:str, component:object):
        """Register a new component with a given ID."""
        if component_id in cls._components:
            raise KeyError(f"Component with ID '{component_id}' already exists.")
        cls._components[component_id] = component

    @classmethod
    def delete_component(cls, component_id:str):
        """Delete a component by its ID."""
        if component_id not in cls._components:
            raise KeyError(f"No component '{component_id}' to delete, because it does not exist.")
        del cls._components[component_id]

    @classmethod
    def get_component(cls, component_id:str):
        """Get a component by its ID."""
        if component_id not in cls._components:
            raise KeyError(f"Component with ID '{component_id}' not found.")
        return cls._components[component_id]

    @classmethod
    def register_uid_object(cls, uid:str, new_object:UIDObj):
        """Register a new UIDObject"""
        UIDObject.register(uid, new_object)

    @classmethod
    def get_uid_object(cls, uid:str):
        """Get a UIDObject by its UID."""
        return UIDObject.get(uid)

    @classmethod
    def remove_uid_object(cls, uid:str):
        """Remove a UIDObject by its UID."""
        UIDObject.remove(uid)

    @classmethod
    def iterate_uid_objects(cls, iterate_type:UIDObject):
        """Iterate over UIDObjects of a specific type."""
        return UIDObject.iterate(iterate_type)
