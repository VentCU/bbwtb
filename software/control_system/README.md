# VentCU Control System
> `version 0.1-alpha`

## Code Flow
`ventilator.py` instantiates a `UIControllerInterface` and passes into it a `UI` and `VentilatorController`.
`ventilator.py` creates a log file in the `\logs` directory.
`ui_controller_interface.py` handles interactions between Qt UI event loop handling of user input and `VentilatorController`
`ventilator_controller.py` instantiates low level sensors and actuators from respective `\sensors` and `\actuators` directories.
`ventilator_controller.py` then handles core continuous ventilation state machine as seen in prior `README`
