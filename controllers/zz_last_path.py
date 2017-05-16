#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2016/12/12.

from argeweb import auth, add_authorizations
from argeweb import Controller, scaffold, route_menu, Fields, route_with, route
from argeweb.components.pagination import Pagination
from argeweb.components.search import Search
from argeweb.components.csrf import CSRF, csrf_protect


class ZzLastPath(Controller):
    class Meta:
        components = (scaffold.Scaffolding, Pagination, Search, CSRF)

    @route_with(template='/<(zhtw|zhcn|enus|zh_tw|zh_cn|en_us)>/<:(.*)>.html')
    @add_authorizations(auth.check_user)
    def zz_full_path_with_lang(self, lang, path):
        """
        對應到全部的 .html 路徑
        """
        # 取消樣版系統的快取
        # TODO 語系的支援
        self.meta.view.cache = False

        self.context['information'] = self.host_information
        # 先從 Datastore 讀取樣版, 再從 實體檔案 讀取樣版 (template, themes 相關目錄)
        self.meta.view.template_name = [
            u'assets:/themes/%s/%s.html' % (self.theme, path), u'/' + path + u'.html']


    @route_with(template='/<:(.*)>.html')
    @add_authorizations(auth.check_user)
    def zz_full_path(self, path):
        """
        對應到全部的 .html 路徑
        """
        # 取消樣版系統的快取
        self.meta.view.cache = False

        self.context['information'] = self.host_information
        # 先從 Datastore 讀取樣版, 再從 實體檔案 讀取樣版 (template, themes 相關目錄)
        self.meta.view.template_name = [
            u'assets:/themes/%s/%s.html' % (self.theme, path), u'/' + path + u'.html']