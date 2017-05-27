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
from ..models.host_information_model import HostInformationModel


def check_authorizations(controller, path, host_information):
    redirect_to = ''
    can_render = False
    check = host_information.authorization_check
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
        redirect = host_information.authorization_redirect
        redirect = controller.util.parse_json(redirect)
        if key_path is not '' and key_path in redirect:
            redirect_to = redirect[key_path]
        if key_all is not '' and key_all in redirect:
            redirect_to = redirect[key_all]
    return can_render, redirect_to


def get_information(server_name, namespace, **kwargs):
    namespace_manager.set_namespace('shared')
    info = HostInformationModel.get_by_host(server_name)
    namespace_manager.set_namespace(namespace)
    return info


class ZzLastPath(Controller):
    class Meta:
        components = (scaffold.Scaffolding, Pagination, Search, CSRF)

    @route_with('/')
    @route_with('/index.html')
    @add_authorizations(auth.check_user)
    def index(self):
        # 取消樣版系統的快取
        self.meta.view.cache = False
        self.context['information'] = self.host_information
        try:
            can_render, redirect_to = check_authorizations(self, '/index.html', get_information(self.server_name, self.namespace))
        except ImportError:
            can_render = True
            redirect_to = ''
        if can_render:
            # 先從 Datastore 讀取樣版, 再從 實體檔案 讀取樣版 (template, themes 相關目錄)
            self.meta.view.template_name = [u'assets:/themes/%s/index.html' % self.theme, u'/index.html']
            if self.theme == 'default':
                # 若有語系參數的話 ( hl )
                index_path = u'%s.html' % self.params.get_string('hl', u'index').lower().replace('-', '')
                self.meta.view.template_name = [u'assets:/themes/%s/%s' % (self.theme, index_path), index_path]
        else:
            if redirect_to is not '':
                return self.redirect(redirect_to)
            return self.abort(403)

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
        path = '/%s.html' % path
        # 取消樣版系統的快取
        self.meta.view.cache = False

        self.context['information'] = self.host_information
        can_render, redirect_to = check_authorizations(self, path, get_information(self.server_name, self.namespace))
        if can_render:
            # 先從 Datastore 讀取樣版, 再從 實體檔案 讀取樣版 (template, themes 相關目錄)
            self.meta.view.template_name = [
                u'assets:/themes/%s%s' % (self.theme, path), path]
        else:
            if redirect_to is not '':
                return self.redirect(redirect_to)
            return self.abort(403)

