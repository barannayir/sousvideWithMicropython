import machine, onewire, ds18x20, time, ADC

sensor_pin = machine.Pin(4)
pot = ADC(Pin(34))
role = Pin(26, Pin.OUT)
disp_1 = Pin(16,Pin.OUT,value = 0)
disp_2 = Pin(17,Pin.OUT,value = 0)
role.value(1) #role kapalı


displaylist = [15,11,14,13,12,18,19]
displayled = []
for seg in displaylist:
    displayled.append(Pin(seg, Pin.OUT))

arrSeg = [[1,1,1,1,1,1,0],
          [0,1,1,0,0,0,0],
          [1,1,0,1,1,0,1],
          [1,1,1,1,0,0,1],
          [0,1,1,0,0,1,1],
          [1,0,1,1,0,1,1],
          [1,0,1,1,1,1,1],
          [1,1,1,0,0,0,0],
          [1,1,1,1,1,1,1],
          [1,1,1,1,0,1,1]]


pot.atten(ADC.ATTN_11DB)

sensor = ds18x20.DS18X20(onewire.OneWire(sensor_pin))
rom = sensor.scan()

tim0 = Timer(0)
def Dongu(tim0):
    sensor.convert_temp()
    sicaklik = sensor.read_temp(rom)
    istenenSicaklik = pot.read()
    map(istenenSicaklik, 0, 1023, 0, 99)
    DispYaz(istenenSicaklik)
    if istenenSicaklik >= (sicaklik-1):
        role.value(1) #röleyi kapat
    else:
        role.value(0) #röleyi aç

def map(x, i_m, i_M, o_m, o_M): #potansiyometreden gelen 0-1023 arası değeri 0-99 arasında mapleme
    return max(min(o_M, (x - i_m) * (o_M - o_m) // (i_M - i_m) + o_m), o_m)
     
def DispYaz(sayi):
    global rakam1, rakam2
    rakam1 = (sayi//10)%10
    rakam2 = sayi%10
    if sayi < 10:
        rakam1 = 0
        disp_1.on()
        for j in range(7):
            displayled[j].value(arrSeg[rakam1][j])
        time.sleep_ms(5)
        disp_1.off()
        disp_2.on()
        for k in range(7):
            displayled[k].value(arrSeg[rakam2][k])
        time.sleep_ms(5)  
        disp_2.off()  
    else:
        disp_1.on()
        for j in range(7):
            displayled[j].value(arrSeg[rakam1][j])
        time.sleep_ms(5)
        disp_1.off()
        disp_2.on()
        for k in range(7):
            displayled[k].value(arrSeg[rakam2][k])
        time.sleep_ms(5)  
        disp_2.off()  
        
        
    
tim0.init(period=500, mode=Timer.PERIODIC, callback=Dongu)
