Lennox LCC Experiments
======================

The Lennox iComfort system is relatively powerful, but doesn't expose all of its power through the iComfort web interface. It also doesn't provide an official integration SDK, only offering indirect access through HomeKit and IFTTT and so on.

There is a local HTTPS port running on the system, and the Android Mobile Setup app gives examples on how to use it. Instead of going through the internet to iComfort, this approach interfaces directly with the device which provides more detailed information:

```
Comp. Short Cycle Delay Active: No
Cooling Rate: 32.5 %
Heating Rate: 0.0 %
Compressor Shift Delay Active: No
Defrost Status: Off
Reversing Valve Status: Cool Mode
High Pressure Switch: Closed
Low Pressure Switch: Closed
Top Cap Switch Status: Closed
Liquid Line Temp: 71.8 F
Ambient Temp: 66.8 F
Coil Temp: 73.2 F
Run Time Since Last Defrost: 0 min
Control Will Defrost at Delta: 0.0 F
Current Delta: -6.8 F
Compressor Active Alarm: 0
Compressor Hz: 22.0 Hz
Compressor Speed Reduction: Off
Heat Sink Temperature: 75.2 F
Inverter Input Voltage: 246.0 V
Inverter Input Current: 2.398 A
DC Link Voltage: 331.0 V
Compressor Current: 2.930 A
Heating Rate: 0.0 %
Blower CFM Demand: 450 CFM
Blower Off Delay: Off
Blower On Delay: Off
Indoor Blower RPM: 388
Indoor Blower Power: 2.5 %
Outdoor Temperature: open
Discharge Air Temperature: open
Line Voltage: 586.9 V
24VAC Voltage: 27.8 V
G - Input: Off
W1 - Input: Off
Upstage Timer: Off
# of Electric Heat Sections ON: 0
Link Relay Status: Closed
Defrost Status: Off
Dehumidification Relay Status: Open
Humidification Relay Status: Open
O Relay Status: Open
Y2 Relay Status: Open
Y1 Relay Status: Open
Detecting Electrical Heat: Off
Undetected Electric Heat: No
Electric Heat On Delay: Off
Outdoor Temperature: 64
Demand: 32.5
Humidity: 51
Temperature: 73
```
