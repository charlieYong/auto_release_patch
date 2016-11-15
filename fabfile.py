#coding: utf-8

from fabric.api import *
from server_conf import *

'''
热更新自动发布脚本
1, 将文件列表推送到web服务器
2，运行web服务器上的自动发布脚本
'''

def put_release_bin(server):
    '''将自动发布脚本推送到对应的服务器'''
    # 配置服务器
    env.host_string = server.host
    env.password = server.passwd
    # 上传脚本
    fname = "auto_release_patch.py"
    put (fname, "%s%s" % (server.remote_dir, fname), mirror_local_mode=True)

@task
def put_to_android():
    put_release_bin(server_android)

@task
def put_to_ios():
    put_release_bin(server_ios)

@task
def put_to_itest():
    put_release_bin(server_itest)

@task
def put_to_tw_android():
    put_release_bin(tw_server_android)

@task
def put_to_tw_ios():
    put_release_bin(tw_server_ios)

def release_patch(server, version, files):
    '''执行发布操作'''
    # 配置服务器
    env.host_string = server.host
    env.password = server.passwd
    # 解析要更新的文件列表
    fileList = files.split (' ')
    # 上传到服务器
    for filename in fileList:
        #print filename
        if put (filename, "%s%s" % (server.remote_dir, filename)).failed:
            print ("update file failed:" + filename)
            # 跳出发布流程
            return
    # 执行自动发布脚本
    print run("%s %s %s" % (server.release_bin, version, files))

@task(alias='120')
def release_patch_to_120(version, files):
    '''发布到120服务器'''
    release_patch (server_120, version, files)

@task(alias='android')
def release_patch_to_android(version, files):
    '''发布到android线上服务器'''
    release_patch (server_android, version, files)

@task(alias='ios')
def release_patch_to_ios(version, files):
    '''发布到ios线上服务器'''
    release_patch (server_ios, version, files)

@task(alias='itest')
def release_patch_to_itest(version, files):
    '''发布到ios测试服务器'''
    release_patch (server_itest, version, files)

@task(alias='tw_ios')
def release_patch_to_tw_ios(version, files):
    '''发布到台湾ios服务器'''
    release_patch (tw_server_ios, version, files)

@task(alias='tw_android')
def release_patch_to_tw_android(version, files):
    '''发布到台湾android服务器'''
    release_patch (tw_server_android, version, files)
