# VentCU
> A radically accessible, affordable, and producible ventilator. 

## VentCU has not been clinically tested. It is NOT approved for medical use.

## What is VentCU?
In response to the exploding, unmet demand for ventilators caused by the global COVID-19 crisis, VentCU was developed as an intermediary manual ventilation device for clinical use.  Designed in collaboration with medical professionals and skilled engineers, VentCU is positioned as a **radically affordable** device able to be **assembled with no prior experience and no specialized tools**.  *Constructed entirely from consumer-off-the-shelf parts*, available in the hundreds to thousands in a matter of days, hospital technicians and maker enthusiasts alike will be able to construct VentCU with nothing more than an instruction manual, an Allen key, a pair of scissors, and a soldering iron.

## [VentCU Website](https://coda.io/@maker/ventcu) 
Check out our website (https://coda.io/@maker/ventcu) for detailed technical, BOM, and contact information.
Also, feel free to [support us](https://www.gofundme.com/f/ventcu-open-source-ventilator) or share our work on social media!

## Repository Structure
- Media contains images of the VentCU, including renders and profile views.
- Mechanics contains STEP files of the main assembly and its subcomponents. 
- Electronics contains simple image and Eagle schematics, along with relevant component documentation.
- Software contains the VentCU control system in its native file structure. 

## Software
VentCU runs currently on a Raspberry Pi 4 B, Python, and Flask stack, relying on a touchscreen web interface to view and control RPi GPIO. We have mocked up our main control, homing, and UI state diagrams below:
### Main Control
![main control](software/documentation/main_control_fsm.jpg)
### Homing
![homing](software/documentation/homing_fsm.png)
### Mock UI
![mock ui](software/documentation/mock_ui.png)

Detailed information on configuration, testing, and troubleshooting is forthcoming.

## Software Changelog
Newest on top.

### bbwtb