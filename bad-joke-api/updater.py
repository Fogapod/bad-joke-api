import asyncio
import os
import _thread

from constants import EXIT_CODE_RESTART_IMMEDIATELY


SLEEP_DURATION = 15


async def updater_task(app):
    try:
        while True:
            await asyncio.sleep(SLEEP_DURATION)
            # TODO: logger
            print('[GIT] Checking for updates')

            try:
                process = await asyncio.create_subprocess_exec(
                    'git', 'pull', stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
            except FileNotFoundError:
                print('[GIT] No git executable found!')
                print('[GIT] Stopping updater')
                break

            stdout, stderr = await process.communicate()

            if stdout == b'Already up to date.\n':  # no updates
                continue
            if stdout.startswith(b'Updating'):  # update begun
                print('[GIT] Updated local files, restarting to apply changes')
                # TODO: call app destructor
                os.sys.exit(EXIT_CODE_RESTART_IMMEDIATELY)

            print(f'[GIT] Something unexpected happened: {stdout.decode()}')
            asyncio.sleep(SLEEP_DURATION)  # 2x sleep time
    except (asyncio.CancelledError, RuntimeError):
        pass
        

def run_updater_thread():
    _thread.start_new_thread(updater_task, ())
