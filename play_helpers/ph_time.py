import time

from play_helpers.ph_keys import PhKeys
from play_helpers.ph_util import PhUtil


def _get_time():
    """
    :return: Script Time, CPU Time
    """
    script_time = time.time()
    cpu_time = time.process_time()
    return script_time, cpu_time


def _diff_time(start_time, end_time):
    return end_time - start_time


class TimeStates:
    TIMER_INIT = 1
    TIMER_ON = 2
    TIMER_OFF = 3

    name_mapping = {
        TIMER_INIT: 'TIMER_INIT',
        TIMER_ON: 'TIMER_ON',
        TIMER_OFF: 'TIMER_OFF',
    }


class PhTime:
    """

    """

    def __init__(self):
        """

        """
        self.start_time_script = None
        self.start_time_cpu = None
        self.end_time_script = None
        self.end_time_cpu = None
        self.diff_script = None
        self.diff_cpu = None
        self.state = TimeStates.TIMER_INIT

    def start(self):
        """

        :return:
        """
        self.start_time_script, self.start_time_cpu = _get_time()
        self.state = TimeStates.TIMER_ON

    def stop(self):
        """

        :return:
        """
        self.end_time_script, self.end_time_cpu = _get_time()
        self.state = TimeStates.TIMER_OFF

    def get_state(self):
        return TimeStates.name_mapping.get(self.state, PhKeys.UNKNOWN)

    def result(self):
        end_time_script = self.end_time_script
        end_time_cpu = self.end_time_cpu
        if self.state == TimeStates.TIMER_ON:
            end_time_script, end_time_cpu = _get_time()
        self.diff_script = _diff_time(start_time=self.start_time_script, end_time=end_time_script)
        self.diff_cpu = _diff_time(start_time=self.start_time_cpu, end_time=end_time_cpu)

    def print(self):
        """

        :return:
        """
        self.result()
        PhUtil.print_separator(main_text='Time Details')
        print(f'Current Time Stamp: {PhUtil.get_time_stamp(default_format=True)}')
        print(f'Execution Time: {PhUtil.format_time(self.diff_script, time_interval=True)}; '
              f'Milliseconds: {self.diff_script * 1000}')
        print(f'Execution Time CPU: {PhUtil.format_time(self.diff_cpu, time_interval=True)}; '
              f'Milliseconds: {self.diff_cpu * 1000}')
        print(f'Timer State:', self.get_state())
        PhUtil.print_separator()
