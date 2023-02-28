import logging.config

from src.logs.log_conf_main import LOGGING_CONFIG
from src.logs.func_auto_log import autolog_info, autolog_warning

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


class Maintenance:
    def __init__(
            self,
            title: str,
            date: str,
            current_mileage: int,
            description: str = '',
    ):
        autolog_info(f'Car class called')
        self.title = title
        self.date = date
        self.current_mileage = current_mileage
        self.description = description

    def __str__(self):
        if self.description == '':
            fstring = f'{self.title} {self.date}, with {self.current_mileage}'
        else:
            fstring = (f'{self.title} {self.date}, with {self.current_mileage},\n'
                       f'Description: {self.description}')
        return fstring


class Work:
    def __init__(self, title: str, description: str = '', is_regular: bool = False):
        self.title = title
        self.description = description
        self.is_regular = is_regular


class RegularWork(Work):
    def __init__(self, title: str, next_maintenance_after: int, description: str = '', is_regular=True):
        super().__init__(title, description, is_regular)
        self.next_maintenance_after = next_maintenance_after

    def __str__(self):
        if self.description == '':
            fstring = f'{self.title}, regular: {self.is_regular}, next at: {self.next_maintenance_after}'
        else:
            fstring = (f'{self.title} regular: {self.is_regular}, next at: {self.next_maintenance_after}\n'
                       f'Description: {self.description}')
        return fstring


class CustomWork(RegularWork):
    def __init__(self, title: str, description: str = '', is_regular: bool = False, next_maintenance_after: int = 0):
        super().__init__(title, next_maintenance_after, description, is_regular)

    def __str__(self):
        if self.is_regular:
            fstring = (f'{self.title} regular: {self.is_regular}, next at: {self.next_maintenance_after}\n'
                       f'Description: {self.description}')
        else:
            fstring = (f'{self.title}\n'
                       f'Description: {self.description}')
        return fstring


def main():

    maintenance = Maintenance('Maintenance', '22.01.2023', 300000, 'Description')
    work = Work('Brakes', 'benro brakes')
    regular_work = RegularWork('Motor Oil', 123, 'oil: Lukoil')
    custom_work = CustomWork('Clutch', 'dasd', True, 123)
    # print(work)
    # print(vars(work))
    print(custom_work)
    print(regular_work)
    print(regular_work.title)
    print(vars(regular_work))


if __name__ == '__main__':
    main()