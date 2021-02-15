import re

def line_filter(line):

    if type(line) is bytes:
        line = line.decode()

    try:

        date = line.split()[0] + ' ' + line.split()[1]
       # user_agent = line.strip().split('"')[-4]
        status_code = re.findall(r'\(\d\d?\d?\:.*\)', line)[0]
        status_code = str(status_code).strip('(')
        status_code = str(status_code).strip(')')
        url = line.strip().split('"')[1]
        url = url.lstrip('GET ')
        url = url.lstrip('POST ')
        url = url.rstrip(' HTTP/1.1')

        #url = line.strip().split('"')[1].split()[1]

        # ip = line.split()[0]
        # user_agent = line.strip().split('"')[-4]
        # url = line.strip().split('"')[1].split()[1]
        # date = line.split()[3][1:].split(':')[0]

    except Exception:
        print('[Error in line]', line)
        return

    # if 'google' not in user_agent.lower():
    #     return

    return date, status_code, url