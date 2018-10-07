import os
import time
import _thread

from constants import EXIT_CODE_RESTART_IMMEDIATELY


SLEEP_DURATION = 5


def updater_task():
    while True:
        time.sleep(SLEEP_DURATION)
        # TODO: logger
        print('[GIT] Checking for updates')
        output = os.popen('git pull').read()
        if output == 'Already up to date.\n':  # no updates
            continue
        if output.startswith('Updating'):  # update begun
            print('[GIT] Pulled update, restarting to apply changes')
            os.sys.exit(EXIT_CODE_RESTART_IMMEDIATELY)
        
        print('[GIT] Something unexpected happened: ' + output)
        time.sleep(SLEEP_DURATION)  # 2x sleep time
        

def run_updater_thread():
    _thread.start_new_thread(updater_task, ())
