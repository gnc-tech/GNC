# CGM91AD10 Tactical-Grade Six Degrees of Freedom Inertial Sensor

> A highly compatible alternative to ADIS16495, featuring precision tactical-grade 6DoF inertial measurement

![CGM91AD10 Tactical-Grade Six Degrees of Freedom Inertial Sensor](https://www.gnc-tech.com/products/navigation/mems/imu/D-Q-JDW-CGM91AD10/D-Q-JDW-CGM91AD10.webp)

## 📋 Basic Information

| Item | Information |
|------|------|
| **Product Model** | `D-Q-JDW-CGM91AD10` |
| **Product Category** | navigation / mems / imu |
| **Product Page** | [https://www.gnc-tech.com/products/mems-imu-6-dof-cgm91ad10/](https://www.gnc-tech.com/products/mems-imu-6-dof-cgm91ad10/) |
| **Source File Path** | `navigation\mems\imu\D-Q-JDW-CGM91AD10.mdx` |

## 🔧 Available Models

- **CGM91AD10** (`D-Q-JDW-CGM91AD10`)

## 🏷️ Keywords

`CGM91AD10` • `Tactical-Grade IMU` • `ADIS16495 Alternative` • `6DoF Inertial Sensor`

## 📖 Detailed Technical Information

## D-Q-JDW-CGM91AD10

### Overview

The **CGM91AD10** is a tactical-grade 6DoF inertial measurement unit (IMU), integrating triaxial gyroscopes and accelerometers in a sealed ceramic package. It delivers low-noise, stable data across −45°C to +85°C.

Factory calibration ensures excellent bias stability and minimal drift. With a digital SPI interface and integrated filtering, it offers easy system integration.

**CGM91AD10** is fully compatible with the ADIS16495 series, serving as a high-performance, drop-in alternative for advanced inertial applications.

### Product Images

![Product Image](https://www.gnc-tech.com/products/navigation/mems/imu/D-Q-JDW-CGM91AD10/D-Q-JDW-CGM91AD10-Slide-01.webp)

![Product Image](https://www.gnc-tech.com/products/navigation/mems/imu/D-Q-JDW-CGM91AD10/D-Q-JDW-CGM91AD10-Slide-02.webp)

![Product Image](https://www.gnc-tech.com/products/navigation/mems/imu/D-Q-JDW-CGM91AD10/D-Q-JDW-CGM91AD10-Slide-03.webp)

### Features

- Fully calibrated triaxial gyroscope and accelerometer
- Industry-leading in-run bias stability and random walk performance
- Digital SPI interface with programmable FIR filtering and averaging
- Robust ceramic vacuum package with enhanced noise isolation
- High resistance to mechanical shock (up to 10,000 g survival)
- Compact, lightweight form factor: optimized for embedded use
- Configurable I/O, data-ready alarm, and external clock sync support
- Single supply voltage operation (3.0 – 3.6 V)
- Compatible with ADIS16495 form factor, electrical and data interface

### package

#### Dimensions(mm)
<ProductImage 
productId="D-Q-JDW-CGM91AD10" 
type="package" 
subType="dimensions" 
invertMode="light-only" 
/>
    
{
  headers: ['Attribute', 'Value'],
  rows: [
['Length', '47 mm'],
['Width', '44 mm'],
['Height', '15 mm'],
['Weight', '48 ± 2 g']
  ]

#### Pins
<ProductImage 
productId="D-Q-JDW-CGM91AD10" 
type="package" 
subType="pins" 
invertMode="light-only" 
/>
<ProductImage 
productId="D-Q-JDW-CGM91AD10" 
type="package" 
subType="pin-assignments" 
invertMode="light-only" 
/>
    
{
  headers: ['Pin', 'Name', 'Type', 'Description'],
  rows: [
['1', 'DIO3', 'Input/Output', 'Configurable Digital I/O'],
['2', 'DIO4', 'Input/Output', 'Configurable Digital I/O'],
['3', 'SCLK', 'Input', 'SPI Clock'],
['4', 'DOUT', 'Output', 'SPI Data Output (SCLK falling edge)'],
['5', 'DIN', 'Input', 'SPI Data Input (SCLK rising edge)'],
['6', 'CS', 'Input', 'Chip Select (active low)'],
['7', 'DIO1', 'Input/Output', 'Configurable Digital I/O'],
['8', 'RST', 'Input', 'Reset (leave floating if unused)'],
['9', 'DIO2', 'Input/Output', 'Configurable Digital I/O'],
['10,11', 'VDD', 'Supply', 'Power Supply Input'],
['13,14', 'GND', 'Supply', 'Ground'],
['12,15–24', 'DNC', '-', 'Do Not Connect']
  ]

> **Note:**
> 1. This representation displays the top view pinout for the mating socket connector.
> 2. The actual connector pins are not visible from the top view.
> 3. Mating connector: SAMTEC CLM-112-02 or equivalent.
> 4. DNC = Do not connect to these pins.

### Applications

- Inertial Navigation Systems (INS)
- Unmanned Aerial Vehicles (UAVs)
- Platform Stabilization & Control
- Industrial Robotics
- Surveying Equipment
- Geophysical Instrumentation
- Personnel and Asset Tracking

### Specifications

#### Gyroscope Performance (Each Axis)

  _High stability, low noise, and factory-calibrated response for tactical-grade navigation._

  
{
headers: ['Parameter', 'Min', 'Typ', 'Max', 'Unit'],
rows: [
  ['Dynamic Range', '±450', '–', '±480', '°/sec'],
  ['Sensitivity', '–', '2,621,440', '–', 'LSB/°/sec'],
  ['Repeatability', '–', '0.01', '–', '%'],
  ['Sensitivity Temp. Coefficient', '–', '±10', '–', 'ppm/°C'],
  ['Nonlinearity', '–', '0.02', '–', '% of FS'],
  ['Bias Repeatability', '–', '1.0', '–', '°/hr'],
  ['In-Run Bias Stability', '–', '0.3', '–', '°/hr'],
  ['Angular Random Walk', '–', '0.1', '–', '°/√hr'],
  ['Bias Temp. Coefficient', '–', '±0.15', '–', '°/hr/°C'],
  ['Linear Acceleration Effect on Bias', '–', '1.0', '–', '°/hr/g'],
  ['Output Noise (RMS)', '–', '0.05', '–', '°/sec'],
  ['Rate Noise Density', '–', '0.002', '–', '°/sec/√Hz'],
  ['3 dB Bandwidth', '250', '–', '–', 'Hz'],
  ['Sensor Resonant Frequency', '11.5', '12', '13.5', 'kHz']
]

  > 📝 _In-run bias stability as low as 0.3 °/hr and angular random walk under 0.1 °/√hr provide excellent short-term and long-term precision._

  ---

#### Accelerometer Performance (Each Axis)

  _Designed for precise motion detection in dynamic systems with minimal drift and noise._

  
{
headers: ['Parameter', 'Min', 'Typ', 'Max', 'Unit'],
rows: [
  ['Dynamic Range', '–', '±30', '–', 'g'],
  ['Sensitivity', '–', '65,536,000', '–', 'LSB/g'],
  ['Repeatability', '–', '±0.02', '–', '%'],
  ['Sensitivity Temp. Coefficient', '–', '±5', '–', 'ppm/°C'],
  ['Misalignment (Axis to Axis)', '–', '±0.05', '–', 'degrees'],
  ['Misalignment (Axis to Frame)', '–', '±0.05', '–', 'degrees'],
  ['Nonlinearity (±20 g range)', '–', '0.05', '–', '% of FS'],
  ['Bias Repeatability', '–', '1.5', '–', 'mg'],
  ['In-Run Bias Stability', '–', '10', '–', 'µg'],
  ['Velocity Random Walk', '–', '0.02', '–', 'm/s/√hr'],
  ['Bias Temp. Coefficient', '–', '±0.005', '–', 'mg/°C'],
  ['Output Noise (RMS)', '–', '1.0', '–', 'mg'],
  ['Noise Density', '–', '25', '–', 'µg/√Hz'],
  ['3 dB Bandwidth', '200', '–', '–', 'Hz'],
  ['Sensor Resonant Frequency', '5.5', '–', '–', 'kHz']
]

  > 📝 _Exceptional in-run bias stability (10 µg) and low noise floor enable accurate linear motion tracking even under vibration._

  ---

#### Electrical & Timing Characteristics

  _Comprehensive interface and timing support for flexible integration into embedded platforms._

  
{
headers: ['Parameter', 'Min', 'Typ', 'Max', 'Unit'],
rows: [
  ['Input High Voltage (VIH)', '2.5', '–', '–', 'V'],
  ['Input Low Voltage (VIL)', '–', '0.45', '–', 'V'],
  ['Logic 1 Input Current', '–', '10', '–', 'µA'],
  ['Logic 0 Input Current', '–', '10', '–', 'µA'],
  ['Input Capacitance', '–', '10', '–', 'pF'],
  ['Output High Voltage (VOH)', '2.65', '–', '–', 'V'],
  ['Output Low Voltage (VOL)', '–', '0.4', '–', 'V'],
  ['Flash Endurance', '100000', '–', '–', 'cycles'],
  ['Flash Data Retention', '20 yrs', '–', '–', 'years'],
  ['Power-On Start-Up Time', '1000', '–', '–', 'ms'],
  ['Reset Recovery Time', '500', '–', '–', 'ms'],
  ['Flash Update Time', '375', '–', '–', 'ms'],
  ['Test Time', '50', '–', '–', 'ms'],
  ['Conversion Rate', '3.2', '–', '–', 'kSPS'],
  ['Initial Clock Accuracy', '0.01', '–', '–', '%'],
  ['Clock Temp. Coefficient', '20', '–', '–', 'ppm/°C'],
  ['Sync Input Clock Range', '0.7', '3.2', '–', 'kHz'],
  ['Operating Voltage', '3.0', '3.3', '3.6', 'V'],
  ['Power Supply Current', '–', '380', '–', 'mA']
]

    
> **Note:**
> - All specifications are typical values unless otherwise noted.
> - For mechanical specifications, refer to the [Package](#package) section.
  

---

**🔗 View Online**: [https://www.gnc-tech.com/products/mems-imu-6-dof-cgm91ad10/](https://www.gnc-tech.com/products/mems-imu-6-dof-cgm91ad10/)
