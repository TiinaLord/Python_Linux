import os
import subprocess
import collections
from datetime import datetime


class SystemStatusParser:

    def __init__(self):
        self.users = collections.defaultdict(list)
        self.process_count = 0
        self.total_memory = 0.0
        self.total_cpu = 0.0
        self.most_memory_process = None
        self.most_cpu_process = None

    def check_system_status(self):
        ps_aux_output = subprocess.check_output(['ps', 'aux']).decode().splitlines()[1:]
        for line in ps_aux_output:
            values = line.split()
            user = values[0]
            self.users[user].append(values)

        self.process_count = sum(len(procs) for procs in self.users.values())

        # Calculate memory and CPU usage efficiently
        self.total_memory = sum(float(value[3]) for values in self.users.values() for value in values)
        self.total_cpu = sum(float(value[2]) for values in self.users.values() for value in values)

        # Find processes with highest memory and CPU usage
        self.most_memory_process = max(self.users.values(), key=lambda procs: max(float(value[3]) for value in procs))[0]
        self.most_cpu_process = max(self.users.values(), key=lambda procs: max(float(value[2]) for value in procs))[0]

    def print_report(self):
        report = f"""
Отчёт о состоянии системы:
Пользователи системы: {', '.join(self.users.keys())}
Процессов запущено: {self.process_count}

Пользовательских процессов:{chr(10)}{''.join(f"{user}: {len(procs)}{chr(10)}" for user, procs in self.users.items())} 

Всего памяти используется: {round(self.total_memory, 1)} mb
Всего CPU используется: {round(self.total_cpu, 1)} %
Больше всего памяти использует: {self.most_memory_process[10][:20]}
Больше всего CPU использует: {self.most_cpu_process[10][:20]}
"""
        print(report)

        with open(datetime.now().strftime('%d-%m-%Y-%H-%M-scan.txt'), 'w') as file:
            file.write(report)


if __name__ == "__main__":
    parser = SystemStatusParser()
    parser.check_system_status()
    parser.print_report()
