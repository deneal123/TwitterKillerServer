import subprocess
import os
import filecmp
import logging
import shutil
import sysconfig
import setup_common
import sys

errors = 0  # Определение переменной 'errors'
log = logging.getLogger('sd')

# ANSI escape-код для желтого цвета
YELLOW = '\033[93m'
RESET_COLOR = '\033[0m'


def install_req():
    setup_common.check_repo_version()
    setup_common.check_python()

    # Обновление pip, если необходимо
    setup_common.install('--upgrade pip')

    setup_common.install_requirements('requirements.txt', check_no_verify_flag=True)


def main_menu():
    setup_common.clear_screen()
    install_req()


if __name__ == '__main__':
    setup_common.ensure_base_requirements()
    setup_common.setup_logging()
    main_menu()
