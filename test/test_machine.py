from unittest.mock import Mock
from plover.machine.base import ThreadedStenotypeBase, SerialStenotypeBase
from test.test_passport import MockSerial

class MyMachine(ThreadedStenotypeBase):
    def run(self):
        raise "some unexpected error"

def test_update_machine_staten_on_unhandled_exception():
    machine = MyMachine()
    callback = Mock()
    machine.add_state_callback(callback)
    machine.start_capture()
    machine.join()
    callback.assert_called_with('disconnected')

class MySerialMachine(SerialStenotypeBase):
    def run(self):
        raise "some unexpected error"

def test_close_serial_port_on_unhandled_exception(monkeypatch):
    MockSerial.close = Mock()
    monkeypatch.setattr('plover.machine.base.serial.Serial', MockSerial)
    machine = MySerialMachine({})
    machine.start_capture()
    machine.join()
    MockSerial.close.assert_called()
