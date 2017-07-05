#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/5/27.

from google.appengine.api import namespace_manager
from argeweb import auth, add_authorizations
from argeweb import Controller, scaffold, route_menu, Fields, route_with, route
from argeweb.components.pagination import Pagination
from argeweb.components.search import Search
from argeweb.components.csrf import CSRF, csrf_protect


def check_authorizations(controller, path, config):
    redirect_to = ''
    can_render = False
    if config is None:
        check = '''
        {
            "anonymous": ["*"],
            "user": [],
            "member": []
        }        
        '''
        redirect = '''
        {
            "user": "/login.html"
        }
        '''
    else:
        check = config.authorization_check
        redirect = config.authorization_redirect
    key_all = ''
    key_path = ''
    if check != '':
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
        redirect = config.authorization_redirect
        redirect = controller.util.parse_json(redirect)
        if key_path is not '' and key_path in redirect:
            redirect_to = redirect[key_path]
        if key_all is not '' and key_all in redirect:
            redirect_to = redirect[key_all]
    return can_render, redirect_to


class ZzLastPath(Controller):
    @route_with('/')
    @route_with(template='/<:(.*)>.html')
    @add_authorizations(auth.check_user)
    def zz_full_path(self, path=u'index'):
        """
        對應到全部的 .html 路徑
        """
        path = '/%s.html' % path
        path_ds = 'assets:/themes/%s%s' % (self.theme, path)
        self.context['information'] = self.host_information
        zz_config = self.meta.Model.find_by_name('zz_last_path_config')
        # 樣版系統的快取
        self.meta.view.cache = zz_config.view_cache
        path_app = '/application/%s/templates%s' % (self.theme, path)
        can_render = True
        redirect_to = ''
        if zz_config.use_authorization_check:
            try:
                can_render, redirect_to = check_authorizations(self, path, zz_config)
            except ImportError:
                can_render = False
        if can_render:
            if zz_config.use_real_template_first:
                # 先從 實體檔案 讀取樣版, 再從 Datastore 讀取樣版
                self.meta.view.template_name = [path, path_app, path_ds]
            else:
                # 先從 Datastore 讀取樣版, 再從 實體檔案 讀取樣版
                self.meta.view.template_name = [path_ds, path, path_app]
        else:
            if redirect_to is not '':
                return self.redirect(redirect_to)
            return self.abort(403)

    def admin_list(self):
        return scaffold.list(self)

    def admin_add(self):
        return scaffold.add(self)

    @route
    @route_menu(list_name=u'backend', text=u'路徑映射設定', sort=9961, group=u'系統設定', need_hr=True)
    def admin_config(self):
        record = self.meta.Model.find_by_name('zz_last_path_config')
        if record is None:
            record = self.meta.Model()
            record.name = 'zz_last_path_config'
            record.put()
        return scaffold.edit(self, record.key)

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
        try:
            record = self.meta.Model.find_by_name('zz_last_path_config')
            if record is None:
                record = self.meta.Model()
                record.name = 'zz_last_path_config'
                record.put()
            return 'done'
        except ImportError:
            self.logging.error(u'建設 zz_last_path 設定時，發生錯誤"')
            return 'ImportError'
