#!/usr/bin/env python3

import datetime
import re
import subprocess
import sys

AT = "/usr/bin/at"

def main():
    if len(sys.argv) != 3:
        sys.exit(1)

    target = sys.argv[1]
    wake_time = sys.argv[2]

    # Only allow numeric extension names and HHMM times.
    if not re.fullmatch(r"[0-9]{1,8}", target):
        sys.exit(1)

    if not re.fullmatch(r"[0-9]{4}", wake_time):
        sys.exit(1)

    hour = int(wake_time[:2])
    minute = int(wake_time[2:])

    if hour > 23 or minute > 59:
        sys.exit(1)

    now = datetime.datetime.now().astimezone()
    scheduled = now.replace(
        hour=hour, minute=minute, second=0, microsecond=0
    )

    # If today's requested time has passed, schedule tomorrow.
    if scheduled <= now:
        scheduled += datetime.timedelta(days=1)

    timestamp = scheduled.strftime("%Y%m%d%H%M")

    # When the phone answers, run the wakeup-playback dialplan.
    command = (
        f"/usr/sbin/asterisk -rx "
        f"'channel originate PJSIP/{target} "
        f"extension 263@from-internal'"
    )

    try:
        subprocess.run(
            [AT, "-t", timestamp],
            input=command + "\n",
            text=True,
            check=True,
            timeout=10,
        )
    except (subprocess.SubprocessError, OSError):
        sys.exit(1)

    print(f"Wake-up call scheduled for {scheduled:%Y-%m-%d %H:%M}")
    sys.exit(0)

if __name__ == "__main__":
    main()