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

import serial


class KroneHLSTController:
    """
    Controls a HLST (Heizungs- und Lichtsteuerung)
    (heater, fan and light control) board.
    """
    
    CMD_GET_STATUS = 0x01
    CMD_LOCK = 0xC6
    CMD_UNLOCK = 0xC7
    CMD_CONTROL = 0x0A

    def __init__(self, port, debug = False):
        self.debug = debug
        self.port = serial.Serial(port, baudrate=19200, timeout=1.0)
    
    def build_parameters(self, light, heater, fan, force_heater, force_fan, low_min_temp):
        """
        light: 1=on, 0=off
        heater: 1=on, 0=off
        fan: 1=on, 0=off
        force_heater: 1=force on, 0=automatic
        force_fan: 1=force on, 0=automatic
        low_min_temp: 1=-20°C temperature limit, 0=0°C temperature limit
        """
        parameter_byte = 0x00
        parameter_byte |= int(light) << 7
        parameter_byte |= int(heater) << 6
        parameter_byte |= int(fan) << 5
        parameter_byte |= int(force_heater) << 2
        parameter_byte |= int(force_fan) << 1
        parameter_byte |= int(low_min_temp)
        return parameter_byte
        
    def send_command(self, address, command, parameters = None, num_response_bytes = 0):
        if command == self.CMD_GET_STATUS:
            control = 0x81 # read data
        elif command in (self.CMD_LOCK, self.CMD_UNLOCK, self.CMD_CONTROL):
            control = 0x02 # write data, one block, no ack
        else:
            control = 0x00 # invalid
        
        data = [command]
        
        if parameters is not None:
            data.append(parameters)
        
        payload = [0x10, address, 0x00, control, 0x01] + data + [0x00]
        length = len(payload)
        payload[2] = length
        
        checksum = 0x00
        for byte in payload:
            checksum ^= byte
        
        cmd_bytes = [0xff, 0xff] + payload + [checksum]
        
        if self.debug:
            print(" ".join((format(x, "02X") for x in cmd_bytes)))
        
        # Send it
        self.port.write(bytearray(cmd_bytes))

        # Read response
        if num_response_bytes > 0:
            return self.port.read(num_response_bytes)
        else:
            return None
    
    def send_heartbeat(self, address):
        cmd_bytes = [0xff, 0xff, 0x10, address, 0x00]
        if self.debug:
            print(" ".join((format(x, "02X") for x in cmd_bytes)))
        self.port.write(bytearray(cmd_bytes))
