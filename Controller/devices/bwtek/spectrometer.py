from ctypes import *

from lantz.foreign import LibraryDriver
from lantz import Action
from lantz import Feat, DictFeat
from lantz import Q_


class spectrometer(LibraryDriver):
    LIBRARY_NAME = 'bwtekusb.dll'
    def __init__(self,channel):
        super(spectrometer,self).__init__()
        self.channel = c_int(channel)
        self.intTime = 0*Q_('ms')

    @Action()
    def initDevice(self):
        return self.lib.InitDevices()

    @Action()
    def readEEPROM(self,filename):
        filename = c_wchar_p(filename)
        self.lib.bwtekReadEEPROMUSB(filename,self.channel)

    @Action()
    def testUSB(self):
        nTiming = c_int(1)
        nPixelNo = c_int(2048)
        nInputMode = c_int(1)
        return self.lib.bwtekTestUSB(nTiming,nPixelNo,nInputMode,self.channel)

    @Feat(units='ms', limits=(5, 65535))
    def integrationTime(self):
        return self.intTime

    @integrationTime.setter
    def integrationTime(self, time):
        time = c_long(int(time))  # Time in microseconds
        print(time.value)
        self.intTime = time.value*Q_('ms')
        self.lib.bwtekSetTimeUSB(time, self.channel)

    @Action()
    def close(self):
        self.lib.bwtekCloseUSB(self.channel)

if __name__ == '__main__':
    with spectrometer(0) as inst:
        inst.initDevice()
        inst.readEEPROM("test.dat")
        print('EEPROM read')
        print('Test USB: %s' % inst.testUSB())
        inst.integrationTime = 1*Q_('s')
        print(inst.integrationTime)
        inst.close()
