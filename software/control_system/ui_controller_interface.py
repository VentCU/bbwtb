class UIControllerInterface:

    def __init__(self, ventilator_ui, ventilator_controller):
        self.ui = ventilator_ui
        self.controller = ventilator_controller

        self.interface_elements()

    def interface_elements(self):

        self.ui.stack.start.start_button.clicked.connect(
            lambda: self.controller.start()
        )
