#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/5/27.

from argeweb import Fields
from argeweb.core.model import HostInformationModel as Model


class HostInformationModel(Model):
    authorization_check = Fields.CodeJSONProperty(verbose_name=u'驗証檢查', default=u'''
        {
            "anonymous": ["*"],
            "user": [],
            "member": []
        }
    ''')
    authorization_redirect = Fields.CodeJSONProperty(verbose_name=u'驗証重新導向路徑', default=u'''
        {
            "user": "/login.html"
        }
    ''')