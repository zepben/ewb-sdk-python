#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from enum import Enum

__all__ = ["UnitSymbol", "unit_symbol_from_id", "unit_symbol_from_cim_name"]


def unit_symbol_from_cim_name(value: str):
    return _unitsymbol_by_cim_name[value]


def unit_symbol_from_id(value: int):
    return _unitsymbol_members_by_id[value]


class UnitSymbol(Enum):
    """
    The derived units defined for usage in the CIM. In some cases, the derived unit is equal to an SI unit. Whenever possible, the standard derived symbol is
    used instead of the formula for the derived unit. For example, the unit symbol Farad is defined as “F” instead of “CPerV”. In cases where a standard
    symbol does not exist for a derived unit, the formula for the unit is used as the unit symbol. For example, density does not have a standard symbol and
    so it is represented as “kgPerm3”. With the exception of the “kg”, which is an SI unit, the unit symbols do not contain multipliers and therefore
    represent the base derived unit to which a multiplier can be applied as a whole. Every unit symbol is treated as an unparseable text as if it were a
    single-letter symbol. The meaning of each unit symbol is defined by the accompanying descriptive text and not by the text contents of the unit symbol. To
    allow the widest possible range of serializations without requiring special character handling, several substitutions are made which deviate from the
    format described in IEC 80000-1. The division symbol “/” is replaced by the letters “Per”. Exponents are written in plain text after the unit as “m3”
    instead of being formatted as “m” with a superscript of 3 or introducing a symbol as in “m^3”. The degree symbol “°” is replaced with the letters “deg”.
    Any clarification of the meaning for a substitution is included in the description for the unit symbol. Non-SI units are included in list of unit symbols
    to allow sources of data to be correctly labelled with their non-SI units (for example, a GPS sensor that is reporting numbers that represent feet
    instead of meters). This allows software to use the unit symbol information correctly convert and scale the raw data of those sources into SI-based
    units. The integer values are used for harmonization with IEC 61850.
    """

    NONE = (0, "none")
    """Dimension less quantity, e.g. count, per unit, etc."""

    METRES = (1, "m")
    """Length in metres."""

    KG = (2, "kg")
    """Mass in kilograms. Note: multiplier “k” is included in this unit symbol for compatibility with IEC 61850-7-3."""

    SECONDS = (3, "s")
    """Time in seconds."""

    A = (4, "A")
    """Current in amperes."""

    K = (5, "K")
    """Temperature in kelvins."""

    MOL = (6, "mol")
    """Amount of substance in moles."""

    CD = (7, "cd")
    """Luminous intensity in candelas."""

    DEG = (8, "deg")
    """Plane angle in degrees."""

    RAD = (9, "rad")
    """Plane angle in radians (m/m)."""

    SR = (10, "sr")
    """Solid angle in steradians (m2/m2)."""

    GY = (11, "Gy")
    """Absorbed dose in grays (J/kg)."""

    BQ = (12, "Bq")
    """Radioactivity in becquerels (1/s)."""

    DEGC = (13, "degC")
    """Relative temperature in degrees Celsius.In the SI unit system the symbol is °C. Electric charge is measured in coulomb that has the unit symbol C. 
    To distinguish degree Celsius from coulomb the symbol used in the UML is degC. The reason for not using °C is that the special character ° is difficult to 
    manage in software."""" """

    SV = (14, "Sv")
    """Dose equivalent in sieverts (J/kg)."""

    F = (15, "F")
    """Electric capacitance in farads (C/V)."""

    C = (16, "C")
    """Electric charge in coulombs (A·s)."""

    SIEMENS = (17, "S")
    """Conductance in siemens."""

    HENRYS = (18, "H")
    """Electric inductance in henrys (Wb/A)."""

    V = (19, "V")
    """Electric potential in volts (W/A)."""

    OHM = (20, "ohm")
    """Electric resistance in ohms (V/A)."""

    J = (21, "J")
    """Energy in joules (N·m = C·V = W·s)."""

    N = (22, "N")
    """Force in newtons (kg·m/s²)."""

    HZ = (23, "Hz")
    """Frequency in hertz (1/s)."""

    LX = (24, "lx")
    """Illuminance in lux (lm/m²)."""

    LM = (25, "lm")
    """Luminous flux in lumens (cd·sr)."""

    WB = (26, "Wb")
    """Magnetic flux in webers (V·s)."""

    T = (27, "T")
    """Magnetic flux density in teslas (Wb/m2)."""

    W = (28, "W")
    """Real power in watts (J/s). Electrical power may have real and reactive components. The real portion of electrical power (I²R or VIcos(phi)), 
    is expressed in Watts. See also apparent power and reactive power."""

    PA = (29, "Pa")
    """Pressure in pascals (N/m²). Note: the absolute or relative measurement of pressure is implied with this entry. See below for more explicit forms."""

    M2 = (30, "m2")
    """Area in square metres (m²)."""

    M3 = (31, "m3")
    """Volume in cubic metres (m³)."""

    MPERS = (32, "mPers")
    """Velocity in metres per second (m/s)."""

    MPERS2 = (33, "mPers2")
    """Acceleration in metres per second squared (m/s²)."""

    M3PERS = (34, "m3Pers")
    """Volumetric flow rate in cubic metres per second (m³/s)."""

    MPERM3 = (35, "mPerm3")
    """Fuel efficiency in metres per cubic metres (m/m³)."""

    KGM = (36, "kgm")
    """Moment of mass in kilogram metres (kg·m) (first moment of mass). 
    Note: multiplier “k” is included in this unit symbol for compatibility with IEC 61850-7-3."""

    KGPERM3 = (37, "kgPerm3")
    """Density in kilogram/cubic metres (kg/m³). Note: multiplier “k” is included in this unit symbol for compatibility with IEC 61850-7-3."""

    M2PERS = (38, "m2Pers")
    """Viscosity in square metres / second (m²/s)."""

    WPERMK = (39, "WPermK")
    """Thermal conductivity in watt/metres kelvin."""

    JPERK = (40, "JPerK")
    """Heat capacity in joules/kelvin."""

    PPM = (41, "ppm")
    """Concentration in parts per million."""

    ROTPERS = (42, "rotPers")
    """Rotations per second (1/s). See also Hz (1/s)."""

    RADPERS = (43, "radPers")
    """Angular velocity in radians per second (rad/s)."""

    WPERM2 = (44, "WPerm2")
    """Heat flux density, irradiance, watts per square metre."""

    JPERM2 = (45, "JPerm2")
    """Insulation energy density, joules per square metre or watt second per square metre."""

    SPERM = (46, "SPerm")
    """Conductance per length (F/m)."""

    KPERS = (47, "KPers")
    """Temperature change rate in kelvins per second."""

    PAPERS = (48, "PaPers")
    """Pressure change rate in pascals per second."""

    JPERKGK = (49, "JPerkgK")
    """Specific heat capacity, specific entropy, joules per kilogram Kelvin."""

    VA = (50, "VA")
    """Apparent power in volt amperes. See also real power and reactive power."""

    VAR = (51, "VAr")
    """
    Reactive power in volt amperes reactive. The “reactive” or “imaginary” component of electrical power (VIsin(phi)). (See also real power and apparent power). 
    Note: Different meter designs use different methods to arrive at their results. Some meters may compute reactive power as an arithmetic value, while others 
    compute the value vectorially. The data consumer should determine the method in use and the suitability of the measurement for the intended purpose.
    """

    COSPHI = (52, "cosPhi")
    """Power factor, dimensionless. 
    Note 1: This definition of power factor only holds for balanced systems. See the alternative definition under code 153. 
    Note 2 : Beware of differing sign conventions in use between the IEC and EEI. It is assumed that the data consumer understands the type of meter in use 
    and the sign convention in use by the utility."""

    VS = (53, "Vs")
    """Volt seconds (Ws/A)."""

    V2 = (54, "V2")
    """Volt squared (W²/A²)."""

    AS = (55, "As")
    """Ampere seconds (A·s)."""

    A2 = (56, "A2")
    """Amperes squared (A²)."""

    A2S = (57, "A2s")
    """Ampere squared time in square amperes (A²s)."""

    VAH = (58, "VAh")
    """Apparent energy in volt ampere hours."""

    WH = (59, "Wh")
    """Real energy in watt hours."""

    VARH = (60, "VArh")
    """Reactive energy in volt ampere reactive hours."""

    VPERHZ = (61, "VPerHz")
    """Magnetic flux in volt per hertz."""

    HZPERS = (62, "HzPers")
    """Rate of change of frequency in hertz per second."""

    CHARACTER = (63, "character")
    """Number of characters."""

    CHARPERS = (64, "charPers")
    """Data rate (baud) in characters per second."""

    KGM2 = (65, "kgm2")
    """Moment of mass in kilogram square metres (kg·m²) (Second moment of mass, commonly called the moment of inertia). Note: multiplier “k” is included in 
    this unit symbol for compatibility with IEC 61850-7-3."""

    DB = (66, "dB")
    """Sound pressure level in decibels. Note: multiplier “d” is included in this unit symbol for compatibility with IEC 61850-7-3."""

    WPERS = (67, "WPers")
    """Ramp rate in watts per second."""

    LPERS = (68, "lPers")
    """Volumetric flow rate in litres per second."""

    DBM = (69, "dBm")
    """Power level (logarithmic ratio of signal strength , Bel-mW), normalized to 1mW. 
    Note: multiplier “d” is included in this unit symbol for compatibility with IEC 61850-7-3."""

    HOURS = (70, "h")
    """Time in hours, hour = 60 min = 3600 s."""

    MIN = (71, "min")
    """Time in minutes, minute = 60 s."""

    Q = (72, "Q")
    """Quantity power, Q."""

    QH = (73, "Qh")
    """Quantity energy, Qh."""

    OHMM = (74, "ohmm")
    """Resistivity, ohm metres, (rho)."""

    APERM = (75, "APerm")
    """A/m, magnetic field strength, amperes per metre."""

    V2H = (76, "V2h")
    """Volt-squared hour, volt-squared-hours."""

    A2H = (77, "A2h")
    """Ampere-squared hour, ampere-squared hour."""

    AH = (78, "Ah")
    """Ampere-hours, ampere-hours."""

    COUNT = (79, "count")
    """Amount of substance, Counter value."""

    FT3 = (80, "ft3")
    """Volume, cubic feet."""

    M3PERH = (81, "m3Perh")
    """Volumetric flow rate, cubic metres per hour."""

    GAL = (82, "gal")
    """Volume in gallons, US gallon (1 gal = 231 in3 = 128 fl ounce)."""

    BTU = (83, "Btu")
    """Energy, British Thermal Units."""

    L = (84, "l")
    """Volume in litres, litre = dm3 = m3/1000."""

    LPERH = (85, "lPerh")
    """Volumetric flow rate, litres per hour."""

    LPERL = (86, "lPerl")
    """Concentration, The ratio of the volume of a solute divided by the volume of the solution. 
    Note: Users may need use a prefix such a ‘µ’ to express a quantity such as ‘µL/L’."""

    GPERG = (87, "gPerg")
    """Concentration, The ratio of the mass of a solute divided by the mass of the solution. 
    Note: Users may need use a prefix such a ‘µ’ to express a quantity such as ‘µg/g’."""

    MOLPERM3 = (88, "molPerm3")
    """Concentration, The amount of substance concentration, (c), the amount of solvent in moles divided by the volume of solution in m³."""

    MOLPERMOL = (89, "molPermol")
    """Concentration, Molar fraction, the ratio of the molar amount of a solute divided by the molar amount of the solution."""

    MOLPERKG = (90, "molPerkg")
    """Concentration, Molality, the amount of solute in moles and the amount of solvent in kilograms."""

    SPERS = (91, "sPers")
    """Time, Ratio of time. Note: Users may need to supply a prefix such as ‘µ’ to show rates such as ‘µs/s’."""

    HZPERHZ = (92, "HzPerHz")
    """Frequency, rate of frequency change. Note: Users may need to supply a prefix such as ‘m’ to show rates such as ‘mHz/Hz’."""

    VPERV = (93, "VPerV")
    """Voltage, ratio of voltages. Note: Users may need to supply a prefix such as ‘m’ to show rates such as ‘mV/V’."""

    APERA = (94, "APerA")
    """Current, ratio of amperages. Note: Users may need to supply a prefix such as ‘m’ to show rates such as ‘mA/A’."""

    VPERVA = (95, "VPerVA")
    """Power factor, PF, the ratio of the active power to the apparent power. 
    Note: The sign convention used for power factor will differ between IEC meters and EEI (ANSI) meters. 
    It is assumed that the data consumers understand the type of meter being used and agree on the sign convention in use at any given utility."""

    REV = (96, "rev")
    """Amount of rotation, revolutions."""

    KAT = (97, "kat")
    """Catalytic activity, katal = mol / s."""

    JPERKG = (98, "JPerkg")
    """Specific energy, Joules / kg."""

    M3UNCOMPENSATED = (99, "m3Uncompensated")
    """Volume, cubic metres, with the value uncompensated for weather effects."""

    M3COMPENSATED = (100, "m3Compensated")
    """Volume, cubic metres, with the value compensated for weather effects."""

    WPERW = (101, "WPerW")
    """Signal Strength, ratio of power. Note: Users may need to supply a prefix such as ‘m’ to show rates such as ‘mW/W’."""

    THERM = (102, "therm")
    """Energy, therms."""

    ONEPERM = (103, "onePerm")
    """Wavenumber, reciprocal metres, (1/m)."""

    M3PERKG = (104, "m3Perkg")
    """Specific volume, cubic metres per kilogram, v."""

    PAS = (105, "Pas")
    """Dynamic viscosity, pascal seconds."""

    NM = (106, "Nm")
    """Moment of force, newton metres."""

    NPERM = (107, "NPerm")
    """Surface tension, newton per metre."""

    RADPERS2 = (108, "radPers2")
    """Angular acceleration, radians per second squared."""

    JPERM3 = (109, "JPerm3")
    """Energy density, joules per cubic metre."""

    VPERM = (110, "VPerm")
    """Electric field strength, volts per metre."""

    CPERM3 = (111, "CPerm3")
    """Electric charge density, coulombs per cubic metre."""

    CPERM2 = (112, "CPerm2")
    """Surface charge density, coulombs per square metre."""

    FPERM = (113, "FPerm")
    """Permittivity, farads per metre."""

    HPERM = (114, "HPerm")
    """Permeability, henrys per metre."""

    JPERMOL = (115, "JPermol")
    """Molar energy, joules per mole."""

    JPERMOLK = (116, "JPermolK")
    """Molar entropy, molar heat capacity, joules per mole kelvin."""

    CPERKG = (117, "CPerkg")
    """Exposure (x rays), coulombs per kilogram."""

    GYPERS = (118, "GyPers")
    """Absorbed dose rate, grays per second."""

    WPERSR = (119, "WPersr")
    """Radiant intensity, watts per steradian."""

    WPERM2SR = (120, "WPerm2sr")
    """Radiance, watts per square metre steradian."""

    KATPERM3 = (121, "katPerm3")
    """Catalytic activity concentration, katals per cubic metre."""

    D = (122, "d")
    """Time in days, day = 24 h = 86400 s."""

    ANGLEMIN = (123, "anglemin")
    """Plane angle, minutes."""

    ANGLESEC = (124, "anglesec")
    """Plane angle, seconds."""

    HA = (125, "ha")
    """Area, hectares."""

    TONNE = (126, "tonne")
    """Mass in tons, “tonne” or “metric ton” (1000 kg = 1 Mg)."""

    BAR = (127, "bar")
    """Pressure in bars, (1 bar = 100 kPa)."""

    MMHG = (128, "mmHg")
    """Pressure, millimetres of mercury (1 mmHg is approximately 133.3 Pa)."""

    MILES_NAUTICAL = (129, "M")
    """Length, nautical miles (1 M = 1852 m)."""

    KN = (130, "kn")
    """Speed, knots (1 kn = 1852/3600) m/s."""

    MX = (131, "Mx")
    """Magnetic flux, maxwells (1 Mx = 10-8 Wb)."""

    G = (132, "G")
    """Magnetic flux density, gausses (1 G = 10-4 T)."""

    OE = (133, "Oe")
    """Magnetic field in oersteds, (1 Oe = (103/4p) A/m)."""

    VH = (134, "Vh")
    """Volt-hour, Volt hours."""

    WPERA = (135, "WPerA")
    """Active power per current flow, watts per Ampere."""

    ONEPERHZ = (136, "onePerHz")
    """Reciprocal of frequency (1/Hz)."""

    VPERVAR = (137, "VPerVAr")
    """Power factor, PF, the ratio of the active power to the apparent power. 
    Note: The sign convention used for power factor will differ between IEC meters and EEI (ANSI) meters. 
    It is assumed that the data consumers understand the type of meter being used and agree on the sign convention in use at any given utility."""

    OHMPERM = (138, "ohmPerm")
    """Electric resistance per length in ohms per metre ((V/A)/m)."""

    KGPERJ = (139, "kgPerJ")
    """Weight per energy in kilograms per joule (kg/J). Note: multiplier “k” is included in this unit symbol for compatibility with IEC 61850-7-3."""

    JPERS = (140, "JPers")
    """Energy rate in joules per second (J/s)."""

    @property
    def short_name(self):
        return str(self)[11:]

    @property
    def name(self):
        return self.value[1]

    def id(self):
        return self.value[0]


_unitsymbol_members_by_id = [us for us in UnitSymbol.__members__.values()]
_unitsymbol_by_cim_name = {str(us): us for us in UnitSymbol.__members__.values()}
