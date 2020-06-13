This document provides information about the GUI functionality that needs to be implemented as of 5/24/2020. Reach to to Delphine about any questions.
This is all written with the assumption that the GUI consists of seperate UI files, where each is unhidden/hidden as needed.

start.ui -> first screen that shows up when ventilator is turned on
-Clicking start_button should close current window and open start_homing.ui

start_homing.ui -> screen that allows user to start homing procedure
-Clicking start_button should close current window and open homing.ui. Must also send signal to Raspberry Pi to begin homing procedure.
-Clicking cancel_button should close current window and open start.ui

homing.ui -> waiting screen during homing process
-No buttons are present on this page. Raspberry Pi should send a signal after homing procedure is finished causing current window to close and open confirm_homing.ui

confirm_homing.ui -> user must verify measured Ambu bag size
-Raspberry Pi must send identified bag diameter. bag_size_label must be set to this number. Should be formated as bagsize + '' (Ex: 8'')
-Clicking rehome_button should close current window and open homing.ui. Must also send signal to Raspberry Pi to begin homing procedure
-Clicking confirm_button should close current window and open edit_parameters.ui window.

edit_parameters.ui -> screen for user to modify parameters
-tidal_volume_label is preset to some reasonable number (ex: 500 ml). Clicking tidal_increase_button or tidal_decrease_button should increase or decrease tidal_volume_label by 5ml respectively. (***NOTE: more research should be done in limits of reasonable tidal volume to inform starting and increment values)
-bpm_label is preset to some reasonable number (ex: 40). Clicking bpm_increase_button or bpm_decrease_button should increase or decrease bpm_label by 1 repectively. (***NOTE: more research should be done in limits of reasonable bpm to inform starting and increment values)
-ie_ratio_label is preset to some reasonable number (ex: 1:2). Clicking ie_increase_button or ie_decrease button should increase of decrease the ie_ratio_label. Research should be done to determine what incrementing I:E ratio means. Ex: 2:1, 1:2, 1:3, 1:4...
-Clicking set_button should close current window and open confirm_parameters.ui
-Clicking back_button should close current window and open main.ui. Back button should be HIDDEN if this is the first time turing on ventilator (ie should not be possible to jump to main screen without first confirming parameters)

confirm_parameters.ui -> user must review and confirm parameters before they are enacted
-confirm_bpm_label, confirm_ie_label and confirm_tidal_volume must all be set their corresponding values from their counterparts in edit_paramters.ui
**NOTE: Currently the confirm_parameters.ui is identical to the edit_parameterd.ui with an additional window overlayed on top (confirm_settings). Instead of closing edit_parameters.ui and opening confirm_parameters.ui it may make more sense to simply hide the confirm_settings window.
-Clicking confirm_button should close current window and open main_screen.ui
-Clicking cancel_button should close current window and open edit_parameters.ui

main_window.ui -> default window shown during ventilation that shows status of different parameters/pressure readings
Note: this screen is exactly the same as mock.ui but only contains pressure graph
-Graphs (pressure_graph and volume_graph) must receive and plot pressure readings from Pi-Clicking edit_parameters_button should close current window and open edit_parameters.ui
-NEW: set_TV_label, set_BPM_label, set_IE_label, set_PIP_label, set_PEEP_label, set_PLAT_label should all display user settings for the parameters (or preset thresholds for pressures)
-NEW: measured_TV_label, measured_BPM_label, measured_IE_label, measured_PIP_label, measured_PEEP_label, measured_PLAT_label should display measured pressures and parameters
-NEW: message_log_label should display appropriate message (alarm message, nothing etc.)

alarm_condidtion.ui -> shown when alarm condition is triggered
-Raspberry Pi must send alarm signal. Current window closes and alarm_condition.ui is shown.
-error_message_label is set to text corresponding to alarm condition sent by the Pi
-dismiss_alarm button closes current window and opens main_screen.ui. Signal is sent to Pi to silence alarm.
-silence_alarm closes current window and opens main_screen.ui. Signal is sent to Pi to silence alarm for 2 minutes.
Note: A conversation about alarm logic still needs to happen--> what does it mean to fully dismiss alarm? How does one reset dismissed alarms?
