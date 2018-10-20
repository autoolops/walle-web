# -*- coding: utf-8 -*-
"""

    walle-web

    :copyright: © 2015-2017 walle-web.io
    :created time: 2017-03-25 11:15:01
    :author: wushuiyong@walle-web.io
"""


from flask import request, abort
from flask_login import current_user
from flask_login import login_user, logout_user
from walle.api.api import ApiResource
from walle.form.user import LoginForm
from walle.model.user import UserModel


class PassportAPI(ApiResource):
    action = ['login', 'logout']

    def post(self, method=None):
        """
        user login
        /passport/

        :return:
        """

        if method in self.action:
            self_method = getattr(self, method.lower(), None)
            return self_method()
        else:
            abort(404)

    def login(self):
        """
        user login
        /passport/

        :return:
        """
        form = LoginForm(request.form, csrf_enabled=False)
        if form.validate_on_submit():
            user = UserModel.query.filter_by(email=form.email.data).first()

            if user is not None and user.verify_password(form.password.data):
                login_user(user)
                return self.render_json(data=current_user.to_json())

        return self.render_json(code=-1, data=form.errors)

    def logout(self):
        logout_user()
        return self.render_json()