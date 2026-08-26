from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


class AuthService:

    password_hasher = PasswordHasher()

    @classmethod
    def hash_password(cls, password: str) -> str:
        return cls.password_hasher.hash(password)


    @classmethod
    def verify_password(
        cls,
        password: str,
        password_hash: str
    ) -> bool:

        try:
            return cls.password_hasher.verify(
                password_hash,
                password
            )

        except VerifyMismatchError:
            return False
