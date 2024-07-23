import secrets
import string


class UIDObj:
    objects = {}
    stacks = {}

    def __init__(self):
        self.__uid = self._generate_8_char_alphanumeric_uid()
        self.objects[self.uid] = self

    @classmethod
    def iterate(cls, iterate_type: object):
        for uid, obj in cls.objects.items():
            if isinstance(obj, iterate_type):
                yield uid, obj

    @classmethod
    def get(cls, uid: str):
        if uid in cls.objects:
            return cls.objects[uid]
        else:
            raise ValueError(f"No object found with UID: {uid}")

    @classmethod
    def remove(cls, uid: str):
        if uid in cls.objects:
            del cls.objects[uid]
        else:
            raise ValueError(f"No object found with UID: {uid}")

    @staticmethod
    def _generate_8_char_alphanumeric_uid():
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(8))

    @property
    def uid(self):
        return self.__uid
