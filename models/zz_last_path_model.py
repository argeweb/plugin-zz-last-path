#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/5/27.

from argeweb import Fields
from argeweb import BasicModel


class ZzLastPathModel(BasicModel):
    name = Fields.HiddenProperty(verbose_name=u'識別名稱', default=u'zz_last_path_config')
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
