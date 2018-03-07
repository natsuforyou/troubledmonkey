#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import wda
import os
import time
from models import Case, TroubledLog, TroubledLogDetail, session_maker
from base import OSType, TroubledLogDetailState


class OS:
    @staticmethod
    def instance(os_type: str):
        if os_type == OSType.IOS:
            os = IOS()
        elif os_type == OSType.ANDROID:
            os = Android()
        else:
            raise RuntimeError('未知的平台：' + os_type)
        os.init()
        return os

    def init(self):
        pass

    def start(self, log: TroubledLog, *args: Case):
        pass

    def init_log_detail(self, log: TroubledLog, case: Case):
        session = session_maker()
        _troubled_log_detail = TroubledLogDetail(log_id=log.ID, case_id=case.ID, case_name=case.NAME,
                                                 state=TroubledLogDetailState.UI_START)
        session.add(_troubled_log_detail)
        session.commit()


class IOS(OS):
    client = None

    def init(self):

        self.client = wda.Client()

    def start(self, log: TroubledLog, *args: Case):
        session = session_maker()
        for case in args:
            count = case.TOTAL_COUNT
            while count > 0:
                super().init_log_detail(log, case)
                _is_crash = False
                _crash_log = ''
                _session = self.client.session('com.apple.mobilesafari', ['-u', case.SCHEMA])
                try:
                    _session(name=u'打开').click_exists()
                    time.sleep(5)
                except Exception as e:
                    _is_crash = True
                    _crash_log = str(e)
                finally:
                    _image = self.client.http.get('screenshot').value
                    session.query(TroubledLogDetail).filter(
                        TroubledLogDetail.LOG_ID == log.ID).filter(
                        TroubledLogDetail.STATE == TroubledLogDetailState.MONKEY_DONE).update(
                        {TroubledLogDetail.IS_CRASH: _is_crash,
                         TroubledLogDetail.CRASH_LOG: _crash_log,
                         TroubledLogDetail.SCREEN_SHOT: _image,
                         TroubledLogDetail.STATE: TroubledLogDetailState.DONE})
                    session.commit()
                    if _session(name=u"确认").click_exists():
                        time.sleep(1)

                    _session.tap(40, 44)
                    _session.close()
                count -= 1


class Android(OS):
    def init(self):
        pass

    def start(self, log: TroubledLog, *args: Case):
        session = session_maker()
        for case in args:
            for _ in range(case.TOTAL_COUNT):
                super().init_log_detail(log, case)
                _is_crash = False
                _crash_log = ''
                try:
                    os.popen(
                        'adb shell am start -n com.cmbchina.ccd.pluto.cmbActivity/.SplashActivity -d ' + case.SCHEMA)
                    #pid = os.getpid()
                    #time.sleep(30)

                    pid1 = pid2 = os.getpid()
                    i = 0
                    #从启动APP开始,如果pid没有改变则等待15秒关闭
                    while pid1 == pid2 and i < 20:
                        time.sleep(1)
                        i += 1
                        pid2 = os.getpid()
                        #print("get pid:" + str(pid2))

                except Exception as e:
                    print(e)
                finally:
                    new_pid = os.getpid()
                    if new_pid != pid1:
                        _is_crash = True
                        _crash_log = ''
                    # 截图
                    _image: str = ''

                    # _troubled_log_detail = session.query(TroubledLogDetail).filter(
                    #     TroubledLogDetail.LOG_ID == log.ID).filter(
                    #     TroubledLogDetail.STATE == TroubledLogDetailState.MONKEY_DONE).one_or_none()
                    #
                    # if _troubled_log_detail is not None:
                    #     _troubled_log_detail.IS_CRASH = _is_crash
                    #     _troubled_log_detail.CRASH_LOG = _crash_log
                    #     _troubled_log_detail.SCREEN_SHOT = _image
                    #     session.update(_troubled_log_detail)
                    session.query(TroubledLogDetail).filter(
                        TroubledLogDetail.LOG_ID == log.ID).filter(
                        TroubledLogDetail.STATE == TroubledLogDetailState.MONKEY_DONE).update(
                        {TroubledLogDetail.IS_CRASH: _is_crash,
                         TroubledLogDetail.CRASH_LOG: _crash_log,
                         TroubledLogDetail.SCREEN_SHOT: _image,
                         TroubledLogDetail.STATE: TroubledLogDetailState.DONE})
                    session.commit()

                    os.system("adb shell am force-stop com.cmbchina.ccd.pluto.cmbActivity")

    @staticmethod
    def get_current_pid():
        output = os.popen(
            'adb shell "ps -ef| grep com.cmbchina.ccd.pluto.cmbActivity$| grep -v grep| awk \"{print \$2}\""')
        return output
