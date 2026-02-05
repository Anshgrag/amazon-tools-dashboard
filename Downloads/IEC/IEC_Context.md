# IEC (Introduction to Electronics and Communication Engineering) - Complete Course Context

## Course Information

**Course Code:** 21ESC143 / 1BESC104C / 22BESC104C  
**Course:** Introduction to Electronics and Communication Engineering  
**Academic Year:** 2022-23 / 2025-26  
**Institution:** Dayananda Sagar College of Engineering, Bangalore

### Course Objectives:
- Operation of Semiconductor diode and their applications
- Transistor operation and its biasing
- Study of linear Op-amps and its applications
- Logic circuits and their optimization
- Principles of Communication Systems

### Course Outcomes:
- CO1: Identify different building blocks in digital electronics using logic gates
- CO2: Understand fundamental concepts of electronic components and devices
- CO3: Apply transistor concepts and design circuits using OPAMPS
- CO4: Describe functioning of communication systems and modulation techniques
- CO5: Appreciate electronic devices and their applications
- CO6: Understand concepts of electronic devices and interdisciplinary applications

---

## MODULE 1: Semiconductor Diode

### 1.1 Diode Introduction
- **Definition:** A diode is a 2-terminal, 2-layer, single-junction semiconductor device made of Silicon or Germanium
- **Construction:** p-type and n-type semiconductor materials joined together (PN junction)
- **Symbol:** Arrowhead indicates direction of conventional current flow
- **Anode:** p-type region, **Cathode:** n-type region
- **Operation:** Unidirectional device - allows current in one direction only

### 1.2 PN Junction and Depletion Region
- **PN Junction:** Formed when p-type and n-type materials are placed in contact
- **Depletion Region:** Region near junction where flow of charge carriers decreases
  - Immobile positive ions at n-side
  - Immobile negative ions at p-side
  - Acts as a barrier preventing further diffusion of electrons and holes

### 1.3 Biasing Conditions
- **Forward Biasing:**
  - Positive terminal to p-type, negative to n-type
  - Reduces depletion region width
  - Allows current to flow
  - Barrier potential must be overcome: 0.7V for Si, 0.3V for Ge
  
- **Reverse Biasing:**
  - Positive terminal to n-type, negative to p-type
  - Increases depletion region width
  - Prevents current flow (only small leakage current in nA range)
  - Reverse saturation current flows due to minority carriers

### 1.4 V-I Characteristics
- **Forward Characteristics:**
  - Cut-in voltage (knee voltage): 0.7V for Si, 0.3V for Ge
  - Below cut-in: negligible current (μA)
  - Above cut-in: rapid increase in current (mA)
  
- **Reverse Characteristics:**
  - Very low reverse current (nA for Si, μA for Ge)
  - Reverse breakdown voltage: large increase in current
  - Typical breakdown voltage: 75V

### 1.5 Rectifiers

#### Half Wave Rectifier (HWR)
- **Circuit:** Single diode with transformer and load
- **Operation:**
  - Positive half cycle: Diode conducts, current flows through load
  - Negative half cycle: Diode does not conduct, no current
- **Parameters:**
  - Average DC voltage: Vdc = Vm/π
  - RMS voltage: VRMS = Vm/2
  - Rectification efficiency: 40.6%
  - Ripple factor: 1.21
  - PIV: Vm

#### Full Wave Rectifier (FWR)
**With Center-Tapped Transformer:**
- **Circuit:** Two diodes, center-tapped transformer
- **Operation:** Both half cycles utilized
- **Parameters:**
  - Average DC voltage: Vdc = 2Vm/π
  - RMS voltage: VRMS = Vm/√2
  - Rectification efficiency: 81.2%
  - Ripple factor: 0.48
  - PIV: 2Vm

**Bridge Rectifier:**
- **Circuit:** Four diodes in bridge configuration
- **Operation:** Uses all four diodes
- **Parameters:**
  - Average DC voltage: Vdc = 2Vm/π
  - RMS voltage: VRMS = Vm/√2
  - Rectification efficiency: 81.2%
  - Ripple factor: 0.48
  - PIV: Vm

