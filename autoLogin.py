# -*- coding: utf-8 -*-
# @Time    : 2021/12/06 13:20
# @Author  : spdeng
import ddddocr
import time  # 代码运行停顿
import getpass
from selenium import webdriver  # 用于打开网站
from PIL import Image

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

# 记录账号密码
username = "295338748@qq.com"
password = "Dengsp123456"

class VerificationCode:
    def __init__(self):
        self.driver = webdriver.Chrome(options=options)
        # self.driver = webdriver.Chrome('D:\Python3.9.7\chromedriver.exe')
        self.find_element = self.driver.find_element_by_id
        # 启动浏览器
        self.driver.get("https://xxxx.com") # 打开登陆页面
    
    def get_pictures(self):
        print("==================")
        time.sleep(1)
        # 截取验证码图片
        self.find_element("email").send_keys(username)
        self.find_element("password").send_keys(password)
        self.driver.save_screenshot('./pictures.png') # 全屏截图
        page_snap_obj = Image.open('./pictures.png')
        img = self.find_element('captchaCode') # 验证码元素位置
        time.sleep(1)
        location = img.location
        size = img.size # 获取验证码的大小参数
        left = location['x']
        top = location['y']
        right = left + size['width']
        bottom = top + size['height']
        image_obj = page_snap_obj.crop((left, top, right, bottom)) # 按照验证码的长宽，切割验证码
        image_obj.save("./capimg.png")
        # 读取验证码
        ocr = ddddocr.DdddOcr()
        with open('./capimg.png', 'rb') as f:
            img_bytes = f.read()
        res = ocr.classification(img_bytes)
        print("得到验证码："+res)
        # image_obj.show() # 打开切割后的完整验证码
        # self.driver.close() # 处理完验证码后关闭浏览器
        return res

    def login(self):
        code = self.get_pictures()
        self.find_element("captcha").send_keys(code)
        self.find_element("loginForm").click()
        print("登录成功！")

# 输入验证码并登录
if __name__ == '__main__':
  print("获取验证码开始")
  a = VerificationCode()
  a.login()


# time.sleep(2)
# driver.quit()
