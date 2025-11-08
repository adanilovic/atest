#!/usr/bin/python3

"""
Standard python import statements
"""

"""
Custom python import statements
"""
from arm.register import *

class CLIDR_EL1(Register):

    ctype_name_value_dict = {0 : 'No cache',
                             1 : 'Instruction cache only',
                             2 : 'Data cache only',
                             3 : 'Separate instruction and data caches',
                             4 : 'Unified cache'}

    def __init__(self):
        Register.__init__(self, {
            'ICB'    : RegisterField(name='Inner Cache Boundary',
                                     width=3, shift=30, value=0,
                                     name_value_dict={0 : 'Not disclosed by this mechanism',
                                                      1 : 'L1 cache is the highest Inner Cacheable level',
                                                      2 : 'L2 cache is the highest Inner Cacheable level',
                                                      3 : 'L3 cache is the highest Inner Cacheable level',
                                                      4 : 'L4 cache is the highest Inner Cacheable level',
                                                      5 : 'L5 cache is the highest Inner Cacheable level',
                                                      6 : 'L6 cache is the highest Inner Cacheable level',
                                                      7 : 'L7 cache is the highest Inner Cacheable level',
                                     }),
            'LoUU'   : RegisterField(name='Level of Unification Uniprocessor', width=3, shift=27, value=0, name_value_dict={}),
            'LoC'    : RegisterField(name='Level of Coherence', width=3, shift=24, value=0, name_value_dict={}),
            'LoUIS'  : RegisterField(name='Level of Unfication Inner Shareable', width=3, shift=21, value=0, name_value_dict={}),
            'Ctype7' : RegisterField(name='Cache Type 7', width=3, shift=18, value=0,
                                     name_value_dict=CLIDR_EL1.ctype_name_value_dict),
            'Ctype6' : RegisterField(name='Cache Type 6', width=3, shift=15, value=0,
                                     name_value_dict=CLIDR_EL1.ctype_name_value_dict),
            'Ctype5' : RegisterField(name='Cache Type 5', width=3, shift=12, value=0,
                                     name_value_dict=CLIDR_EL1.ctype_name_value_dict),
            'Ctype4' : RegisterField(name='Cache Type 4', width=3, shift=9,  value=0,
                                     name_value_dict=CLIDR_EL1.ctype_name_value_dict),
            'Ctype3' : RegisterField(name='Cache Type 3', width=3, shift=6,  value=0,
                                     name_value_dict=CLIDR_EL1.ctype_name_value_dict),
            'Ctype2' : RegisterField(name='Cache Type 2', width=3, shift=3,  value=0,
                                     name_value_dict=CLIDR_EL1.ctype_name_value_dict),
            'Ctype1' : RegisterField(name='Cache Type 1', width=3, shift=0,  value=0,
                                     name_value_dict=CLIDR_EL1.ctype_name_value_dict),
        })

class CCSIDR_EL1(Register):

    def __init__(self):
        Register.__init__(self, {
            'LineSize'        : RegisterField(name='Cache Line Size',
                                              width=3, shift=0, value=0,
                                              name_value_dict={},
                                              conversion_function=self.calc_cache_line_size_from_register_value),
            'Associativity'   : RegisterField(name='Associativity of cache - 1',
                                              width=10, shift=3, value=0,
                                              name_value_dict={},
                                              conversion_function=self.calc_associativity_from_register_value),
            'NumSets'         : RegisterField(name='Number of sets - 1',
                                              width=15, shift=13, value=0,
                                              name_value_dict={},
                                              conversion_function=self.calc_num_sets_from_register_value),
        })

    def calc_cache_line_size_from_register_value(self, field_value):
        return pow(2, field_value + 4)

    def calc_associativity_from_register_value(self, field_value):
        return (field_value + 1)

    def calc_num_sets_from_register_value(self, field_value):
        return (field_value + 1)

    def cache_size(self):
        return self.fields['LineSize'].get_value() * \
                self.fields['Associativity'].get_value() * \
                  self.fields['NumSets'].get_value()

class ID_AA64MMFR0_EL1(Register):

    def __init__(self):
        Register.__init__(self, {
            'PARange'        : RegisterField(name='Physical Address range supported',
                                             width=4, shift=0, value=0,
                                             name_value_dict={0 : '4GB',
                                                              1 : '64GB',
                                                              2 : '1TB',
                                                              3 : '4TB',
                                                              4 : '16TB',
                                                              5 : '256TB',
                                                              6 : '4PB',
                                             }),

            'ASIDBits'        : RegisterField(name='Number of ASID bits',
                                             width=4, shift=4, value=0,
                                             name_value_dict={0 : '8 bits',
                                                              2 : '16 bits',
                                             }),
            'BigEnd'        : RegisterField(name='Mixed-endian configuration support',
                                             width=4, shift=8, value=0,
                                             name_value_dict={0 : 'No Mixed-endian support',
                                                              1 : 'Mixed-endian support',
                                             }),
            'SNSMem'        : RegisterField(name='Secure versus Non-secure Memory distinction',
                                             width=4, shift=12, value=0,
                                             name_value_dict={0 : 'Does not support a distinction between Secure and Non-secure memory',
                                                              1 : 'Does support a distinction between Secure and Non-secure memory',
                                             }),
            'BigEndEL0'        : RegisterField(name='Mixed-endian support at EL0 only',
                                             width=4, shift=16, value=0,
                                             name_value_dict={0 : 'No mixed-endian support at EL0',
                                                              1 : 'Mixed-endian support at EL0',
                                             }),
            'TGran16'        : RegisterField(name='Support for 16KB memory translation granule size',
                                             width=4, shift=16, value=0,
                                             name_value_dict={0 : '16KB granule not supported',
                                                              1 : '16KB granule supported',
                                             }),
            'TGran64'        : RegisterField(name='Support for 64KB memory translation granule size',
                                             width=4, shift=24, value=0,
                                             name_value_dict={0 : '64KB granule supported',
                                                              1 : '64KB granule not supported',
                                             }),
            'TGran4'        : RegisterField(name='Support for 4KB memory translation granule size',
                                             width=4, shift=28, value=0,
                                             name_value_dict={0x0 : '4KB granule supported',
                                                              0xf : '4KB granule not supported',
                                             }),
        })

