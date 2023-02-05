from database import methods
from tdamodule import tdamethods


def initialize():
    records = methods.getETF()
    for stock in records:
        tdamethods.initializeOptionData(stock['SYMBOLS'], stock['OptionSize'])

    stockrecords = methods.getStock()
    for stock in stockrecords:
        tdamethods.initializeOptionData(stock['SYMBOLS'], stock['OptionSize'])


initialize()
# methods.deleteALL("options")
