#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
from ui.platfrom import Platform


class Android(Platform):
    url_list = [
        'cmblife://go?url=YummyCouponRush'
    ]

    def start(self):
        for url in self.url_list:
            for index in range(0, 10):
                os.popen('adb shell am start -n com.cmbchina.ccd.pluto.cmbActivity/.SplashActivity -d ' + url)
                pid = self.get_current_pid()
                time.sleep(30)
                pid = self.get_current_pid()
                os.system("adb shell am force-stop com.cmbchina.ccd.pluto.cmbActivity")

    def init(self):
        pass

    def get_current_pid(self):
        output = os.popen(
            'adb shell "ps -ef| grep com.cmbchina.ccd.pluto.cmbActivity$| grep -v grep| awk \"{print \$2}\""')
        return output


if __name__ == '__main__':
    Android().start()