### 1.6 Zener Voltage Regulator
- Zener diode operates in reverse breakdown region
- Maintains constant output voltage despite variations in input voltage or load
- Used for voltage regulation in power supplies

### 1.7 Diode Applications
- Diode logic circuits (AND, OR gates)
- Power supply circuits
- Clipping and clamping circuits
- Protection circuits

---

## MODULE 2: Bipolar Junction Transistors (BJT)

### 2.1 Semiconductor Fundamentals

#### N-Type Silicon
- Pentavalent impurities (P, As, Sb, Bi) - 5 valence electrons
- Donor impurities
- Majority carriers: Electrons (negative)
- Doping with phosphorus creates free electrons

#### P-Type Silicon
- Trivalent impurities (B, Al, In, Ga) - 3 valence electrons
- Acceptor impurities
- Majority carriers: Holes (positive)
- Doping with boron creates holes

### 2.2 Transistor Structure
- **BJT (Bipolar Junction Transistor):** Three-layer device
- **Regions:**
  - **Emitter:** Heavily doped, supplies carriers (emits)
  - **Base:** Very thin and lightly doped, controls current flow
  - **Collector:** Moderately doped, largest region, collects carriers
- **Types:** NPN and PNP
- **Junctions:**
  - Emitter-Base (EB) junction
  - Collector-Base (CB) junction
- **Arrow:** Shows conventional current flow direction

### 2.3 Operating Regions
1. **Active Region:**
   - EB junction: Forward biased
   - CB junction: Reverse biased
   - Used for amplification

2. **Saturation Region:**
   - Both junctions: Forward biased
   - Low resistance between C and E
   - Acts as closed switch

3. **Cut-off Region:**
   - Both junctions: Reverse biased
   - Very high resistance
   - Acts as open switch

### 2.4 Transistor Biasing
- Active mode: EB forward, CB reverse biased
- Biasing voltages applied through external DC sources

### 2.5 Current Relationships
- **IE = IB + IC** (Emitter current = Base current + Collector current)
- **Current Amplification Factor (α):** IC/IE (typically 0.95-0.99)
- **Base Current Amplification Factor (β):** IC/IB (typically 50-300)
- **Relationship:** β = α/(1-α) and α = β/(1+β)

### 2.6 Transistor Configurations

#### Common Base (CB) Configuration
- **Input:** Emitter-Base
- **Output:** Collector-Base
- **Characteristics:**
  - Input: High resistance (reverse biased diode at output)
  - Output: Low resistance (forward biased diode at input)
  - Low input impedance, high output impedance
  - Current gain < 1
  - High voltage gain
  - Used as voltage amplifier/current buffer

#### Common Emitter (CE) Configuration
- **Input:** Base-Emitter
- **Output:** Collector-Emitter
- **Characteristics:**
  - Medium input impedance
  - Medium output impedance
  - High current gain (β)
  - High voltage gain
  - Most widely used configuration
  - High power gain

#### Common Collector (CC) Configuration
- **Input:** Base-Collector
- **Output:** Emitter-Collector
- **Characteristics:**
  - High input impedance
  - Low output impedance
  - Voltage gain ≈ 1
  - High current gain
  - Used as voltage buffer (emitter follower)

### 2.7 Field Effect Transistor (FET)

#### Introduction
- **Voltage controlled device** (unlike BJT which is current controlled)
- **Unipolar device** (only majority carriers)
- **Three terminals:** Drain (D), Source (S), Gate (G)

#### JFET (Junction Field Effect Transistor)
- **N-channel JFET:**
  - N-type bar with p-type gates
  - Majority carriers: Electrons
- **P-channel JFET:**
  - P-type bar with n-type gates
  - Majority carriers: Holes
- **Operation:**
  - Gate-source junction always reverse biased
  - Gate current ≈ 0
  - VGS controls drain current
  - Cutoff voltage: VGS(OFF) when channel closes
  - IDSS: Maximum drain current

