# mixins.py
from django.contrib.auth.mixins import UserPassesTestMixin


class OnlyStaffMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        return self.request.user.is_staff

class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['pk'] or user.is_superuser