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

class SplitFlapDisplay:
    def __init__(self, backend):
        self.backend = backend
        self.check_address_collisions()
    
    def get_fields(self):
        fields = []
        for name in dir(self):
            candidate = getattr(self, name)
            if hasattr(candidate, '_is_field') and candidate._is_field == True:
                fields.append((name, candidate))
        return fields
    
    def check_address_collisions(self):
        """
        Checks if any of the addresses used by the fields are occupied
        by more than one field and raises an exception is necessary
        """
        addresses = []
        for name, field in self.get_fields():
            addresses += field.address_mapping
        if len(addresses) != len(set(addresses)):
            raise ValueError("Some addresses are occupied by more than one field")
    
    def get_module_data(self):
        """
        Returns all addresses and associated codes of the modules
        making up the display
        """
        module_data = []
        fields = self.get_fields()
        for name, field in fields:
            module_data += field.get_module_data()
        module_data.sort(key=lambda d:d[0])
        return module_data
    
    def update(self):
        self.backend.set_module_data(self.get_module_data())
        self.backend.update()