#### MOSFET (Metal Oxide Semiconductor FET)
- **Enhancement Type (E-MOSFET):**
  - Normally OFF device
  - No channel when VGS = 0
  - Channel formed by applying gate voltage
- **Depletion Type (D-MOSFET):**
  - Pre-existing channel
  - Can operate in enhancement or depletion mode
  - Four terminal device: Drain, Source, Gate, Body/Substrate

---

## MODULE 3: Operational Amplifiers

### 3.1 Introduction
- **Definition:** Direct coupled, multistage, very high gain differential amplifier
- **High input impedance, low output impedance**
- **Output proportional to difference between two inputs**
- **Applications:** Comparators, precision rectifiers, instrumentation amplifiers, DAC, mathematical operations

### 3.2 Op-Amp Basics

#### Symbol and Pin Configuration (IC741)
- **Terminals:**
  - Inverting input (-)
  - Non-inverting input (+)
  - Output
  - +VCC and -VEE (power supplies)
- **Pin 741:**
  - Pin 2: Inverting input
  - Pin 3: Non-inverting input
  - Pin 4: -VEE
  - Pin 6: Output
  - Pin 7: +VCC

#### Equivalent Circuit
- Input resistance (Ri) between inverting and non-inverting terminals
- Voltage-controlled voltage source (A × Vi)
- Output resistance (Ro) in series with voltage source

### 3.3 Voltage Transfer Curve
- **Linear Region:** Vi around 0V, output changes linearly with input
- **Saturation Region:** Changes in Vi have little effect on Vo
- **For 741:** Saturation at ±10V with input differential of 50μV

### 3.4 Block Diagram of Op-Amp
1. **Input Stage:**
   - Dual input, input balanced differential amplifier
   - High voltage gain
   - High input impedance
   - Two input terminals
   - Small input offset voltage and current
   - High CMRR
   - Low input bias current

2. **Intermediate Stage:**
   - Differential amplifier with single-ended output
   - Provides additional voltage gain
   - Cascaded amplifiers

3. **Level Shifting Stage:**
   - Brings DC level to ground potential
   - Prevents distortion and clipping

4. **Output Stage:**
   - Supplies load
   - Low output impedance
   - Push-pull amplifier (Class AB/B)
   - Large output voltage swing
   - Large output current swing
   - Short circuit protection

### 3.5 Op-Amp Characteristics

#### Ideal Op-Amp Characteristics
1. Infinite open loop voltage gain (A = ∞)
2. Infinite input impedance (Ri = ∞)
3. Zero output impedance (Ro = 0)
4. Infinite bandwidth (BW = ∞)
5. Infinite CMRR (Common Mode Rejection Ratio)
6. Infinite slew rate
7. Zero PSRR (Power Supply Rejection Ratio)
8. Zero offset voltage
9. Perfect balance
10. Temperature independent

#### Practical Op-Amp Characteristics (741)
1. Open loop voltage gain: 2×10⁵⁵
2. Input resistance: 2 MΩ
3. Output resistance: 75 Ω
4. Input offset current: 20 nA
5. Input bias current: 80 nA
6. CMRR: 90 dB
7. Bandwidth: 1 MHz at unity gain
8. Slew rate: 0.5 V/μs
9. PSRR: 30 μV/V

### 3.6 Important Parameters

#### Slew Rate
- Maximum rate of change of output voltage (V/μs)
- Limits maximum operating frequency
- For 741: 0.5 V/μs

#### CMRR (Common Mode Rejection Ratio)
- Ratio of differential gain to common mode gain
- CMRR = Ad/Ac
- Expressed in dB: CMRR(dB) = 20 log₁₀(CMRR)
- Figure of merit for op-amp

#### Input Offset Voltage (Vos)
- Differential input required to make output zero
- Typically 1 mV

#### Input Bias Current (IB)
- Average of currents entering two input terminals
- IB = (IB1 + IB2)/2 when Vo = 0V

#### Input Offset Current (Iio)
- Difference between two input currents
- Iio = IB1 - IB2 when Vo = 0V

### 3.7 Negative Feedback
- Reduces voltage gain to controllable levels
- Advantages:
  - Amplifier becomes more linear
  - Input and output impedances modified to ideal values
  - Gain becomes more stable
  - Bandwidth increases

