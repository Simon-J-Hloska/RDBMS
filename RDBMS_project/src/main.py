from RDBMS_project.src.ui.menu_controller import MenuController
from RDBMS_project.src.ui.user_interface import UserInterface
from RDBMS_project.src.utils.error_handler import ErrorHandler


def main():
    try:
        mc = MenuController()
        mc.run()
    except Exception as e:
        ui = UserInterface()
        ui.print_error(ErrorHandler.handle_exception(e))

if __name__ == '__main__':
    main()