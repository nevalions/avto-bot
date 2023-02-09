import logging.config

import string
from dateutil.parser import parse

from log_dir.log_conf import LOGGING_CONFIG
from log_dir.func_auto_log import autolog_info, autolog_warning

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


class Car:
    # car class
    description = ''

    def __init__(
            self, model: str,
            model_name: str,
            mileage: str,
            measures: str,
            date_added: str,
            description: str,
            current_mileage: str
    ):
        autolog_info(f'Car class called')
        self.model = model
        self.model_name = model_name
        self.mileage = mileage
        self.measures = measures
        self.date_added = date_added
        self.description = description
        self.current_mileage = current_mileage

    def __str__(self):
        if self.description == '':
            fstring = (f'{self.model} {self.model_name}, with {self.mileage} {self.measures}, '
                       f'added at {self.date_added}')
        else:
            fstring = (f'{self.model} {self.model_name}, with {self.mileage} {self.measures}, '
                       f'added at {self.date_added}\n'
                       f'Description: {str(self.description)}')

        return fstring

    def __getattr__(self, attr):
        return self[attr]

    @classmethod
    # check is text valid
    def not_empty_str(cls, txt):
        autolog_info(f'Car class check "{txt}"')
        if type(txt) != str:
            raise TypeError('Text must be str type')
        if len(txt.strip()) < 2:
            raise TypeError('Text must be minimum 2 letters')

    @classmethod
    # check is digit
    def is_digit(cls, miles):
        autolog_info(f'Car class check "{miles}"')
        if type(miles) != str or not miles.isdigit():
            # !s
            raise TypeError('Miles must be number')

    @classmethod
    # check is int
    def is_km_or_miles(cls, txt):
        autolog_info(f'Car class check "{txt}"')
        if type(txt) != str:
            raise TypeError('Text must be str type')
        if txt not in ['km', 'miles']:
            raise TypeError('Mesures in km or miles')

    # put is_date check to helper file
    def is_date(string, fuzzy=False):
        """
        Return whether the string can be interpreted as a date.

        :param string: str, string to check for date
        :param fuzzy: bool, ignore unknown tokens in string if True
        """
        try:
            parse(string, fuzzy=fuzzy)
            return True
        except ValueError:
            return False

    @property
    # car model
    def model(self):
        return self._model

    @model.setter
    def model(self, model):
        autolog_info(f'Car model entered "{model}"')
        try:
            self.not_empty_str(model)
            self._model = model.strip()
        except Exception as ex:
            logging.error(ex)
            raise ex

    @property
    # car model_name
    def model_name(self):
        return self._model_name

    @model_name.setter
    def model_name(self, model_name):
        autolog_info(f'Car model_name entered "{model_name}"')
        try:
            self.not_empty_str(model_name)
            self._model_name = model_name.strip()
        except Exception as ex:
            logging.error(ex)
            raise ex

    @property
    # car mileage
    def mileage(self):
        return self._mileage

    @mileage.setter
    def mileage(self, mileage):
        autolog_info(f'Car mileage entered "{mileage}"')
        try:
            self.is_digit(mileage)
            self._mileage = mileage.strip()
        except Exception as ex:
            logging.error(ex)
            raise ex

    @property
    # car measures
    def measures(self):
        return self._measures

    @measures.setter
    def measures(self, measures):
        autolog_info(f'Car measures entered "{measures}"')
        try:
            m = measures.strip().translate(str.maketrans('', '', string.punctuation))
            self.is_km_or_miles(m)
            self._measures = m
        except Exception as ex:
            logging.error(ex)
            raise ex

    @property
    # car date_added
    def date_added(self):
        return self._date_added

    @date_added.setter
    def date_added(self, date_added):
        autolog_info(f'Car date_added entered "{date_added}"')
        try:
            if Car.is_date(date_added.strip()):
                self._date_added = date_added.strip()
            else:
                logging.error(f'Wrong date format {date_added}')
                raise TypeError
        except Exception as ex:
            logging.error(ex)
            raise ex

    @property
    # car description
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        autolog_info(f'Car description entered')
        try:
            self._description = description.strip()
        except Exception as ex:
            logging.error(ex)
            raise ex

    @property
    # car current_mileage
    def current_mileage(self):
        return self._current_mileage

    @current_mileage.setter
    def current_mileage(self, current_mileage):
        autolog_info(f'Car current_mileage entered "{current_mileage}"')
        try:
            self.is_digit(current_mileage)
            self._current_mileage = current_mileage.strip()
        except Exception as ex:
            logging.error(ex)
            raise ex


def main():
    try:
        car1 = Car('Gmc', 'Savana', '300000', 'miles', '22.01.2023', '', '1')
        print(car1)
    except Exception as ex:
        autolog_warning('Not valid car')

    try:
        car = Car('Gmc', 'Savana', '300000', 'miles', '22.01.2023', 'BLABLABLA', '300000')
        print(*vars(car).values())
        car.current_mileage = '2'
        print(*vars(car).values())
        # print(Car.is_date(car.date_added))
        # car.date_added = '12 JUN 2023'
        # print(car)
        # car_diction = vars(car)
        #
        # print({(k[1:]): v for k, v in car_diction.items()})
    except Exception as ex:
        autolog_warning('Not valid car')

    # try:
    #     car2 = Car('asd', 'asd', 'asd', 'miles', '22.01.2022')
    #     print(car2)
    # except Exception as ex:
    #     autolog_warning('Not valid car')


if __name__ == '__main__':
    main()
