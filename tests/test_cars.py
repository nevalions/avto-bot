import os
import sys

import pytest
sys.path.append(os.path.join(os.getcwd(), '..'))

from src.classes.cars import Car

car1 = Car('Gmc', 'Savana', '300000', 'miles', '22.01.2023', 'BlaBlaBla', '300000')


def main():
    test_cars_ok()
    test_update_fields()
    test_strip_ok()
    test_remove_punct_ok()
    test_cars_exceptions()


def test_cars_ok():
    assert car1.model == 'Gmc'
    assert car1.model_name == 'Savana'
    assert car1.mileage == '300000'
    assert car1.measures == 'miles'
    assert car1.date_added == '22.01.2023'
    assert car1.current_mileage == '300000'
    assert car1.description == 'BlaBlaBla'


def test_update_fields():
    car1.model = 'Chevrolet'
    car1.model_name = 'Astro'
    car1.mileage = '10000'
    car1.measures = 'km'
    car1.date_added = '01.01.2022'
    car1.description = 'AAAaaaAAA'

    assert car1.model == 'Chevrolet'
    assert car1.model_name == 'Astro'
    assert car1.mileage == '10000'
    assert car1.measures == 'km'
    assert car1.date_added == '01.01.2022'
    assert car1.description == 'AAAaaaAAA'


def test_strip_ok():
    car1.model = '    Chevrolet   '
    assert car1.model == 'Chevrolet'

    car1.model_name = '    Astro     '
    assert car1.model_name == 'Astro'

    car1.model_name = 'Lada Racing '
    assert car1.model_name == 'Lada Racing'

    car1.description = '       AAAaaaAAA         '
    assert car1.description == 'AAAaaaAAA'


def test_remove_punct_ok():
    car1.measures = 'km.'
    assert car1.measures == 'km'

    car1.measures = '!/.km.,:;&?'
    assert car1.measures == 'km'


def test_cars_exceptions():
    with pytest.raises(Exception):
        car1.model = 'G'
    with pytest.raises(Exception):
        car1.model = ''
    with pytest.raises(Exception):
        car1.model = '         '
    with pytest.raises(Exception):
        car1.model_name = '1'
    with pytest.raises(Exception):
        car1.model_name = ''
    with pytest.raises(Exception):
        car1.model_name = '        '
    with pytest.raises(Exception):
        car1.mileage = 'asd'
    with pytest.raises(Exception):
        car1.mileage = '123asd'
    with pytest.raises(Exception):
        car1.mileage = '123.4'
    with pytest.raises(Exception):
        car1.measures = 'kilometers'
    with pytest.raises(Exception):
        car1.measures = 'k'
    with pytest.raises(Exception):
        car1.measures = 'm'
    with pytest.raises(Exception):
        car1.date_added = 'as.12.as'

    with pytest.raises(Exception):
        Car('Gm', 'Savana', '300000', 'miles', 'asd', 'BlaBlaBla', '300000')
    with pytest.raises(Exception):
        Car('Gmc', '', '300000', 'miles', '22.01.2023', 'BlaBlaBla', '300000')
    with pytest.raises(Exception):
        Car('Gmc', 'Savana', '300000a', 'miles', '22.01.2023', 'BlaBlaBla', '300000')
    with pytest.raises(Exception):
        Car('Gmc', 'Savana', '300000', 'kilometers', '22.01.2023', 'BlaBlaBla', '300000')


if __name__ == '__main__':
    main()
