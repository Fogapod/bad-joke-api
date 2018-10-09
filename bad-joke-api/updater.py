import asyncio
import os

from constants import EXIT_CODE_RESTART_IMMEDIATELY


async def updater(app):
    # TODO: logger
    print('[GIT] Checking for updates')

    try:
        process = await asyncio.create_subprocess_exec(
            'git', 'pull', stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
    except FileNotFoundError:
        print('[GIT] No git executable found!')
        # TODO: restart?
        raise

    stdout, stderr = await process.communicate()

    if stdout == b'Already up to date.\n':  # no updates
        print('[GIT] No updates found')
        return

    if stdout.startswith(b'Updating'):  # update begun
        print('[GIT] Updated local files, restarting to apply changes')
        # TODO: call app destructor
        os.sys.exit(EXIT_CODE_RESTART_IMMEDIATELY)

    print(f'[GIT] Something unexpected happened: {stdout.decode()}')
    # TODO: git reset --hard
