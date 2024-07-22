import secrets
import string

class UIDObj:
    objects = {}

    def __init__(self):
        self.__uid = self._generate_8_char_alphanumeric_uid()
        self.objects[self.uid] = self

    @classmethod
    def iterate(cls, iterate_type:object):
        for uid, obj in cls.objects.items():
            if type(obj) is not iterate_type:
                continue
            
            yield uid, obj

    @classmethod
    def get(cls, uid:str):
        return cls.objects[uid]
    
    @classmethod
    def remove(cls, uid:str):
        del cls.objects[uid]

    @staticmethod
    def _generate_8_char_alphanumeric_uid():
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(8))

    @property
    def uid(self):
        return self.__uid
