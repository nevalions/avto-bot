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
    def register_txt() -> str:
        return 'Hi! Please register.\n' \
               'We need some info, to add a garage for you.'

    @staticmethod
    def added_txt() -> str:
        return "✅ Added"

    @staticmethod
    def deleted_txt() -> str:
        return "🗑 Deleted"

    @staticmethod
    def item_updated_txt() -> str:
        return "✅ Item updated"

    def ask_to_delete_txt(self):
        return f"Are you sure you want to delete '<b>{self.text}</b>'?"

    def undo_delete_txt(self):
        return f"Undo deletion '<b>{self.text}</b>'"

    @staticmethod
    def add_description_txt() -> str:
        return "📄 Enter 'Description'"

    @staticmethod
    def update_description() -> str:
        return "Update 'Description'"

    @staticmethod
    def action_canceled_txt() -> str:
        return "Action cancelled"


class TextCar(TextMessages):
    def __init__(self, car_model: str = '', car_model_name: str = '',
                 current_mileage: int = 0, measures='km', description=''
                 ):
        super().__init__()
        self.car_model = car_model
        self.car_model_name = car_model_name
        self.current_mileage = current_mileage
        self.measures = measures
        self.description = description

    def car_model_and_model_name_txt(self) -> str:
        return f'🚙 <b>Car</b>: {self.car_model} {self.car_model_name}'

    def car_current_mileage_txt(self):
        return f'🛣 <b>Current mileage</b>: {self.current_mileage}'

    def car_current_mileage_with_measures_txt(self):
        return f'🛣 <b>Current mileage</b>: {self.current_mileage} {self.measures}'

    def car_txt(self) -> str:
        items = [
            self.car_model_and_model_name_txt(),
            self.car_current_mileage_with_measures_txt(),
            self.main_description_txt()
        ]
        return '\n'.join(items)

    @staticmethod
    def no_car() -> str:
        return "YOU DON'T HAVE ANY CAR"

    @staticmethod
    def add_car_model_txt() -> str:
        return "Please, enter car <b>'Model'</b>" \
               "\n(Lada, Ford, Chevrolet, etc)\n\n" \
               "<b>Don't</b> enter model name!"

    def add_car_model_name_txt(self) -> str:
        return f"Enter 'Model Name' for <b>{self.car_model_name}</b>"

    def add_car_mileage_txt(self) -> str:
        return f"{self.car_model_and_model_name_txt()}\n\n" \
               f"Enter <b>'Mileage'</b>"

    def add_car_measure_txt(self) -> str:
        return f"{self.car_model_and_model_name_txt()}\n" \
               f"{self.car_current_mileage_txt()}\n\n" \
               f"Enter <b>'Measures'</b>"

    def add_car_description_txt(self) -> str:
        return f"{self.car_model_and_model_name_txt()}\n" \
               f"{self.car_current_mileage_with_measures_txt()}\n\n" \
               f"{self.add_description_txt()}"

    def update_model_txt(self) -> str:
        return f'🚙 <b>Car:</b> {self.car_model}\n\n' \
               f"Update 'Model'"

    def update_model_name_txt(self) -> str:
        return f'🚙 <b>Car:</b> {self.car_model} <b>{self.car_model_name}</b>\n\n' \
               f"Update 'Model Name'"

    @staticmethod
    def update_car_current_mileage_txt() -> str:
        return "Update car 'Current Mileage'"

    def car_deleted_txt(self):
        return f"{self.car_model_and_model_name_txt()}\n{self.deleted_txt()}"


class TextMaintenance(TextCar):
    def __init__(self, car_model: str = '', car_model_name: str = '',
                 maint_title: str = '', date_main: datetime = None,
                 maintenance_mileage: int = None, description: str = ''):
        super().__init__(car_model, car_model_name)
        TextMessages.__init__(self, description, date_main)

        self.car_model = car_model
        self.car_model_name = car_model_name
        self.maint_title = maint_title
        self.date_main = date_main
        self.maintenance_mileage = maintenance_mileage
        self.description = description

    def maintenance_title_txt(self) -> str:
        return f'🔧 <b>Maintenance</b>: {self.maint_title}'

    def maintenance_mileage_txt(self) -> str:
        return f'🛣 <b>Maintenance mileage</b>: {self.maintenance_mileage}'

    def maintenance_txt(self) -> str:
        items = [
            self.car_model_and_model_name_txt(),
            self.maintenance_title_txt(),
            self.date_to_text(),
            self.maintenance_mileage_txt(),
            self.main_description_txt()
        ]
        return '\n'.join(items)

    def maintenance_added_txt(self):
        return f"{self.maintenance_txt()}\n{self.added_txt()}"

    def maintenance_deleted_txt(self):
        return f"{self.maintenance_title_txt()}\n{self.deleted_txt()}"

    def add_maintenance_txt(self) -> str:
        return f"{self.car_model_and_model_name_txt()}\n\n"\
               f"🔧 Enter maintenance 'Title'"

    @staticmethod
    def add_maintenance_date_txt() -> str:
        return "📅 Please, select maintenance 'Date'"

    @staticmethod
    def add_maintenance_mileage_txt() -> str:
        return "🛣 Enter maintenances 'Mileage'"

    def update_maintenance_txt(self) -> str:
        return f"{self.car_model_and_model_name_txt()}\n"\
               f"{self.maintenance_title_txt()}\n\n"

    def update_maintenance_title_txt(self) -> str:
        return f"{self.update_maintenance_txt()}"\
               f"Enter new maintenance 'Title'"

    def update_maintenance_description_txt(self) -> str:
        return f"{self.update_maintenance_txt()}"\
               f"Enter new maintenance 'Description'"

    def update_maintenance_mileage_txt(self) -> str:
        return f"{self.update_maintenance_txt()}"\
               f"Enter new maintenance 'Mileage'"

    def update_maintenance_date_txt(self) -> str:
        return f"{self.update_maintenance_txt()}"\
               f"Enter new maintenance 'Date'"

    def no_maintenance_txt(self) -> str:
        return f"{self.car_model_and_model_name_txt()}\n"\
               f"Does not have any maintenances"