### 3.8 Virtual Ground Concept
- Due to very high gain, potential difference between inputs is very small
- When non-inverting input is grounded, inverting input is at virtual ground
- Current through input terminal is zero

### 3.9 Op-Amp Applications

#### Inverting Amplifier
- **Circuit:** Input to inverting terminal, non-inverting grounded
- **Gain:** Af = -Rf/R1
- **Phase:** 180° phase shift (output inverted)
- **Input impedance:** R1 (low)
- **Output impedance:** Very low

#### Non-Inverting Amplifier
- **Circuit:** Input to non-inverting terminal
- **Gain:** Af = 1 + Rf/R1
- **Phase:** No phase shift (output in-phase)
- **Input impedance:** Very high
- **Output impedance:** Very low

#### Voltage Follower (Buffer Amplifier)
- **Circuit:** R1 = ∞, Rf = 0
- **Gain:** Unity (Af = 1)
- **Vo = Vin**
- Used for impedance matching

#### Inverting Summing Amplifier (Adder)
- **Multiple inputs** to inverting terminal
- **Output:** Vo = -(V1 + V2 + ... + Vn) if Rf = R1 = R2 = ... = Rn
- **General:** Vo = -(Rf/R1×V1 + Rf/R2×V2 + ... + Rf/Rn×Vn)
- Output is negative sum of inputs

#### Non-Inverting Summing Amplifier
- **Multiple inputs** to non-inverting terminal
- **Output:** Vo = (V1 + V2) if R1 = R2 = Rf
- Output is sum of inputs (not inverted)

#### Integrator
- **Circuit:** Feedback capacitor Cf
- **Output:** Vo = -(1/R1Cf)∫Vin dt
- Output is integral of input (with sign change)
- Used in analog computers, filters

#### Differentiator
- **Circuit:** Input capacitor C1
- **Output:** Vo = -RfC1(dVin/dt)
- Output is derivative of input (with sign change)
- Time constant: τ = RfC1

#### Difference Amplifier (Subtractor)
- **Two inputs:** V1 to non-inverting, V2 to inverting
- **Output:** Vo = (Rf/R1)(V1 - V2)
- Amplifies difference between two inputs

---

## MODULE 4: Communication Systems

### 4.1 Block Diagram of Communication System
```
Information Source → Input Transducer → Transmitter → Channel → Receiver → Output Transducer → Destination
```

**Functions:**
- **Information Source:** Produces message (text, voice, video)
- **Input Transducer:** Converts non-electrical message to electrical signal
- **Transmitter:** Processes electrical signal, performs modulation
- **Channel:** Medium through which message travels (guided or unguided)
- **Receiver:** Reproduces message signal, performs demodulation
- **Output Transducer:** Converts electrical signal to original form

### 4.2 Communication Channels

#### Guided Media
- **Twisted Pair:**
  - Two insulated copper wires twisted together
  - Used in telephones, LANs
  - Data rate: ~9600 bps/100m
  - Cheap but susceptible to noise
  
- **Coaxial Cable:**
  - Central copper wire surrounded by insulation and copper mesh
  - Used in cable TV, LANs
  - Impedance: 50Ω or 75Ω
  - Excellent noise immunity
  - Higher bandwidth than twisted pair
  
- **Fiber Optic:**
  - Glass/plastic fibers transmitting light
  - No electrical interference
  - Bandwidth: 2 Gbps
  - Lightweight, thin, low attenuation
  - Expensive to install

#### Unguided Media
- **Radio Waves (3 kHz to 1 GHz):**
  - Omnidirectional, penetrate walls
  - AM/FM radio, TV, cellular, Wi-Fi
  
- **Microwaves (1 GHz to 300 GHz):**
  - Highly directional
  - Satellite, radar, Wi-Fi, microwave ovens
  
- **Infrared (300 GHz to 400 THz):**
  - Short-range, line of sight
  - Remote controls, short-range wireless

