import os
import gzip

from filter import line_filter


base_dir = 'logs2'


all_log_files = os.listdir(base_dir)
all_log_files.sort()
print(all_log_files)


result_file = open('results_log.csv', 'w', encoding='utf-8')
result_file.write('Date\tURL\tGoogleBotUserAgent\n')

#result = dict()


for filename in all_log_files:

    file_path = f'{base_dir}/{filename}'

    if 'error' in file_path:
        continue

    if file_path.endswith('.gz'):
        log_file = gzip.open(file_path)
    else:
        log_file = open(file_path)

    for line in log_file:

        data = line_filter(line)

        if not data:
            continue

        ip, ua, url, date = data

        result_file.write(f'{date}\t{url}\t{ua}\n')

#         if date not in result:
#             result[date] = 1
#         else:
#             result[date] += 1

#     log_file.close()


# for key, val in result.items():
#     result_file.write(f'{key}\t{val}\n')