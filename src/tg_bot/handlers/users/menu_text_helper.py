class MenuText(object):
    def __init__(self, txt=''):
        self.txt = txt

    @staticmethod
    def menu_separator():
        return f'<code>|{30 * "-"}|</code>'

    @staticmethod
    def main_menu():
        return {'add_car': '➕ ADD NEW CAR',
                'show_cars': '🔍 SHOW YOUR CARS'
                }

    @staticmethod
    def register():
        return 'REGISTER'

    @staticmethod
    def cancel():
        return 'CANCEL'

    @staticmethod
    def delete():
        return '❌ DELETE'

    @staticmethod
    def edit_title():
        return 'EDIT TITLE'

    @staticmethod
    def edit_description():
        return 'EDIT DESCRIPTION'

    @staticmethod
    def edit_mileage():
        return 'EDIT MILEAGE'

    @staticmethod
    def edit_date():
        return 'EDIT DATE'

    @staticmethod
    def no_description():
        return 'NO DESCRIPTION'

    @staticmethod
    def edit_car_model():
        return 'EDIT CAR MODEL'

    @staticmethod
    def edit_car_model_name():
        return 'EDIT CAR MODEL NAME'

    @staticmethod
    def edit_car_current_mileage():
        return 'ADD CAR CURRENT MILEAGE'


    @staticmethod
    def add_maintenance():
        return '🔧 ADD NEW CAR MAINTENANCE 🔧'

    @staticmethod
    def show_maintenance():
        return '🔧 SHOW CAR MAINTENANCES 🔧'

    @staticmethod
    def show_maintenances():
        return '🔧 SHOW CAR MAINTENANCES 🔧'



    @staticmethod
    def show_works():
        return '⚙ SHOW CAR MAINTENANCE WORKS ⚙'


cancel_txt = MenuText.cancel()
delete_txt = MenuText.delete()
separator = MenuText.menu_separator()
