import pytest

from tenable_io.api.users import UserCreateRequest

from tests.base import BaseTest
from tests.config import TenableIOTestConfig


class TestImpersonation(BaseTest):

    @pytest.mark.vcr()
    def test_impersonation(self, client):
        user_id = client.users_api.create(UserCreateRequest(
            username='test_impersonation@%s' % TenableIOTestConfig.get('users_domain_name'),
            name='test_impersonation',
            password='Sdk!Test1',
            permissions='16',
            type='local',
            email='test_user_email@%s' % TenableIOTestConfig.get('users_domain_name')
        ))
        user = client.users_api.get(user_id)
        impersonating_client = client.impersonate(user.username)
        impersonating_user = impersonating_client.session_api.get()
        assert impersonating_user.username == user.username, u'The current session user should be the impersonated user'
        client.users_api.delete(user_id)
