#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/5/27.

from google.appengine.api import namespace_manager
from argeweb import Controller, scaffold, route
from argeweb import route_with, route_menu
from argeweb.components.pagination import Pagination
from argeweb.components.search import Search


class HostInformation(Controller):
    class Meta:
        components = (scaffold.Scaffolding, Pagination, Search)

    class Scaffold:
        display_in_list = ('authorization_check', 'authorization_redirect')
        excluded_in_form = ('host', 'namespace', 'site_name', 'plugins', 'theme', 'is_lock')

    def admin_list(self):
        namespace_manager.set_namespace('shared')
        return scaffold.list(self)

    def admin_add(self):
        namespace_manager.set_namespace('shared')
        return scaffold.add(self)

    @route
    @route_menu(list_name=u'backend', text=u'頁面路徑驗証設定', sort=9952, group=u'系統設定', need_hr=True)
    def admin_config(self):
        namespace_manager.set_namespace('shared')
        return scaffold.edit(self, self.host_information.key)

    def admin_edit(self, key):
        namespace_manager.set_namespace('shared')
        self.context['item'] = self.params.get_ndb_record(key)
        return scaffold.edit(self, key)

    def admin_view(self, key):
        namespace_manager.set_namespace('shared')
        self.context['item'] = self.params.get_ndb_record(key)
        return scaffold.edit(self, key)

    def admin_delete(self, key):
        namespace_manager.set_namespace('shared')
        return scaffold.delete(self, key)
