'''
Author  : Michael Borden
Date    : Feb 6, 2019
Update  : Feb 17, 2019

Purpose : EE class to help simulate electical neural dynamics.
'''
import math

class UnitMathOps:
    def __init__(self, value, units, utype, T):
        self.T = T
        self.value = 0.00
        self.units = units.replace(utype, '')
        self.type  = utype
        self.convTable = {'μ': 10**-6,
                          'n': 10**-6,
                          'm': 10**-3, 
                          '' : 1,
                          'k': 10** 3,
                          'M': 10** 6 }
        self.setValue(value, units)

    def __add__(self, other):
        self.assertType('add', other.type)
        val = self.value + other.value
        return self.T(self.getValue(val, self.units), self.units)

    def __sub__(self, other):
        self.assertType('sub', other.type)
        val = self.value - other.value
        return self.T(self.getValue(val, self.units), self.units)

    def __mul__(self, other):
        self.assertType('mul', other.type)
        val = self.value * other.value
        return self.T(self.getValue(val, self.units), self.units)

    def __div__(self, other):
        self.assertType('div', other.type)
        val = self.value / other.value
        return self.T(self.getValue(val, self.units), self.units)

    def __floordiv__(self, other):
        self.assertType('floordiv', other.type)
        val = self.value // other.value
        return self.T(self.getValue(val, self.units), self.units)

    def __mod__(self, other):
        self.assertType('mod', other.type)
        val = self.value % other.value
        return self.T(self.getValue(val, self.units), self.units)

    def __pow__(self, other):
        self.assertType('pow', other.type)
        val = self.value ** other.value
        return self.T(self.getValue(val, self.units), self.units)

    def __abs__(self):
        val = abs(self.value)
        return self.T(self.getValue(val, self.units), self.units)

    def __lt__(self, other):
        self.assertType('compare', other.type)
        return self.value < other.value

    def __le__(self, other):
        self.assertType('compare', other.type)
        return self.value <= other.value

    def __eq__(self, other):
        self.assertType('compare', other.type)
        return self.value == other.value

    def __ne__(self, other):
        self.assertType('compare', other.type)
        return self.value != other.value

    def __ge__(self, other):
        self.assertType('compare', other.type)
        return self.value >= other.value

    def __gt__(self, other):
        self.assertType('compare', other.type)
        return self.value > other.value

    def __str__(self):
        return '{} {}{}'.format(self.getValue(self.value, self.units), 
                                self.units, self.type)
    
    def assertType(self, func, t):
        assert self.type == t, 'ERROR: Cannot {} type {} and {}' \
                         .format(func, self.type, t)

    def setValue(self, value, units=''):
        self.value = value * self.convTable[units]
        
    def getValue(self, value, units=''):
        return value / self.convTable[units]


class Power(UnitMathOps):
    def __init__(self, watts, units=''):
        P = lambda w, u: Power(w, u)
        UnitMathOps.__init__(self, watts, units , 'W', P) # P

    def volts(self, other):
        assert other.type in ['A', 'Ω'], 'ERROR: Must be type Amps or Ohms'
        if (other.type == 'A'):
            return Voltage(self.value / other.value)
        else:
            return Voltage(math.sqrt(self.value * other.value))
            
    def amps(self, other):
        assert other.type in ['V', 'Ω'], 'ERROR: Must be type Volts or Ohms'
        if (other.type == 'V'):
            return Current(self.value / other.value)
        else:
            return Current(math.sqrt(self.value / other.value))

    def ohms(self, other):
        assert other.type in ['A', 'V'], 'ERROR: Must be type Amps or Volts'
        if (other.type == 'A'):
            return Resistance(self.value / (other.value**2))
        else:
            return Resistance((other.value**2) / self.value)
        
        
class Voltage(UnitMathOps):
    def __init__(self, volts, units=''):
        V = lambda w, u: Voltage(w, u)
        UnitMathOps.__init__(self, volts, units, 'V', V) # V

    def watts(self, other):
        assert other.type in ['A', 'Ω'], 'ERROR: Must be type Amps or Ohms'
        if (other.type == 'A'):
            return Power(self.value * other.value)
        else:
            return Power((self.value**2) / other.value)
            
    def amps(self, other):
        assert other.type in ['W', 'Ω'], 'ERROR: Must be type Watts or Ohms'
        if (other.type == 'W'):
            return Current(other.value / self.value)
        else:
            return Current(math.sqrt(self.value / other.value))

    def ohms(self, other):
        assert other.type in ['A', 'W'], 'ERROR: Must be type Amps, or Watts'
        if (other.type == 'A'):
            return Resistance(self.value / other.value)
        else:
            return Resistance((self.value**2) / other.value)

class Current(UnitMathOps):
    def __init__(self, amps, units=''):
        C = lambda w, u: Current(w, u)
        UnitMathOps.__init__(self, amps, units, 'A', C) # I

    def watts(self, other):
        assert other.type in ['V', 'Ω'], 'ERROR: Must be type Volts or Ohms'
        if (other.type == 'V'):
            return Power(self.value * other.value)
        else:
            return Power((self.value**2) * other.value)
            
    def volts(self, other):
        assert other.type in ['W', 'Ω'], 'ERROR: Must be type Watts or Ohms'
        if (other.type == 'W'):
            return Voltage(other.value / self.value)
        else:
            return Voltage(self.value * other.value)

    def ohms(self, other):
        assert other.type in ['W', 'V'], 'ERROR: Must be type Watts or Volts'
        if (other.type == 'W'):
            return Resistance(ohter.value / (self.value**2))
        else:
            return Resistance(math.sqrt(other.value/self.value))

class Resistance(UnitMathOps):
    def __init__(self, ohms, units=''):
        R = lambda w, u: Resistance(w, u)
        UnitMathOps.__init__(self, ohms, units, 'Ω', R) # R

    def watts(self, other):
        assert other.type in ['A', 'V'], 'ERROR: Must be type Amps or Volts'
        if (other.type == 'A'):
            return Power(self.value * (other.value**2))
        else:
            return Power((other.value**2) / self.value)
            
    def volts(self, other):
        assert other.type in ['A', 'W'], 'ERROR: Must be type Amps or Watts'
        if (other.type == 'A'):
            return Voltage(self.value * other.value)
        else:
            return Voltage(math.sqrt(self.value * other.value))

    def amps(self, other):
        assert other.type in ['W', 'V'], 'ERROR: Must be type Watts or Volts'
        if (other.type == 'W'):
            return Current(math.sqrt(other.value / self.value))
        else:
            return Current(other.value / self.value)
