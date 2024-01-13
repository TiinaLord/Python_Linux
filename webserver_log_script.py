import json
import os
import re
from collections import defaultdict
from pprint import pprint


class ParseLogsException(BaseException):
    def __init__(self, path: str):
        self.path = path

    def __str__(self):
        return f'ParseLogsException Error: Проверьте путь или креды {self.path}.'


def parse_logs(log_file):

    methods = re.compile(r'(POST|GET|PUT|DELETE|HEAD|OPTIONS)\b')
    host_remote = re.compile(r'^(?:\d{1,3}\.){3}\d{1,3}')
    duration_period = re.compile(r'\s\d+\n')
    date_of_request = re.compile(r'\[[\w\s/:+-]*\]')
    url_part = re.compile(r'\"https?://(\S*)\"')

    with open(log_file, 'r') as file:
        requests_number = 0
        methods_dict = defaultdict(int)
        summary_requests = []
        dict_ip_requests = defaultdict(lambda: {"requests_number": 0})

        for line in file:
            method = methods.search(line).group(0)
            remote_host = host_remote.search(line).group(0)
            request_duration = int(duration_period.search(line).group(0).replace('\n', ''))
            date = date_of_request.search(line).group(0)
            is_url = url_part.search(line)
            url = is_url.group(0)[1:-1] if is_url else '-'

            request_info = {
                'method': method,
                'ip': remote_host,
                'duration': request_duration,
                'date': date,
                'url': url,
            }
            summary_requests.append(request_info)

            requests_number += 1
            methods_dict[method] += 1
            dict_ip_requests[request_info['ip']]["requests_number"] += 1

        top_ips = dict(sorted(dict_ip_requests.items(), key=lambda x: x[1]["requests_number"], reverse=True)[0:3])
        top_durations = sorted(summary_requests, key=lambda x: x['duration'], reverse=True)[0:3]

        result = {
            'total_requests': requests_number,
            'total_methods': dict(methods_dict),
            'top_ips': {k: v['requests_number'] for k, v in top_ips.items()},
            'top_longest_requests': top_durations}

        with open(f'{log_file}.json', 'w') as json_file:
            json.dump(result, json_file, indent=4)

        pprint(result)


def main():
    log_file_path = "/home/user/PycharmProjects/Python_Linux/Python_Linux/log_file.log"

    try:
        for log_file in _get_log_files(log_file_path):
            parse_logs(log_file)
    except ParseLogsException as e:
        print(e)


def _get_log_files(path):
    if os.path.isfile(path):
        yield path
    elif os.path.isdir(path):
        for file in os.listdir(path):
            if file.endswith(".log"):
                yield os.path.join(path, file)
    else:
        raise ParseLogsException(path)


if __name__ == '__main__':
    main()