### 4.3 Modulation
- **Definition:** Process of varying some parameter of carrier wave in accordance with modulating signal
- **Modulating Signal:** Baseband/information signal
- **Carrier:** High frequency sinusoidal signal

#### Need for Modulation
1. **Reduction in antenna height:**
   - Height = λ/4 = c/(4f)
   - Baseband (10 kHz): 7.5 km - impractical
   - Modulated (1 MHz): 75 m - practical

2. **Avoid mixing of signals:**
   - Different carriers for different signals occupy different frequency slots

3. **Increase range of communication:**
   - Higher frequencies travel longer distances

4. **Multiplexing:**
   - Multiple signals over same channel

5. **Improve reception quality:**
   - FM and digital techniques reduce noise

### 4.4 Types of Modulation

#### Amplitude Modulation (AM)
- **Definition:** Amplitude of carrier varied in proportion to modulating signal
- **Waveform:** Envelope follows modulating signal
- **Applications:** AM radio broadcasting

#### Frequency Modulation (FM)
- **Definition:** Frequency of carrier varied according to instantaneous value of message signal
- **Amplitude and phase constant**
- **Applications:** FM radio broadcasting

#### Phase Modulation (PM)
- **Definition:** Phase of carrier varies as per amplitude variations of message signal
- **Applications:** Digital communications

### 4.5 AM/FM Transmitter Block Diagram
```
Audio → Audio Amplifier → AM Modulator → RF Power Amplifier → Antenna
       ↑
   RF Oscillator
```

**Stages:**
- **Audio:** Processing of audio, quality control
- **AM Modulator:** Modulates RF carrier with audio signal
- **RF Oscillator:** Generates carrier frequency
- **RF Power Amplifier:** Boosts modulated signal

### 4.6 Superheterodyne Receiver
```
Antenna → RF Amplifier → Mixer/Oscillator → IF Amplifier → Detector → Audio Amplifier → Speaker
```

**Stages:**
- **RF Amplifier:** Amplifies received signal
- **Mixer/Oscillator:** Converts RF to Intermediate Frequency (IF)
- **IF Amplifier:** Most amplification occurs here
- **Detector:** Demodulates RF to audio
- **Audio Amplifier:** Amplifies audio for speaker

### 4.7 Mobile Phone Operation (GSM)
**RF Part:**
- RF up converter: Baseband to RF (890-915 MHz)
- RF down converter: RF (935-960 MHz) to baseband

**Baseband Part:**
- Converts voice/data to baseband signal
- DSP-based for latency and power requirements
- Codec: 8 KHz sampling, 13 kbps rate
- ADC/DAC for analog/digital conversion
- AGC, AFC for gain and frequency control

**Hardware Components:**
- Display (LCD, TFT, OLED, touch screen)
- Keypad (numeric, alphabetic)
- Microphone and Speaker
- Camera (mega-pixel sensors)
- Battery (Li-ion, 3.6/3.7V, 600-960 mAh)
- Connectivity (WLAN, Bluetooth, USB, GPS)

### 4.8 GSM Network Architecture

#### Mobile Station (MS)
- Hardware: Display, battery, electronics, IMEI
- SIM: Subscriber identity, IMSI number

#### Base Station Subsystem (BSS)
- **BTS (Base Transceiver Station):**
  - Radio transmitters/receivers
  - Communicates directly with mobiles
  - Um interface with protocols
  
- **BSC (Base Station Controller):**
  - Controls group of BTSs
  - Manages radio resources
  - Handles handovers
  - Abis interface to BTS

#### Network Switching Subsystem (NSS)
- **MSC (Mobile Services Switching Centre):**
  - Main switching node
  - Registration, authentication, call routing
  - Interface to PSTN
  
- **HLR (Home Location Register):**
  - Database of subscriber information
  - Last known location
  
- **VLR (Visitor Location Register):**
  - Selected info from HLR
  - Enables services for current subscriber
  
- **EIR (Equipment Identity Register):**
  - Validates mobile equipment
  - IMEI checking (allowed, barred, monitored)
  
- **AuC (Authentication Centre):**
  - Protected database with secret keys
  - Authentication and ciphering
  
