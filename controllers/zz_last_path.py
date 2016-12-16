#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2016/12/12.

from argeweb import Controller, route_menu, route_with, route


class ZzLastPath(Controller):
    @route_with(template="/<:(.*)>.html")
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