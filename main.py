from view.main_view import MainView
from model.click_engine import ClickEngine
from controller.click_controller import ClickController
import sys
import ctypes

if __name__ == "__main__":
    if sys.platform.startswith("win"):
        try:
            app_id = "autoclicker.pro.app.1.0"
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
        except Exception:
            pass

    model = ClickEngine()
    view = MainView()
    controller = ClickController(model, view)
    view.controller = controller

    view.mainloop()