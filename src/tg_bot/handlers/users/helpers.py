import logging.config
from datetime import datetime

from src.logs.log_conf_main import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


class TextMessages:
    def __init__(self, text: str = ''):
        self.text = text

    def added(self):
        message = self.text + '✅ Added'
        return message

    def deleted(self):
        message = self.text + 'Deleted 🗑'
        return message


class TextMaintenance(TextMessages):
    def __init__(self, car_model: str, car_model_name: str, maint_title: str,
                 maint_date: datetime, maint_maintenance_mileage: int,
                 maint_description: str):
        super().__init__()
        self.car_model = car_model
        self.car_model_name = car_model_name
        self.maint_title = maint_title
        self.maint_date = maint_date
        self.maint_maintenance_mileage = maint_maintenance_mileage
        self.maint_description = maint_description

    def maintenance_title(self):
        return f'🔧 Maintenance: {self.maint_title}\n'

    def maintenance_date(self):
        date = datetime.strftime(self.maint_date, "%d.%m.%Y")
        return f'📅 Date: {date}\n'

    def maintenance_mileage(self):
        return f'🛣 Maintenance mileage: {self.maint_maintenance_mileage}\n'

    def maintenance_description(self):
        return f'📄 Description: {self.maint_description}\n'

    def maintenance_car(self):
        return f'🚙 Car: {self.car_model} {self.car_model_name}\n'

    def maintenance(self):
        message = self.maintenance_title() + self.maintenance_date()
        return message

    # def maintenance(self):
    #     message = f'🚙 Car: {self.car_model} {self.car_model_name}\n' \
    #               f'🔧 Maintenance: {self.maint_title}\n' \
    #               f'📅 Date: {self.maint_date}\n' \
    #               f'🛣 Maintenance mileage: {self.maint_maintenance_mileage}\n' \
    #               f'📄 Description: {self.maint_description}\n'
    #     return message

    def maintenance_added(self):
        message = self.maintenance() + self.added()
        return message
