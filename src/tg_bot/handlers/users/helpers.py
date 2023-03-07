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
            description: str = ''
    ):
        self.text = text
        self.date_main = date_main
        self.description = description

    def date_to_text(self) -> str:
        return f'📅 <b>Date</b>: {self.date_main.strftime("%d.%m.%Y")}'

    def main_description_txt(self) -> str:
        return f'📄 <b>Info</b>: {self.description}'

    @staticmethod
    def added() -> str:
        return '✅ Added'

    @staticmethod
    def deleted() -> str:
        return '🗑 Deleted'

    def ask_to_delete(self):
        return f"Are you sure you want to delete '<b>{self.text}</b>'?"

    def undo_delete(self):
        return f"Undo deletion '<b>{self.text}</b>'"

    @staticmethod
    def add_description_txt() -> str:
        return '📄 Enter description'

    @staticmethod
    def update_description() -> str:
        return 'Update description'

    @staticmethod
    def action_canceled() -> str:
        return 'Action cancelled'

    @staticmethod
    def item_updated() -> str:
        return '✅ Item updated'


class TextCar(TextMessages):
    def __init__(self, car_model: str = '', car_model_name: str = '',
                 current_mileage: int = 0, measures='km', description=''
                 ):
        super().__init__()
        self.car_model = car_model
        self.car_model_name = car_model_name
        self.current_mileage = current_mileage
        self.measures = measures
        self.description_main = description

    def car_model_and_model_name(self) -> str:
        return f'🚙 <b>Car</b>: {self.car_model} {self.car_model_name}'

    def car_current_mileage(self):
        return f'🛣 <b>Current mileage</b>: {self.current_mileage} {self.measures}'

    def car_txt(self) -> str:
        items = [
            self.car_model_and_model_name(),
            self.car_current_mileage(),
            self.main_description_txt()
        ]
        return '\n'.join(items)

    @staticmethod
    def no_car() -> str:
        return "YOU DON'T HAVE ANY CAR"

    def update_model(self) -> str:
        return f'🚙 <b>Car:</b> {self.car_model}\n' \
               f"Update 'Model'"

    def update_model_name(self) -> str:
        return f'🚙 <b>Car:</b> {self.car_model} <b>{self.car_model_name}</b>\n' \
               f"Update 'Model Name'"

    @staticmethod
    def update_car_current_mileage() -> str:
        return "Update car <b>current mileage</b>"

    def car_deleted(self):
        return f"{self.car_model_and_model_name()}\n{self.deleted()}"


class TextMaintenance(TextCar):
    def __init__(self, car_model: str = '', car_model_name: str = '',
                 maint_title: str = '', date_main: datetime = None,
                 maint_maintenance_mileage: int = None, description: str = ''):
        super().__init__(car_model, car_model_name)
        TextMessages.__init__(self, description, date_main)

        self.car_model = car_model
        self.car_model_name = car_model_name
        self.maint_title = maint_title
        self.date_main = date_main
        self.maint_maintenance_mileage = maint_maintenance_mileage
        self.description_main = description

    def maintenance_title(self) -> str:
        return f'🔧 <b>Maintenance</b>: {self.maint_title}'

    def maintenance_mileage(self) -> str:
        return f'🛣 <b>Maintenance mileage</b>: {self.maint_maintenance_mileage}'

    def maintenance_txt(self) -> str:
        items = [
            self.car_model_and_model_name(),
            self.maintenance_title(),
            self.date_to_text(),
            self.maintenance_mileage(),
            self.main_description_txt()
        ]
        return '\n'.join(items)

    def maintenance_added(self):
        return f"{self.maintenance_txt()}\n{self.added()}"

    def maintenance_deleted(self):
        return f"{self.maintenance_title()}\n{self.deleted()}"

    def add_maintenance_txt(self) -> str:
        return f"{self.car_model_and_model_name()}\n"\
               f"🔧 Enter maintenance 'Title'"

    @staticmethod
    def add_date_txt() -> str:
        return "📅 Please, select maintenance 'Date'"

    @staticmethod
    def add_maintenance_mileage_txt() -> str:
        return "🛣 Enter maintenances 'Mileage'"
