import board
import busio
import bitbangio
pins = (board.RX, board.TX, board.A3, board.A1, board.A2, board.A4)
for sck in pins:
    for mosi in pins:
        for miso in pins:

            if sck == mosi or sck == miso or mosi == miso:
                continue

            try:
                
                spi = bitbangio.SPI(clock=sck, MOSI=mosi, MISO=miso)
            except:
                print("FAILED: clock={}, mosi={}, miso={}".format(sck, mosi, miso))
                continue
            spi.deinit()
            print("Works: clock={}, mosi={}, miso={}".format(sck, mosi, miso))