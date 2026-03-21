# /usr/bin/python3
# -*- coding: utf-8 -*-
"""
standardAtmosphere - Implements 1976 NASA standard atmosphere model to height 84 km.
Based on Public Domain Aeronautical Software

Created at 03.08.21 20:17

@author: David Potucek

ICAO Standard atmosphere
MSA (Mezinarodni standardni atmosfera)
Model předpokládá že:
    - atmosféra je homogenní, složení vzduchu 78 % dusík, 21 % kyslík, 1 % ostatní plyny
    - vzduch je ideální plyn, tj. platí stavová rovnice plynů
    - tíhové zrychlení je konstantní g = 9,81 m/s2
    - podmínky ve výšce H = 0 m (při hladině moře)
        - tlak vzduchu 101325 Pa (1013.25 hPa)
        - hustota vzduchu 1,225 kg/m3
        - teplota vzduchu 15 °C (288.15 K)
    - až do výšky 11 km (tj. až do tropopauzy) klesá teplota o 6,5 stupně Celsia na 1 000 m, potom zůstává konstantní -56,5 °C"""

import math

#   S E A   L E V E L   C O N D I T I O N S
STANDARD_PRESSURE = 101325.0    # [Pa]
STANDARD_TEMPERATURE = 288.15   # [K]
STANDARD_DENSITY = 1.225        # [kg/m^3]
ASOUNDZERO = 340.294    # speed of sound at S.L.  m/sec
MUZERO = 1.7894E-5      # viscosity at sea-level, kg/(m·s)
ETAZERO = 1.4607E-5     # kinetic viscosity at sea-level, m²/s
KAPPA_ZERO = 0.025326   # thermal coeff. at sea-level [watts per meter per kelvin]

# Physical constants
G = 9.80665             # gravitational acceleration [m/s²]
R = 287.05287           # specific gas constant for air [J/(kg·K)]
GAMMA = 1.4             # ratio of specific heats
KELVIN2C = 273.15       # Kelvin to Celsius conversion


def simple_atm(alt):
    '''Prijme vysku v metrech a vrati hustotu[kg/m^3], tlak[hPa] a teplotu[C] do 11km.
    :param alt [m]
    :return hustota, tlak, teplota, sound_speed
        hustota [kg/m^3]
        tlak [hPa]
        teplota [C]
        sound_speed [m/s]
    '''
    if alt > 11000:
        raise ValueError('Altitude exceeds 11000m limit for simple_atm()')
    
    tepl = 15 - 0.0065 * alt
    temp = (1 - alt/44308)
    tlkx = 1013.25 * pow(temp, 5.2553)
    hustx = 1.225 * pow(temp, 4.2553)
    sound_speed = 20.05 * math.sqrt(tepl + KELVIN2C)
    return hustx, tlkx, tepl, sound_speed


def get_atmosphere_properties(altitude):
    """Calculate atmospheric properties at given altitude using 1976 Standard Atmosphere.
    
    :param altitude: Geometric altitude [m], valid up to 84852m
    :return: Dictionary with atmospheric properties
        - temperature [K]
        - pressure [Pa]
        - density [kg/m³]
        - sound_speed [m/s]
        - viscosity [kg/(m·s)]
        - kinematic_viscosity [m²/s]
    """
    # Atmospheric layers (geopotential altitude, temperature, lapse rate)
    layers = [
        (0, 288.15, -0.0065),      # Troposphere
        (11000, 216.65, 0.0),      # Tropopause
        (20000, 216.65, 0.001),    # Stratosphere 1
        (32000, 228.65, 0.0028),   # Stratosphere 2
        (47000, 270.65, 0.0),      # Stratopause
        (51000, 270.65, -0.0028),  # Mesosphere 1
        (71000, 214.65, -0.002),   # Mesosphere 2
    ]
    
    if altitude < 0 or altitude > 84852:
        raise ValueError(f'Altitude {altitude}m out of valid range [0, 84852]m')
    
    # Find appropriate layer
    layer_idx = 0
    for i, (h, _, _) in enumerate(layers):
        if altitude >= h:
            layer_idx = i
        else:
            break
    
    h_base, T_base, lapse_rate = layers[layer_idx]
    
    # Calculate temperature
    T = T_base + lapse_rate * (altitude - h_base)
    
    # Calculate pressure
    if layer_idx == 0:
        P_base = STANDARD_PRESSURE
    else:
        # Calculate base pressure for this layer
        P_base = STANDARD_PRESSURE
        for i in range(layer_idx):
            h0, T0, L = layers[i]
            h1 = layers[i + 1][0]
            if L != 0:
                P_base *= (T0 / (T0 + L * (h1 - h0))) ** (G / (R * L))
            else:
                P_base *= math.exp(-G * (h1 - h0) / (R * T0))
    
    if lapse_rate != 0:
        P = P_base * (T_base / T) ** (G / (R * lapse_rate))
    else:
        P = P_base * math.exp(-G * (altitude - h_base) / (R * T))
    
    # Calculate density using ideal gas law
    rho = P / (R * T)
    
    # Calculate speed of sound
    a = math.sqrt(GAMMA * R * T)
    
    # Calculate viscosity (Sutherland's formula)
    mu = MUZERO * (T / STANDARD_TEMPERATURE) ** 1.5 * (STANDARD_TEMPERATURE + 110.4) / (T + 110.4)
    
    # Calculate kinematic viscosity
    nu = mu / rho
    
    return {
        'temperature': T,
        'pressure': P,
        'density': rho,
        'sound_speed': a,
        'viscosity': mu,
        'kinematic_viscosity': nu
    }


