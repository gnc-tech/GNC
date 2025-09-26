# CGM92AD10 Tactical-Grade 10DoF Inertial Measurement Unit

> High-precision 10DoF IMU integrating gyroscopes, accelerometers, magnetometers, and barometric pressure sensor

![CGM92AD10 Tactical-Grade 10DoF Inertial Measurement Unit](https://www.gnc-tech.com/images/products/navigation/mems/imu/D-Q-JDW-CGM92AD10/D-Q-JDW-CGM92AD10.webp)

## 📋 Basic Information

| Item | Information |
|------|------|
| **Product Model** | `D-Q-JDW-CGM92AD10` |
| **Product Category** | navigation / mems / imu |
| **Product Page** | [https://www.gnc-tech.com/products/mems-imu-10-dof-cgm92ad10/](https://www.gnc-tech.com/products/mems-imu-10-dof-cgm92ad10/) |
| **Source File Path** | `navigation\mems\imu\D-Q-JDW-CGM92AD10.mdx` |

## 🔧 Available Models

- **CGM92AD10** (`D-Q-JDW-CGM92AD10`)

## 🏷️ Keywords

`CGM92AD10` • `Tactical-Grade 10DoF IMU` • `ADIS16488 Alternative` • `10DoF Inertial Sensor`

## 📖 Detailed Technical Information


## D-Q-JDW-CGM92AD10

  
### overview

    # Overview
    ---
    The **CGM92AD10** is a tactical-grade 10DoF inertial measurement unit integrating gyroscopes, accelerometers, magnetometers, and a barometric pressure sensor in a compact, vacuum-sealed ceramic package. It provides low-noise, stable inertial and environmental measurements across −45°C to +85°C.

    Factory-calibrated and ready for integration, **CGM92AD10** is a mechanical and electrical drop-in replacement for the ADIS16488 series, ideal for navigation, stabilization, and sensing in challenging environments.
  

  
### slider

    
#### Product Images

![Product Image](https://www.gnc-tech.com/images/products/D-Q-JDW-CGM92AD10-Slide-01.webp)

![Product Image](https://www.gnc-tech.com/images/products/D-Q-JDW-CGM92AD10-Slide-02.webp)

![Product Image](https://www.gnc-tech.com/images/products/D-Q-JDW-CGM92AD10-Slide-03.webp)

![Product Image](https://www.gnc-tech.com/images/products/D-Q-JDW-CGM92AD10-Slide-04.webp)


  

  
### features

    - Full 10DoF sensing: gyroscope, accelerometer, magnetometer, barometer
    - Factory-calibrated for bias, sensitivity, and alignment
    - Low in-run bias drift and angular random walk
    - SPI digital interface, up to 2.46 kSPS
    - Built-in FIR filtering and data decimation
    - Operating temperature: −45°C to +85°C
    - Shock survivability up to 10,000 g
    - Single 3.0–3.6 V power supply
  

  
### package

    #### Dimensions(mm)
    <ProductImage
        productId="D-Q-JDW-CGM92AD10" 
        type="package" 
        subType="overview" 
        invertMode="light-only" 
    />
    <ProductImage 
        productId="D-Q-JDW-CGM92AD10" 
        type="package" 
        subType="dimensions" 
        invertMode="light-only" 
    />
    
```json
{
      headers: ['Attribute', 'Value'],
      rows: [
        ['Length', '47 mm'],
        ['Width', '44 mm'],
        ['Height', '14 mm'],
        ['Weight', '48 g']
      ]
    
```

    #### Pins
    <ProductImage 
        productId="D-Q-JDW-CGM92AD10" 
        type="package" 
        subType="pins" 
        invertMode="light-only" 
    />
    <ProductImage 
        productId="D-Q-JDW-CGM92AD10" 
        type="package" 
        subType="pin-assignments" 
        invertMode="light-only" 
    />
    
```json
{
      headers: ['Pin', 'Name', 'Type', 'Description'],
      rows: [
        ['1', 'DIO3', 'Input/Output', 'Configurable Digital I/O'],
        ['2', 'DIO4', 'Input/Output', 'Configurable Digital I/O'],
        ['3', 'SCLK', 'Input', 'SPI Clock'],
        ['4', 'DOUT', 'Output', 'SPI Data Output (SCLK falling edge)'],
        ['5', 'DIN', 'Input', 'SPI Data Input (SCLK rising edge)'],
        ['6', 'CS', 'Input', 'Chip Select'],
        ['7', 'DIO1', 'Input/Output', 'Configurable Digital I/O'],
        ['8', 'RST', 'Input', 'Reset (optional)'],
        ['9', 'DIO2', 'Input/Output', 'Configurable Digital I/O'],
        ['10–12', 'VDD', 'Supply', 'Main Power Supply'],
        ['13–15', 'GND', 'Supply', 'Power Ground'],
        ['23', 'VDDRTC', 'Supply', 'Real-Time Clock Power'],
        ['Others', 'DNC', '-', 'Do Not Connect']
      ]
    
```

    > **Note:**
    > 1. This representation displays the top view pinout for the mating socket connector.
    > 2. The actual connector pins are not visible from the top view.
    > 3. Mating connector: SAMTEC CLM-112-02 or equivalent.
    > 4. DNC = Do not connect to these pins.
  

  
### applications

    - Inertial navigation and GNSS aiding
    - UAV and robotics guidance
    - Platform and gimbal stabilization
    - Oil & gas downhole tools
    - Mining and geophysical surveying
    - Mobile mapping and autonomous vehicles
  

  
### specifications

    
      #### Gyroscope Performance (Each Axis)

      _Stable angular rate sensing with ultra-low noise and robust environmental calibration._

      
```json
{
        headers: ['Parameter', 'Min', 'Typ', 'Max', 'Unit'],
        rows: [
          ['Dynamic Range', '±450', '–', '±510', '°/sec'],
          ['Sensitivity', '–', '3.052×10⁻⁷', '–', '°/sec/LSB'],
          ['Repeatability', '–', '0.02', '–', '%'],
          ['Sensitivity Temp. Coefficient', '–', '±10', '–', 'ppm/°C'],
          ['Misalignment (Axis to Axis)', '–', '±0.03', '–', '°'],
          ['Misalignment (Axis to Frame)', '–', '±0.03', '–', '°'],
          ['Nonlinearity', '–', '0.01', '–', '% of FS'],
          ['Bias Repeatability', '–', '0.016', '–', '°/sec'],
          ['In-Run Bias Stability', '–', '4.0', '–', '°/hr'],
          ['Angular Random Walk', '–', '0.26', '–', '°/√hr'],
          ['Bias Temp. Coefficient', '–', '±0.00025', '–', '°/sec/°C'],
          ['Linear Accel. Effect on Bias', '–', '0.003', '–', '°/sec/g'],
          ['Output Noise', '–', '0.1', '–', '°/sec rms'],
          ['Rate Noise Density', '–', '0.0049', '–', '°/sec/√Hz'],
          ['3 dB Bandwidth', '330', '330', '–', 'Hz'],
          ['Sensor Resonant Frequency', '22', '22', '–', 'kHz']
        ]
      
```


      > 📝 _Dynamic stability and angular accuracy support precision inertial guidance with low noise and bias drift._

      ---

      #### Accelerometer Performance (Each Axis)

      _Precision linear acceleration measurement across dynamic and static conditions._

      
```json
{
        headers: ['Parameter', 'Min', 'Typ', 'Max', 'Unit'],
        rows: [
          ['Dynamic Range', '±18', '±20', '–', 'g'],
          ['Sensitivity', '–', '1.221×10⁻⁸', '–', 'g/LSB'],
          ['Repeatability', '–', '±0.02', '–', '%'],
          ['Sensitivity Temp. Coefficient', '–', '±5', '–', 'ppm/°C'],
          ['Misalignment (Axis to Axis)', '–', '±0.06', '–', '°'],
          ['Misalignment (Axis to Frame)', '–', '±0.06', '–', '°'],
          ['Nonlinearity (±10 g)', '–', '0.05', '–', '% of FS'],
          ['Nonlinearity (±18 g)', '–', '0.08', '–', '% of FS'],
          ['Bias Repeatability', '–', '5', '–', 'mg'],
          ['In-Run Bias Stability', '–', '0.01', '–', 'mg'],
          ['Velocity Random Walk', '–', '0.007', '–', 'm/s/√hr'],
          ['Bias Temp. Coefficient', '–', '±0.025', '–', 'mg/°C'],
          ['Output Noise', '–', '1.0', '–', 'mg rms'],
          ['Noise Density', '–', '0.088', '–', 'mg/√Hz'],
          ['3 dB Bandwidth', '330', '330', '–', 'Hz'],
          ['Sensor Resonant Frequency', '5.5', '5.5', '–', 'kHz']
        ]
      
```


      ---

      #### Magnetometer Performance

      _3-axis magnetic sensing for heading estimation and environment mapping._

      
```json
{
        headers: ['Parameter', 'Min', 'Typ', 'Max', 'Unit'],
        rows: [
          ['Dynamic Range', '±2.5', '–', '–', 'gauss'],
          ['Sensitivity', '0.1', '–', '–', 'mgauss/LSB'],
          ['Initial Sensitivity Tolerance', '±2', '–', '–', '%'],
          ['Sensitivity Temp. Coefficient', '60', '–', '–', 'ppm/°C'],
          ['Misalignment (Axis to Axis)', '0.35', '–', '–', '°'],
          ['Misalignment (Axis to Frame)', '1.0', '–', '–', '°'],
          ['Nonlinearity', '0.5', '–', '–', '% of FS'],
          ['Initial Bias Error', '±15', '–', '–', 'mgauss'],
          ['Bias Temp. Coefficient', '0.03', '–', '–', 'mgauss/°C'],
          ['Output Noise', '0.22', '–', '–', 'mgauss rms'],
          ['Noise Density', '0.042', '–', '–', 'mgauss/√Hz'],
          ['3 dB Bandwidth', '330', '–', '–', 'Hz']
        ]
      
```


      ---

      #### Barometric Pressure Sensor

      _Environmental pressure sensing for altitude compensation and fusion._

      
```json
{
        headers: ['Parameter', 'Min', 'Typ', 'Max', 'Unit'],
        rows: [
          ['Pressure Range', '300', '1100', '–', 'mbar'],
          ['Extended Range', '10', '1200', '–', 'mbar'],
          ['Sensitivity', '6.1×10⁻⁷', '–', '–', 'mbar/LSB'],
          ['Total Error', '4.5', '–', '–', 'mbar'],
          ['Relative Error', '2.5', '–', '–', 'mbar'],
          ['Nonlinearity (FS)', '0.1', '–', '–', '% of FS'],
          ['Nonlinearity (−45 to +85 °C)', '0.2', '–', '–', '% of FS'],
          ['Linear-g Sensitivity', '0.005', '–', '–', 'mbar/g']
        ]
      
```


      ---

      #### Electrical & Timing Characteristics

      _Compatible with 3.3V logic systems and high-speed SPI communication._

      
```json
{
        headers: ['Parameter', 'Min', 'Typ', 'Max', 'Unit'],
        rows: [
          ['Input High Voltage (VIH)', '2.0', '–', '–', 'V'],
          ['Input Low Voltage (VIL)', '–', '–', '0.8', 'V'],
          ['Logic 1 Input Current', '–', '10', '–', 'µA'],
          ['RST/CS Input Current', '–', '330', '–', 'µA'],
          ['Input Capacitance', '–', '10', '–', 'pF'],
          ['Output High Voltage (VOH)', '2.4', '–', '–', 'V'],
          ['Output Low Voltage (VOL)', '–', '0.4', '–', 'V'],
          ['Flash Endurance', '100000', '–', '–', 'cycles'],
          ['Flash Data Retention', '20 yrs', '–', '–', 'years'],
          ['Power-On Start-Up Time', '1000', '–', '–', 'ms'],
          ['Reset Recovery Time', '500', '–', '–', 'ms'],
          ['Flash Update Time', '375', '–', '–', 'ms'],
          ['Conversion Rate', '2.46', '–', '–', 'kSPS'],
          ['Clock Accuracy', '0.01', '–', '–', '%'],
          ['Clock Temp. Coefficient', '20', '–', '–', 'ppm/°C'],
          ['Sync Input Clock Range', '0.712', '2.4', '–', 'kHz'],
          ['Operating Voltage', '3.0', '–', '3.6', 'V'],
          ['Power Supply Current', '–', '60', '–', 'mA'],
          ['RTC Supply Current', '–', '13', '–', 'µA']
        ]
      
```

    
    > **Note:**
    > - All specifications are typical values unless otherwise noted.
    > - For mechanical specifications, refer to the [Package](#package) section.
  

---

*This document is automatically generated from source file `navigation\mems\imu\D-Q-JDW-CGM92AD10.mdx` *

**🔗 View Online**: [https://www.gnc-tech.com/products/mems-imu-10-dof-cgm92ad10/](https://www.gnc-tech.com/products/mems-imu-10-dof-cgm92ad10/)
