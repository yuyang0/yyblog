#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Time-stamp: <2013-07-22 17:58:41 Monday by Yu Yang>

"""
some utilities
"""
import os

def get_pardir(apath):
    """
    get parent directory of a path
    Arguments:
    - `apath`:the path you want to get parent directory
    """
    pdir = os.path.abspath(os.path.join(apath, os.pardir))
    return pdir

def get_project_root():
    """
    get project root directory
    """
    cur_dir = os.path.realpath(os.path.dirname(__file__))
    root = get_pardir(cur_dir)
    return root

if __name__ == '__main__':
    print get_project_root()
