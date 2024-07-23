from __future__ import annotations
import secrets
import string


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
        self._objects[uid] = new_object

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
