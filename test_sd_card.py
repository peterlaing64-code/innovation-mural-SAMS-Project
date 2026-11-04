import board, busio, sdcardio, storage
spi = busio.SPI(board.A1, MOSI=board.A2, MISO=board.A3)
sd = sdcardio.SDCard(spi, board.A4) # A4 is chip select
storage.mount(storage.VfsFat(sd),"/sd")
with open("/sd/logs/hello.txt","w") as f: # quick test: write a file
    f.write("it works")