def altitude_to_pressure(altitude):
    """Convert altitude to pressure.
    
    :param altitude: Altitude [m]
    :return: Pressure [Pa]
    """
    return get_atmosphere_properties(altitude)['pressure']


def pressure_to_altitude(pressure):
    """Convert pressure to altitude using iterative method.
    
    :param pressure: Pressure [Pa]
    :return: Altitude [m]
    """
    # Simple troposphere formula for initial guess
    alt_guess = 44308 * (1 - (pressure / STANDARD_PRESSURE) ** 0.1903)
    
    # Newton-Raphson iteration
    for _ in range(10):
        P_calc = altitude_to_pressure(alt_guess)
        if abs(P_calc - pressure) < 1:
            break
        # Numerical derivative
        dP = altitude_to_pressure(alt_guess + 1) - P_calc
        alt_guess -= (P_calc - pressure) / dP
    
    return alt_guess


def density_altitude(pressure_altitude, temperature, humidity=0):
    """Calculate density altitude from pressure altitude, temperature, and humidity.
    
    Density altitude is the altitude in standard atmosphere that has the same density
    as the current conditions. Critical for aircraft performance calculations.
    
    :param pressure_altitude: Pressure altitude [m]
    :param temperature: Actual temperature [°C]
    :param humidity: Relative humidity [%], default 0
    :return: Density altitude [m]
    """
    T_kelvin = temperature + KELVIN2C
    
    # Get standard pressure at pressure altitude
    P = altitude_to_pressure(pressure_altitude)
    
    # Calculate vapor pressure if humidity provided
    if humidity > 0:
        # Saturation vapor pressure (Magnus formula)
        e_s = 611.2 * math.exp(17.67 * temperature / (temperature + 243.5))
        e = (humidity / 100.0) * e_s
        # Virtual temperature correction for humidity
        T_virtual = T_kelvin / (1 - (e / P) * (1 - 0.622))
    else:
        T_virtual = T_kelvin
    
    # Calculate actual density
    rho_actual = P / (R * T_virtual)
    
    # Find altitude with same density in standard atmosphere
    # Use binary search
    alt_low, alt_high = 0, 20000
    for _ in range(30):
        alt_mid = (alt_low + alt_high) / 2
        rho_std = get_atmosphere_properties(alt_mid)['density']
        if rho_std > rho_actual:
            alt_low = alt_mid
        else:
            alt_high = alt_mid
        if abs(rho_std - rho_actual) < 1e-6:
            break
    
    return alt_mid


def print_values(a, t, tl, h, s):
    print('vyska nastavena na {} m'.format(a))
    print('v této výšce jsou parametry standardní atmosféry:')
    print('teplota: {} [C]'.format(t))
    print('tlak: {:0.2f} [hPa]'.format(tl))
    print('hustota: {:0.4f} [kg/m^3]'.format(h))
    print('rychlost zvuku: {:0.4f} [m/s]'.format(s))


if __name__ == "__main__":
    # Test simple_atm
    alt = 500
    hust, tlk, tplt, spd = simple_atm(alt)
    print_values(alt, tplt, tlk, hust, spd)
    
    print('\n--- Advanced atmosphere properties ---')
    props = get_atmosphere_properties(5000)
    print(f'At 5000m:')
    print(f'  Temperature: {props["temperature"]:.2f} K ({props["temperature"]-KELVIN2C:.2f} °C)')
    print(f'  Pressure: {props["pressure"]:.2f} Pa ({props["pressure"]/100:.2f} hPa)')
    print(f'  Density: {props["density"]:.4f} kg/m³')
    print(f'  Sound speed: {props["sound_speed"]:.2f} m/s')
    
    print('\n--- Density altitude example ---')
    da = density_altitude(1000, 30, 80)
    print(f'Pressure altitude: 1000m, Temp: 30°C, Humidity: 80%')
    print(f'Density altitude: {da:.0f}m')