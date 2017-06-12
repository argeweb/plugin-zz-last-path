#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/5/27.


plugins_helper = {
    'title': u'Html 路徑映射',
    'desc': u"根據 routing 的規則，此模組的路徑將會在最後被載入",
    'controllers': {
        'zz_last_path': {
            'group': u'路徑映射',
            'actions': [
                {'action': 'config', 'name': u'路徑映射設定'},
                {'action': 'plugins_check', 'name': u'啟用停用模組'},
            ]
        },
    },
    'install_uri': 'zz_last_path:zz_last_path:after_install'
}
