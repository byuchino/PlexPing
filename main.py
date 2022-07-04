# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sys
import syslog
import requests
from requests.exceptions import HTTPError, ConnectionError
import config
import notify
from datetime import datetime


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def usage():
    eprint("usage:  usage message here")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    if len(sys.argv) > 2:
        usage()
        sys.exit(-1)

    if len(sys.argv) == 2:
        cfg = config.Config(sys.argv[1])
    else:
        cfg = config.Config()

    if cfg.get_state() == "New":
        syslog.syslog(f'PlexPing started: config file is {cfg.get_filename()}')

    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%M")

    api_url = cfg.get('url')
    status_code = None
    try:
        response = requests.get(api_url)

        # If the response was successful, no Exception will be raised
        response.raise_for_status()
        status_code = response.status_code
    except ConnectionError as connection_err:
        req_detail = f'Connection error occurred: {connection_err}'
        syslog.syslog(syslog.LOG_ERR, req_detail)
    except HTTPError as http_err:
        req_detail = f'HTTP error occurred: {http_err}'  # Python 3.6
        syslog.syslog(syslog.LOG_ERR, req_detail)
    except Exception as err:
        req_detail = f'Other error occurred: {err}'  # Python 3.6
        syslog.syslog(syslog.LOG_ERR, req_detail)
    else:
        req_detail = f'HTTP response status code:  {status_code}'

    if status_code == 200:
        if cfg.set_state('OK') != 'OK':
            s = f'PlexPing Alert for {cfg.get("nickname", "unknown")}'
            m = f'URL {cfg.get("url")} successfully responded\n{req_detail}'
            syslog.syslog(m)
            notify.notify(m, s)
        cfg.update(last_success=ts)
    else:
        if cfg.set_state('DOWN') != 'DOWN':
            s = f'PlexPing Alert for {cfg.get("nickname", "unknown")}'
            m = f'URL {cfg.get("url")} failed to respond\n{req_detail}'
            syslog.syslog(syslog.LOG_WARNING, m)
            notify.notify(m, s)
        cfg.update(last_failure=ts)

    cfg.update(last_run=ts)
    cfg.save()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
