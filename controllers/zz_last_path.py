#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/5/27.

from datetime import date, timedelta
from argeweb import auth, add_authorizations
from argeweb import Controller, scaffold, route_menu, route_with, route
from argeweb.components.pagination import Pagination
from argeweb.components.search import Search


class Config(object):
    """
    預先加載設定值
    """
    def __init__(self, controller):
        self.controller = controller
        self.controller.events.before_startup += self._on_before_startup

    def _on_before_startup(self, controller, *args, **kwargs):
        controller.context['zz_config'] = self.controller.meta.Model.get_by_name_async('zz_last_path_config')


def check_authorizations(controller, path, check=None, redirect=None):
    key_all = ''
    key_path = ''
    redirect_to = ''
    can_render = False
    if check is None:
        check = '''
        {
            "anonymous": ["*"],
            "user": [],
            "member": []
        }        
        '''
    if redirect is None:
        redirect = '''
        {
            "user": "/login.html"
        }
        '''
    check = controller.util.parse_json(check)
    for k, v in check.items():
        if '*' in v and key_all is '':
            key_all = k
        if path in v and key_path is '':
            key_path = k
    if key_path in ['', 'anonymous'] and 'anonymous' in [key_path, key_all]:
        can_render = True
    else:
        if controller.application_user is not None:
            can_render = key_path is not '' and controller.application_user.has_role(key_path)
            if can_render is False:
                can_render = key_all is not '' and controller.application_user.has_role(key_all)
    if can_render is False:
        redirect = controller.util.parse_json(redirect)
        if key_path is not '' and key_path in redirect:
            redirect_to = redirect[key_path]
        if key_all is not '' and key_all in redirect:
            redirect_to = redirect[key_all]
    if redirect_to.find('?') > 0:
        redirect_to = redirect_to + '&from=' + path
    else:
        redirect_to = redirect_to + '?from=' + path
    return can_render, redirect_to


class ZzLastPath(Controller):
    class Meta:
        components = (scaffold.Scaffolding, Pagination, Search, Config)

    @route_with('/test')
    def test(self):
        demo = {"CheckCode": "879D8063294B0B1CAE969417C50EBE0929FFA07468FDC30380B3F819ABBA73E0",
                "MerchantID": "3653940",
                "MerchantOrderNo": "20171019_6753", "InvoiceNumber": "FM00000101", "TotalAmt": 360,
                "InvoiceTransNo": "17102008374131677", "RandomNum": "3965", "CreateTime": "2017-10-20 08:37:41",
                "BarCode": "10610FM000001013965",
                "QRcodeL": "FM000001011061020396500000157000001680000000034960999Y78Q\/scA0d5p\/F+kxxQ9lA==:**********:1:1:0:",
                "QRcodeR": "**test (\u6e2c\u8a66\u7522\u54c1:1:300"}
        s = []
        for key, val in demo.items():
            s.append('return_' + self.util.underscore(key))
        return self.json(s)

    @route_with('/')
    @route_with(template='/<path:(.*)>.html')
    def zz_full_path(self, path=u'index'):
        """
        對應到全部的 .html 路徑
        """
        try:
            if self.host_information.space_expiration_date < date.today() + timedelta(days=1):
                return self.abort(404)
        except:
            return self.abort(404)
        zz_config = self.context['zz_config']
        if zz_config is None:
            zz_config = self.meta.Model.get_or_create_by_name('zz_last_path_config')
        else:
            zz_config = zz_config.get_result()
        self.context['information'] = self.host_information
        self.context['path'] = path
        can_render = True
        redirect_to = ''
        if zz_config and zz_config.use_authorization_check:
            try:
                can_render, redirect_to = check_authorizations(
                    self, '/%s.html' % path,
                    zz_config.authorization_check,
                    zz_config.authorization_redirect
                )
            except ImportError:
                can_render = False
        if can_render:
            return self.meta.view.set_template_names_from_path(path)
        if redirect_to is not '':
            return self.redirect(redirect_to)
        return self.abort(403)

    def admin_list(self):
        return self.redirect(self.uri('admin:zz_last_path:zz_last_path:config'))

    def admin_add(self):
        return self.redirect(self.uri('admin:zz_last_path:zz_last_path:config'))

    @route
    @route_menu(list_name=u'super_user', text=u'路徑映射設定', sort=3, group=u'系統設定')
    def admin_config(self):
        config_record = self.meta.Model.get_config()
        return scaffold.edit(self, config_record.key)

    def admin_edit(self, key):
        self.context['item'] = self.params.get_ndb_record(key)
        return scaffold.edit(self, key)

    def admin_view(self, key):
        self.context['item'] = self.params.get_ndb_record(key)
        return scaffold.edit(self, key)

    def admin_delete(self, key):
        return scaffold.delete(self, key)

    @route
    def taskqueue_after_install(self):
        config_record = self.meta.Model.get_config()
        return 'done'
