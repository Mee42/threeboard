## Threeboard

![Image](https://github.com/Mee42/threeboard/blob/master/pictures/render-v1.png)

All tagged commits contain pcb designs that were ordered.

#### For building:
- make sure you have both the
[random parts](https://github.com/ai03-2725/random-keyboard-parts.pretty)
and the
[mx switch footprint](https://github.com/ai03-2725/MX_Alps_Hybrid.pretty)
libraries imported into kicad.


The python-mock runs on a raspberry pi, with BCM pins 16, 20, and 21 used as input and pin 12 as the status led. python2 is used due to gpio libaries.

