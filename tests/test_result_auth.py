# -*- coding: utf8 -*-

from default import Test, assert_not_raises, db
from pybossa.auth import ensure_authorized_to
from nose.tools import assert_raises
from werkzeug.exceptions import Forbidden, Unauthorized
from mock import patch
from test_authorization import mock_current_user
from factories import ProjectFactory, TaskFactory, TaskRunFactory
from pybossa.model.result import Result
from pybossa.repositories import ResultRepository


class TestResultAuthorization(Test):

    mock_anonymous = mock_current_user()
    mock_authenticated = mock_current_user(anonymous=False, admin=False, id=2)
    mock_pro = mock_current_user(anonymous=False, admin=False, id=2, pro=True)
    mock_admin = mock_current_user(anonymous=False, admin=True, id=1)
    mock_owner = mock_current_user(anonymous=False, admin=False, id=1)

    def setUp(self):
        super(TestResultAuthorization, self).setUp()
        self.result_repo = ResultRepository(db)

    def create_result(self, n_answers=1, filter_by=False):
        task = TaskFactory.create(n_answers=n_answers)
        TaskRunFactory.create(task=task)
        if filter_by:
            return self.result_repo.filter_by(project_id=1)
        else:
            return self.result_repo.get_by(project_id=1)

    @patch('pybossa.auth.current_user', new=mock_anonymous)
    def test_anonymous_user_cannot_update_results(self):
        """Test anonymous users cannot update results of a specific project"""
        result = self.create_result()
        assert_raises(Unauthorized, ensure_authorized_to, 'update', result)

    @patch('pybossa.auth.current_user', new=mock_authenticated)
    def test_auth_user_cannot_update_results(self):
        """Test non-owner cannot update results of a specific project"""
        result = self.create_result()
        assert_raises(Forbidden, ensure_authorized_to, 'update', result)

    @patch('pybossa.auth.current_user', new=mock_owner)
    def test_auth_owner_can_update_results(self):
        """Test auth owner can update results of a specific project"""
        result = self.create_result()
        result.info = dict(new='value')
        assert ensure_authorized_to('update', result)
        updated_result = self.result_repo.get_by(id=result.id)
        err_msg = "The result has not been updated"
        assert updated_result.info['new'] == 'value', err_msg

    @patch('pybossa.auth.current_user', new=mock_admin)
    def test_admin_can_update_results(self):
        """Test auth owner can update results of a specific project"""
        result = self.create_result()
        result.info = dict(new='value')
        assert ensure_authorized_to('update', result)
        updated_result = self.result_repo.get_by(id=result.id)
        err_msg = "The result has not been updated"
        assert updated_result.info['new'] == 'value', err_msg
