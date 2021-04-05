from django.contrib.auth.base_user import BaseUserManager


class MemberManager(BaseUserManager):
    """
    manager needs to be rewritten since User model is customized.
    """
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        * input
        email: char, user's email.
        password: char

        * output in case of no error
        user: a Member object.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        * input
        email: char, user's email.
        password: char

        * output in case of no error
        user: a Member object, not superuser and not staff.
        """
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        * input
        email: char, user's email.
        password: char

        * output in case of no error
        user: a Member object, superuser or staff.
        """
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        return self._create_user(email, password, **extra_fields)
