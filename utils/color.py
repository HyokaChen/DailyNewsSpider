#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @File       : color.py
 @Time       : 2019-04-16 21:43
 @Author     : Empty Chan
 @Contact    : chen19941018@gmail.com
 @Description:
 @License    : (C) Copyright 2016-2017, iFuture Corporation Limited.
"""
from colorama import init, Fore, Back, Style

init(autoreset=False)


class Colored(object):
    #  前景色:红色  背景色:默认
    @staticmethod
    def red(s):
        return Fore.LIGHTRED_EX + s + Fore.RESET

    #  前景色:绿色  背景色:默认
    @staticmethod
    def green(s):
        return Fore.LIGHTGREEN_EX + s + Fore.RESET

    @staticmethod
    def yellow(s):
        return Fore.LIGHTYELLOW_EX + s + Fore.RESET

    @staticmethod
    def white(s):
        return Fore.LIGHTWHITE_EX + s + Fore.RESET

    @staticmethod
    def blue(s):
        return Fore.LIGHTBLUE_EX + s + Fore.RESET