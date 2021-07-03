## Threeboard: The portable keyboard with **three** Keys!

That's right, 3 keys. Here's a picture of the prototype, see below for how it works:


![The first prototype. Pictured is three keys, with wires to a breadboard with leds, with jumpers to a raspberry pi 4. Two of the keys are pressed and the corrosponding leds are lit](proto1.jpg)

**This prototype is currently functional! It only outputs to STDOUT, and supports only letters and some select symbols, but it does indeed work**


Here's how it works: The user goes through a series of state changes with key chords. A chord is one or more key pressed at the same time. Chords are denoted in binary, from left to right. The chord `000` is unrepresentable, but all others are; `001`, `010`, `011`, `100`, `101`, `110`, `111`

Users start a character at the top of the state tree. By using the left two keys, the user inputs a number from 1 to 3 - but more commonly denoted `01`, `10`, and `11`, to match what your fingers are doing. This branch down the tree is picked, travelled down, and the process repeats. The process ends when the user types the chord '111', which looks at the current place on the tree and types that character. Here's a picture of the tree. Nodes under the `11` side are currently up for debate, and will change in the future. Functionality such as uppercase letters will work by passing through a 'shift' node, which then leads to back to the top of the tree, for the user to pick their desired character


![A state tree. See codes.txt for the textual representation of this](tree.svg)
