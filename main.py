from view.main_view import MainView
from model.click_engine import ClickEngine
from controller.click_controller import ClickController

if __name__ == "__main__":
    model = ClickEngine()
    view = MainView()
    controller = ClickController(model, view)
    view.controller = controller

    view.mainloop()