- **GMSC (Gateway Mobile Switching Centre):**
  - Gateway for incoming calls
  - Routes to correct visited MSC
  
- **SMS-G (SMS Gateway):**
  - SMS-GMSC: SMS to mobile
  - SMS-IWMSC: SMS from mobile

#### Operation Support Subsystem (OSS)
- Controls and monitors network
- Manages traffic load
- Maintenance and operations

---

## MODULE 5: Digital Electronics

### 5.1 Number Systems

#### Binary Number System
- **Base:** 2
- **Digits:** 0, 1
- **Position values:** Powers of 2

#### Decimal Number System
- **Base:** 10
- **Digits:** 0-9
- **Position values:** Powers of 10

#### Octal Number System
- **Base:** 8
- **Digits:** 0-7
- **Position values:** Powers of 8

#### Hexadecimal Number System
- **Base:** 16
- **Digits:** 0-9, A-F (10-15)
- **Position values:** Powers of 16

### 5.2 Number Base Conversions

#### Binary to Decimal
- Multiply each bit by 2ⁿ (position from right, starting at 0)
- Sum all values

#### Decimal to Binary
- Repeated division by 2
- Collect remainders (reverse order)

#### Binary to Hexadecimal
- Group into 4 bits (from right)
- Convert each group to hex digit

#### Hexadecimal to Binary
- Convert each hex digit to 4-bit binary
- Concatenate

### 5.3 Complement Methods

#### 1's Complement
- Invert all bits (0→1, 1→0)

#### 2's Complement
- Invert all bits
- Add 1 to LSB

### 5.4 Signed Binary Numbers
- **MSB (Most Significant Bit)** is sign bit
  - 0 = Positive
  - 1 = Negative
- **Remaining bits:** Magnitude
- **Range:** -2ⁿ⁻¹ to +2ⁿ⁻¹ - 1

