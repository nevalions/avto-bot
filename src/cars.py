import string
from dateutil.parser import parse


class Car:
    # car class
    def __init__(
            self, model: str,
            model_name: str,
            mileage: str,
            measures: str,
            date_added: str,
            description=''
    ):

        self.model = model
        self.model_name = model_name
        self.mileage = mileage
        self.measures = measures
        self.date_added = date_added
        self.description = description

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
        if type(txt) != str:
            raise TypeError('Text must be str type')
        if len(txt.strip()) < 2:
            raise TypeError('Text must be minimum 2 letters')

    @classmethod
    # check is digit
    def is_digit(cls, miles):
        if type(miles) != str or not miles.isdigit():
            # !s
            raise TypeError('Miles must be number')

    @classmethod
    # check is int
    def is_km_or_miles(cls, txt):
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
        try:
            self.not_empty_str(model)
            self._model = model.strip()
        except Exception as ex:
            print(str(ex))
            print('Car not updated')
            raise ex

    @property
    # car model_name
    def model_name(self):
        return self._model_name

    @model_name.setter
    def model_name(self, model_name):
        try:
            self.not_empty_str(model_name)
            self._model_name = model_name.strip()
        except Exception as ex:
            print(str(ex))
            print('Car not updated')
            raise ex

    @property
    # car mileage
    def mileage(self):
        return self._mileage

    @mileage.setter
    def mileage(self, mileage):
        try:
            self.is_digit(mileage)
            self._mileage = mileage.strip()
        except Exception as ex:
            print(str(ex))
            print('Car not updated')
            raise ex

    @property
    # car measures
    def measures(self):
        return self._measures

    @measures.setter
    def measures(self, measures):
        try:
            m = measures.strip().translate(str.maketrans('', '', string.punctuation))
            self.is_km_or_miles(m)
            self._measures = m
        except Exception as ex:
            print(str(ex))
            print('Car not updated')
            raise ex

    @property
    # car date_added
    def date_added(self):
        return self._date_added

    @date_added.setter
    def date_added(self, date_added):
        try:
            if Car.is_date(date_added.strip()):
                self._date_added = date_added.strip()
            else:
                print('Wrong date format')
                print('Car not updated')
                raise Exception
        except Exception as ex:
            print(str(ex))
            print('Car not updated')
            raise ex

    @property
    # car description
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        try:
            self._description = description.strip()
        except Exception as ex:
            print(str(ex))
            print('Description Error')
            raise ex


def main():
    # try:
    #     Car('Gmc', 'Savana', '300000', 'miles', 'asd')
    # except Exception as ex:
    #     print(ex)

    try:
        car = Car('Gmc', 'Savana', '300000', 'miles', '22.01.2023', 'BLABLABLA')
        print(car)
        print(Car.is_date(car.date_added))
        car.date_added = '12 JUN 2023'
        print(car)
        car_diction = vars(car)

        print({(k[1:]): v for k, v in car_diction.items()})
    except Exception as ex:
        print(ex)

    # try:
    #     car2 = Car('asd', 'asd', 'asd', 'miles', '22.01.202')
    #     print(car2)
    # except Exception as ex:
    #     print(ex)


if __name__ == '__main__':
    main()
