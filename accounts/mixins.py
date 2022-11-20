# mixins.py
from django.contrib.auth.mixins import UserPassesTestMixin


class OnlyStaffMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        return self.request.user.is_staff