

def line_filter(line):

    if type(line) is bytes:
        line = line.decode()

    try:

        ip = line.split()[0]
        user_agent = line.strip().split('"')[-4]
        url = line.strip().split('"')[1].split()[1]
        date = line.split()[3][1:].split(':')[0]

    except Exception:
        print('[Error in line]', line)
        return

    if 'google' not in user_agent.lower():
        return

    return ip, user_agent, url, date
