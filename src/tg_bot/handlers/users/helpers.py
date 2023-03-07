import logging.config
from datetime import datetime

from src.logs.log_conf_main import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


class TextMessages(object):
    def __init__(
            self,
            text: str = '',
            date_main: datetime = datetime.utcnow(),
            description_main: str = ''
    ):
        self.text = text
        self.date_main = date_main
        self.description_main = description_main

    def date_to_text(self) -> str:
        return f'📅 <b>Date</b>: {self.date_main.strftime("%d.%m.%Y")}'

    def main_description_txt(self) -> str:
        return f'📄 <b>Description</b>: {self.description_main}'

    def added(self) -> str:
        message = self.text + '✅ Added'
        return message

    def deleted(self) -> str:
        message = self.text + '🗑 Deleted'
        return message


class TextCar(TextMessages):
    def __init__(self, car_model: str = '', car_model_name: str = ''):
        super().__init__()
        self.car_model = car_model
        self.car_model_name = car_model_name

    def car_model_and_model_name(self) -> str:
        return f'🚙 <b>Car</b>: {self.car_model} {self.car_model_name}'


class TextMaintenance(TextCar):
    def __init__(self, car_model: str = '', car_model_name: str = '',
                 maint_title: str = '', date_main: datetime = None,
                 maint_maintenance_mileage: int = None, description_main: str = ''):
        super().__init__(car_model, car_model_name)
        TextMessages.__init__(self, description_main, date_main)

        self.car_model = car_model
        self.car_model_name = car_model_name
        self.maint_title = maint_title
        self.date_main = date_main
        self.maint_maintenance_mileage = maint_maintenance_mileage
        self.description_main = description_main

    def maintenance_title(self) -> str:
        return f'🔧 <b>Maintenance</b>: {self.maint_title}'

    def maintenance_mileage(self) -> str:
        return f'🛣 <b>Maintenance mileage</b>: {self.maint_maintenance_mileage}'

    def maintenance(self) -> str:
        items = [
            self.car_model_and_model_name(),
            self.maintenance_title(),
            self.date_to_text(),
            self.maintenance_mileage(),
            self.main_description_txt()
        ]
        return '\n'.join(items)

    def maintenance_added(self):
        return f"{self.maintenance()}\n{self.added()}"

    def maintenance_deleted(self):
        return f"{self.maintenance_title()}\n{self.deleted()}"
