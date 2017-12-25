#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

import wda
import time
from ui.platfrom import Platform


class IOS(Platform):
    client = wda.Client()

    url_list = [
        'cmblife://go?url=YummyGeneralModule&couponType=Daijinquan&title=quan',
        'cmblife://go?url=Mktcinemas'
    ]

    def start(self):
        for url in self.url_list:
            for index in range(0, 100):

                session = self.client.session('com.apple.mobilesafari', ['-u', url])
                try:
                    session(name=u'打开').click_exists()
                    time.sleep(1)
                    # 判斷文件夾是否存在
                    dir = url  # 文件夾名
                    fulDir = '../target/img/' + dir  # 文件夾路徑
                    if not os.path.exists(fulDir):
                        os.mkdir(url)
                    pngName = url + '_' + returnNowStr + '.png'
                    self.client.screenshot('../img/' + dir + '/' + pngName)
                    session.tap(40, 44)

                except Exception as e:
                    print(e)
                finally:
                    # cmb_session.close()
                    session.close()


# 格式化時間戳
def returnNowStr(self):
    time_local = time.localtime(time.time())
    dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    return str(dt)


if __name__ == '__main__':
    IOS().start()
