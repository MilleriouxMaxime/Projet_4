from controllers.menu_controller import MenuController
from views.base_view import BaseView


def main():

    view = BaseView()
    menu_manager = MenuController(view)
    menu_manager.run()


if __name__ == "__main__":
    main()
