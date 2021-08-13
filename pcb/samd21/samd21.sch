EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L MCU_Microchip_SAMD:ATSAMD21E17A-A U?
U 1 1 6116145F
P 4900 4500
F 0 "U?" H 5530 4546 50  0000 L CNN
F 1 "ATSAMD21E17A-A" H 5530 4455 50  0000 L CNN
F 2 "Package_QFP:TQFP-32_7x7mm_P0.8mm" H 5800 2650 50  0001 C CNN
F 3 "http://ww1.microchip.com/downloads/en/DeviceDoc/SAM_D21_DA1_Family_Data%20Sheet_DS40001882E.pdf" H 4900 4500 50  0001 C CNN
	1    4900 4500
	1    0    0    -1  
$EndComp
$Comp
L random-keyboard-parts:Molex-0548190589 USB?
U 1 1 6116C819
P 1300 3200
F 0 "USB?" V 1837 3167 60  0000 C CNN
F 1 "Molex-0548190589" V 1731 3167 60  0000 C CNN
F 2 "" H 1300 3200 60  0001 C CNN
F 3 "" H 1300 3200 60  0001 C CNN
	1    1300 3200
	0    -1   -1   0   
$EndComp
$Comp
L Regulator_Linear:TLV70033_SOT23-5 U?
U 1 1 6117B146
P 2600 3100
F 0 "U?" H 2600 3442 50  0000 C CNN
F 1 "TLV70033_SOT23-5" H 2600 3351 50  0000 C CNN
F 2 "Package_TO_SOT_SMD:SOT-23-5" H 2600 3425 50  0001 C CIN
F 3 "http://www.ti.com/lit/ds/symlink/tlv700.pdf" H 2600 3150 50  0001 C CNN
	1    2600 3100
	1    0    0    -1  
$EndComp
$Comp
L Device:C_Small C?
U 1 1 6117F8EA
P 1850 3100
F 0 "C?" H 1942 3146 50  0000 L CNN
F 1 "1uF" H 1942 3055 50  0000 L CNN
F 2 "" H 1850 3100 50  0001 C CNN
F 3 "~" H 1850 3100 50  0001 C CNN
	1    1850 3100
	1    0    0    -1  
$EndComp
Connection ~ 1850 3000
Wire Wire Line
	1600 3000 1850 3000
Wire Wire Line
	1850 3000 2200 3000
Wire Wire Line
	1600 3400 1850 3400
Wire Wire Line
	1850 3200 1850 3400
Connection ~ 1850 3400
Wire Wire Line
	1850 3400 2600 3400
Wire Wire Line
	2900 3000 3000 3000
Wire Wire Line
	2600 3400 3000 3400
Connection ~ 2600 3400
$Comp
L Device:C_Small C?
U 1 1 61187842
P 3000 3100
F 0 "C?" H 3092 3146 50  0000 L CNN
F 1 "1uF" H 3092 3055 50  0000 L CNN
F 2 "" H 3000 3100 50  0001 C CNN
F 3 "~" H 3000 3100 50  0001 C CNN
	1    3000 3100
	1    0    0    -1  
$EndComp
Connection ~ 3000 3000
Wire Wire Line
	3000 3000 3650 3000
Wire Wire Line
	3000 3200 3000 3400
Connection ~ 3000 3400
Wire Wire Line
	3000 3400 3700 3400
Wire Wire Line
	2200 3000 2200 3100
Wire Wire Line
	2200 3100 2300 3100
Connection ~ 2200 3000
Wire Wire Line
	2200 3000 2300 3000
Text GLabel 3650 3000 2    50   Input ~ 0
3v
Text GLabel 3700 3400 2    50   Input ~ 0
GND
$EndSCHEMATC