#### Signed Binary Arithmetic
- **Addition:** Add using standard binary rules, ignore carry-out, check overflow
- **Subtraction:** A - B = A + (2's complement of B)
- **Overflow:** Occurs if signs of operands are same but result sign is different

### 5.5 Boolean Algebra

#### Basic Definitions
- **Boolean Algebra:** Branch of algebra for binary variables (0, 1)
- **Boolean Variable:** Can only be 0 (FALSE/LOW) or 1 (TRUE/HIGH)
- **Boolean Constants:** 0 = FALSE, 1 = TRUE
- **Boolean Operations:**
  - **AND (·):** Output 1 only if all inputs are 1
  - **OR (+):** Output 1 if any input is 1
  - **NOT (Complement, ′):** Inverts value (0→1, 1→0)
- **Boolean Expression:** Combination of variables, constants, operators (Y = A·B + C′)
- **Truth Table:** All input combinations with corresponding outputs
- **Logic Function:** Relationship between inputs and output using Boolean operations
- **Complement:** A′ = 1 if A = 0, A′ = 0 if A = 1

### 5.6 Logic Gates
- **AND Gate:** Output 1 only when all inputs are 1
- **OR Gate:** Output 1 when any input is 1
- **NOT Gate:** Inverts input
- **NAND Gate:** Inverted AND (universal gate)
- **NOR Gate:** Inverted OR (universal gate)
- **XOR Gate:** Output 1 when inputs are different
- **XNOR Gate:** Inverted XOR

#### Universal Gates
- **NAND:** Can implement any logic function
- **NOR:** Can implement any logic function

**Implementation of AND using NOR gates:**
- Three NOR gates required
- First two create NOT gates (invert inputs)
- Third acts as NAND gate
- Final output is AND function

### 5.7 Binary Adders

#### Half Adder
- **Inputs:** A, B (single bits)
- **Outputs:** Sum, Carry
- **Boolean Expressions:**
  - Sum = A ⊕ B
  - Carry = A·B
- **Used only for LSB addition**

#### Full Adder
- **Inputs:** A, B, Cin (carry in)
- **Outputs:** Sum, Cout (carry out)
- **Boolean Expressions:**
  - Sum = A′B′Cin + A′BCin′ + AB′Cin′ + ABCin = A ⊕ B ⊕ Cin
  - Cout = A′BCin + AB′Cin + ABCin′ + ABCin = AB + BCin + ACin
- **Can be implemented using two half adders and one OR gate**

### 5.8 De Morgan's Theorems
1. **First Theorem:** (A + B)′ = A′ · B′
2. **Second Theorem:** (A · B)′ = A′ + B′

### 5.9 Canonical and Standard Forms
- **Canonical Forms:**
  - Sum of Products (SOP): OR of AND terms
  - Product of Sums (POS): AND of OR terms
  
- **Standard Forms:**
  - Standard SOP: Not necessarily canonical
  - Standard POS: Not necessarily canonical

---

## Important Formulas Summary

### Diode and Rectifiers
- **HWR DC Voltage:** Vdc = Vm/π
- **FWR DC Voltage:** Vdc = 2Vm/π
- **HWR RMS Voltage:** VRMS = Vm/2
- **FWR RMS Voltage:** VRMS = Vm/√2
- **HWR Efficiency:** 40.6%
- **FWR Efficiency:** 81.2%
- **HWR Ripple Factor:** 1.21
- **FWR Ripple Factor:** 0.48
- **HWR PIV:** Vm
- **FWR PIV (Center-tapped):** 2Vm
- **FWR PIV (Bridge):** Vm

### Transistor
- **IE = IB + IC**
- **α = IC/IE**
- **β = IC/IB**
- **β = α/(1-α)**
- **α = β/(1+β)**

### Op-Amp
- **Inverting Amplifier:** Af = -Rf/R1
- **Non-Inverting Amplifier:** Af = 1 + Rf/R1
- **Voltage Follower:** Af = 1, Vo = Vin
- **Inverting Summer:** Vo = -(Rf/R1×V1 + Rf/R2×V2 + ...)
- **Non-Inverting Summer:** Vo = (V1R2 + V2R1)/(R1 + R2) × (1 + Rf/R)
- **Integrator:** Vo = -(1/R1Cf)∫Vin dt
- **Differentiator:** Vo = -RfC1(dVin/dt)
- **Difference Amplifier:** Vo = (Rf/R1)(V1 - V2)
- **CMRR:** CMRR = Ad/Ac
- **CMRR(dB):** 20 log₁₀(CMRR)

### Communication
- **Wavelength:** λ = c/f (c = 3×10⁸ m/s)
- **Antenna Height:** h = λ/4
- **Frequency:** f = c/λ

### Digital Electronics
- **2's Complement:** Invert bits + 1
- **Binary to Decimal:** Sum of (bit × 2ⁿ)
- **Full Adder:**
  - Sum = A ⊕ B ⊕ Cin
  - Cout = AB + BCin + ACin

---

## Textbooks and References

**Textbooks:**
1. Electronic Devices and Circuits, David A Bell, 5th Edition, Oxford, 2016
2. Op-amps and Linear Integrated Circuits, Ramakanth A Gayakwad, Pearson Education, 4th Edition
3. Digital Logic and Computer Design, M. Morris Mano, PHI Learning, 2008
4. Dr T C Manjunath etal, "Basic Electronics", 2017, 1st edition, Subhash Publications
5. Electronic Instrumentation and Measurements, David A Bell, Oxford University Press, 2013
6. Electronic Communication Systems, George Kennedy, 4th Edition, TMH

**Reference Books:**
1. Mike Tooley, 'Electronic Circuits, Fundamentals & Applications', 4th Edition, Elsevier, 2015
2. D P Kothari, I J Nagrath, 'Basic Electronics', 2nd edition, McGraw Hill Education, 2018

**E-Resources:**
- https://nptel.ac.in/courses/122106025
- https://nptel.ac.in/courses/108105132
- https://nptel.ac.in/courses/117104072
- https://www.rfwireless-world.com
- https://en.wikipedia.org/wiki/Anti-lock_braking_system
- https://en.wikipedia.org/wiki/Internet_of_things

---

**End of IEC Course Context**
