# coding:utf-8
__author__ = 'xxj'


# coding: utf-8
# 测试"Selenium + Chrome"使用带用户名密码认证的代理

import os
import re
import time
import zipfile
from selenium import webdriver

# Chrome代理模板插件(https://github.com/RobinDev/Selenium-Chrome-HTTP-Private-Proxy)目录
CHROME_PROXY_HELPER_DIR = 'F:\py_project\lol\huakuai\ip_rtbasia\Chrome-proxy-helper'
# 存储自定义Chrome代理扩展文件的目录（存储zip文件）
CUSTOM_CHROME_PROXY_EXTENSIONS_DIR = 'F:\py_project\lol\huakuai\ip_rtbasia\chrome-proxy-extensions'


def get_chrome_proxy_extension(proxy):
    """获取一个Chrome代理扩展,里面配置有指定的代理(带用户名密码认证)
    proxy - 指定的代理,格式: username:password@ip:port
    """
    m = re.compile('([^:]+):([^\@]+)\@([\d\.]+):(\d+)').search(proxy)
    if m:
        # 提取代理的各项参数
        username = m.groups()[0]    # 用户名
        password = m.groups()[1]    # 密码
        ip = m.groups()[2]    # ip
        port = m.groups()[3]    # port
        print username, password, ip, port
        # 创建一个定制Chrome代理扩展目录(用于存放zip文件)
        if not os.path.exists(CUSTOM_CHROME_PROXY_EXTENSIONS_DIR):
            os.mkdir(CUSTOM_CHROME_PROXY_EXTENSIONS_DIR)
        else:
            print '存放zip文件的目录已经创建存在'    # set
        extension_file_path = os.path.join(CUSTOM_CHROME_PROXY_EXTENSIONS_DIR, '{}.zip'.format(proxy.replace(':', '_')))
        if not os.path.exists(extension_file_path):
            # 扩展文件不存在，创建
            zf = zipfile.ZipFile(extension_file_path, mode='w')
            zf.write(os.path.join(CHROME_PROXY_HELPER_DIR, 'manifest.json'), 'manifest.json')    # zf对象的write方法参数一是manifest.json文件路径(数据来源)；参数二：是在zip文件中生成的文件名
            # # 替换模板中的代理参数
            background_content = open(os.path.join(CHROME_PROXY_HELPER_DIR, 'background.js')).read()
            background_content = background_content.replace('mimvp_proxy_host', ip)
            background_content = background_content.replace('mimvp_proxy_port', port)
            background_content = background_content.replace('mimvp_username', username)
            background_content = background_content.replace('mimvp_password', password)
            print 'background_content：', background_content
            zf.writestr('background.js', background_content)    # zf对象的writestr方法参数一是在zip文件中生成的文件名；参数二是字符串（来源字符串）
            zf.close()
        else:
            print '该代理[{proxy}]存在'.format(proxy=proxy)
        return extension_file_path
    else:
        raise Exception('Invalid proxy format. Should be username:password@ip:port')


if __name__ == '__main__':
    # 测试
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    # 添加一个自定义的代理插件（配置特定的代理，含用户名密码认证）
    xxx = '8c84700fa7d2:kgvavaeile@117.57.90.235:17514'
    options.add_extension(get_chrome_proxy_extension(proxy=xxx))    # 添加扩展
    options.add_argument('no-sandbox')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(
        executable_path=r'C:\Users\xj.xu\Downloads\chromedriver_win32\chromedriver.exe',
        chrome_options=options)
    # 访问一个IP回显网站，查看代理配置是否生效了
    url = 'http://httpbin.org/ip'
    print 'url：', url
    # driver.set_page_load_timeout(2)
    driver.get(url)    # 总是会卡在这里
    print 'url1：', url
    time.sleep(5)
    driver.quit()



