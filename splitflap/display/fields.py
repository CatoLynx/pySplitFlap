"""
Copyright 2019 Julian Metzler

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

class BaseField:
    # This is needed so Form.get_fields() will know what to include
    _is_field = True
    
    def __init__(self, start_address = None, length = 1, descending = False, address_mapping = None, display_mapping = None):
        """
        start_address: the address of the first module in this field
        length: How many modules make up this field
        descending: If using start_address, select descending addresses
        address_mapping: If modules have non-sequential addresses, the list of
                         addresses corresponding to the digits in this field
        display_mapping: Optional mapping of split-flap card numbers to
                         displayed text or symbols for all modules in this field
        """
        if start_address is None and address_mapping is None:
            raise AttributeError("Either start_address or address_mapping must be present")
        if type(length) is not int or length <= 0:
            raise ValueError("length must be a positive integer")
        if start_address is not None:
            if start_address not in range(256):
                raise ValueError("start_address must be an int between 0 and 255")
            if descending:
                if start_address - length < 0:
                    raise ValueError("Field is too long for given start address")
            else:
                if start_address + length > 256:
                    raise ValueError("Field is too long for given start address")
        if address_mapping is not None:
            if len(address_mapping) != length:
                raise ValueError("Length of address_mapping doesn't match field length")
        self.start_address = start_address
        self.length = length
        self.descending = descending
        if address_mapping is not None:
            self.address_mapping = address_mapping
        else:
            if self.descending:
                self.address_mapping = list(range(start_address, start_address-length, -1))
            else:
                self.address_mapping = list(range(start_address, start_address+length))
        self.display_mapping = display_mapping
        if display_mapping is not None:
            self.inverse_display_mapping = {v: k for k, v in display_mapping.items()}
        else:
            self.inverse_display_mapping = None
        self.value = None
    
    def set(self, value):
        self.value = value
    
    def get(self):
        return self.value
    
    def get_single_module_data(self, pos):
        raise NotImplementedError
    
    def get_module_data(self):
        module_data = []
        for i in range(self.length):
            module_data.append(self.get_single_module_data(i))
        return module_data


class TextField(BaseField):
    def __init__(self, *args, value = "", upper_only = True, **kwargs):
        super().__init__(*args, **kwargs)
        self.upper_only = upper_only
        self.set(value)
    
    def set(self, value):
        if type(value) is not str:
            raise ValueError("value must be str")
        if self.upper_only:
            value = value.upper()
        self.value = value[:self.length].ljust(self.length)
    
    def get_single_module_data(self, pos):
        """
        Returns the split-flap module address and code for the given position
        in the field with the current field value
        """
        if pos >= self.length:
            raise ValueError("pos must be inside field boundaries")
        addr = self.address_mapping[pos]
        char = self.value[pos]
        if self.display_mapping is not None:
            code = self.inverse_display_mapping.get(char, 0)
        else:
            code = ord(char.encode('iso-8859-1'))
        return addr, code


class CustomMapField(BaseField):
    def __init__(self, display_mapping, *args, value = [], **kwargs):
        super().__init__(*args, display_mapping=display_mapping, **kwargs)
        self.set(value)

    def set(self, value):
        if type(value) not in (list, tuple):
            value = [value] * self.length
        self.value = value[:self.length] + [None] * (self.length - len(value))
    
    def get_single_module_data(self, pos):
        """
        Returns the split-flap module address and code for the given position
        in the field with the current field value
        """
        if pos >= self.length:
            raise ValueError("pos must be inside field boundaries")
        addr = self.address_mapping[pos]
        display_value = self.value[pos]
        code = self.inverse_display_mapping.get(display_value, 0)
        return addr, code