#!/usr/bin/env python
# coding: utf-8

import os
import sys
import hashlib

'''
1，获取需更新的文件列表
2，计算md5值，按规则组成更新行内容
3，将更新内容追加写入到线上更新配置文件
'''

def cal_file_md5(filename):
    '''计算文件md5值'''
    hash_md5 = hashlib.md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
           hash_md5.update(chunk)
    return hash_md5.hexdigest()

class Game(object):
    '''游戏的基类'''
    def __init__(self):
        '''配置（具体配置由子类来实现）'''
        self.workdir = "script_working_dir"
        self.patch = "patch_file_to_update"
        self.url = 'web_server_url'

    def create_update_record(self, version, filename):
        '''创建更新项记录：url version md5 size'''
        return "%s%s %s %s %s\n" % (
                self.url,
                filename,
                version,
                cal_file_md5(filename),
                os.path.getsize(filename)
        )

    def release_patch(self, version, fileList):
        '''发布更新'''
        # cd to working dir first
        os.chdir(self.workdir)
        if not os.path.isfile(self.patch):
            print("update file doesnot exists:%s" % self.patch)
            return
        rowList = []
        for filename in fileList:
            if not os.path.isfile(filename):
                print("patch file doesnot exists:%s" % filename)
                continue
            rowList.append(self.create_update_record(version, filename))
        with open (self.patch, "a") as f:
            for row in rowList:
                # print to debug
                print row.strip()
                f.write(row)
            # print info
            print ("%d patchs added to update-list" % len(rowList))

class XGame(Game):
    '''XGame类'''
    def __init__(self):
        '''配置初始化'''
        self.workdir = "/Users/charlie/code/auto_release_patch/"
        self.patch = "patch.txt"
        self.url = 'http://192.168.1.120/xgame/conf/'

if __name__ == "__main__":
    '''usage: %s version file1 file2 file...'''
    if len(sys.argv) <= 2:
        print("usage: %s version file1 file2 ..." % sys.argv[0])
        sys.exit (-1)
    game = XGame ()
    game.release_patch (sys.argv[1], sys.argv[2:])
