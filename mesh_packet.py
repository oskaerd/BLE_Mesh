import random

''' Class for storing data received from gateway device. '''

NumberOfValues = 7

''' Converts received byte-like array to proper format dictionary '''
def listToDict( src ):
    ret_dict = {}

    ret_dict['opcode'] = src[0]
    ret_dict['dev_id'] = (src[1] << 8) + src[2]
    ret_dict['temperature'] = (src[3] << 8) + src[4]
    ret_dict['humidity'] = src[5]
    ret_dict['pressure'] = (src[6] << 24) + (src[7] << 16) + (src[8] << 8) + \
                            src[9]
    ret_dict['light'] = src[10]
    ret_dict['battery_voltage'] = src[11]

    return ret_dict


class meshPacket:
    ''' Takes dictionary of expected values '''
    def __init__(self, values):
        self.values = values
        self.populate_data(values)


    def populate_data(self, values):
        self.values = values
        self.opcode = values['opcode']
        self.id = values['dev_id']
        self.temperature = int(values['temperature'] * 1000)
        self.humidity = values['humidity']
        self.pressure = int(values['pressure'] * 100 )
        self.light = values['light']
        self.battery_voltage = values['battery_voltage']

    def updateValues(self):
        print('update')
        ret = meshPacketTestCase()
        ret.printValues()
        self.populate_data(ret.getRandomData())
        
        return ret.getRandomData()

    def printValues(self):
        for key in self.values:
            print( 'Key ' + str(key) + ' value ' + str( self.values[key] ) )

    def dictToBytesArray(self):
        bytes_array = []

        bytes_array.append( self.opcode ) # uint8_t 
        bytes_array.append( self.id >> 8) # uint16_t 
        bytes_array.append( self.id & 0xFF)
        bytes_array.append( self.temperature >> 8 ) # uint16_t
        bytes_array.append( (self.temperature & 0xFF )) # uint16_t
        bytes_array.append( self.humidity ) # uint8_t 
        bytes_array.append( (self.pressure & 0xFF000000 ) >> 24) # uint32_t
        bytes_array.append( (self.pressure & 0x00FF0000 ) >> 16)
        bytes_array.append( (self.pressure & 0x0000FF00 ) >> 8)
        bytes_array.append( (self.pressure & 0x000000FF ))
        bytes_array.append( self.light ) # uint16_t
        bytes_array.append( self.battery_voltage ) # uint8_t
        
        self.printValues()
        return bytes(bytes_array)


''' For generating dummy random data for test '''
class meshPacketTestCase:
    def __del__(self):
        print('deleting')

    def __init__(self):
        print('Creating...')
        random.seed()
        self.randomValues = {}
        # test for opcode
        self.randomValues['opcode'] = 0xB3
        # test device id
        self.randomValues['dev_id'] = 0xBEEF
        # append temperature 
        self.randomValues['temperature'] = 22 + 5*random.random()
        # append humidity
        self.randomValues['humidity'] = 40 + random.randint(0, 5)
        # append pressure
        self.randomValues[ 'pressure' ] = 1000 + 10 * random.random()
        # append lux
        self.randomValues[ 'light' ] = 50
        # append battery voltage times 10
        self.randomValues[ 'battery_voltage' ] = 33

    def printValues(self):
        for key in self.randomValues:
            print( 'Key ' + str(key) + ' value ' + str( self.randomValues[key] ) )

    def updateValues(self):
        random.seed()
        # update temperature 
        self.randomValues['temperature'] = 22 + 5*random.random()
        # update humidity
        self.randomValues['humidity'] = 40 + random.randint(0, 5)
        # update pressure
        self.randomValues[ 'pressure' ] = 1000 + 10 * random.random()

    def getRandomData(self):
        return self.randomValues
