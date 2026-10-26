from machine import Pin
import time, gc, machine
from nextion import NexText, NexHardware, NexNumber, NexPage, NexCheckbox

rt=machine.RTC()
nh = NexHardware(rx_pin=16, tx_pin=17)
#get page 1 
flsh=NexPage(nh, 0, 0, "flashscreen")
#get the time on page 1
thn=NexNumber(nh, 0, 9, "flashscreen.n1")
bln=NexNumber(nh, 0, 10, "flashscreen.n2")
tgl=NexNumber(nh, 0, 11, "flashscreen.n3")
jam=NexNumber(nh, 0, 12, "flashscreen.n4")
mnt=NexNumber(nh, 0, 13, "flashscreen.n5")
det=NexNumber(nh, 0, 14, "flashscreen.n6")
#get countdown
count=NexText(nh, 0, 30, "flashscreen.counter")
#getcombobox
Cbox=NexCheckbox(nh, 0, 29, "flashscreen.c0")
#get device mode
dvState=NexText(nh, 0, 7,"flashscreen.divmode")
#get menus` value 
#menu=NexNumber(nh, 0, 38,"flashscreen.menu")
#set esp32 time
rt.datetime((thn.getValue(), bln.getValue(), tgl.getValue(), jam.getValue(), mnt.getValue(), det.getValue(), 36, 5))


time.sleep(1)
pres2=Pin(34,Pin.IN)  #pin input for selector measure menu
time.sleep(1)
pressed=Pin(23,Pin.IN) #pin input for selector web
time.sleep(1)
flsh.show()

print(pressed.value(),pres2.value()) #debug
Cbox.setValue(1)
#menu.setValue(1)
time.sleep(0.5)
#option for measurement, basic, web
if pres2.value()==1 and pressed.value()==0: 
    print("pres2 ", pres2.value(),"Measurement")
    dvState.setText("Measurement Menu") 
    print("time", rt.datetime())
    gc.collect() 
    import measurestd11des 
    measurestd11des.main_menu()
     
elif pres2.value()==0 and pressed.value()==0:
    Cbox.setValue(0)
    print("pres2 ", pres2.value(),"pressed ", pressed.value(),"Basic")
    dvState.setText("Basic")
    time.sleep(10)
    gtx=dvState.getText()
    st=30
    while gtx!="Basic GO":
        for xCnt in range(st,-1,-1):
            count.setText(xCnt)
            gtx=dvState.getText()
            if gtx=="":
                gtx=dvState.getText()
                time.sleep(1)
            if gtx=="":
                gtx=dvState.getText()
                time.sleep(1)
            if gtx=="":
                gtx=dvState.getText()
                time.sleep(1)
            time.sleep(5)
            sCnr=count.getText()
            print("Counter -...- ",xCnt," alat ",sCnr)
            
            if gtx=="Basic GO" or xCnt==0:
                break
        
    import measurebasic21Des #measurement    
    measurebasic21Des.sensorBasic()
    
elif pressed.value()==1 and (pres2.value()==1 or pres2.value()==0):
    print("pressed ", pressed.value(),"Active Web")
    dvState.setText("Active Web")
    time.sleep(0.5)
    from web_download import web_download
    FileLog="/dt/Temp.csv"
    web_download(FileLog)
    time.sleep(1)
else:
    print("Try again")
    dvState.setText("Try Again")
    
time.sleep(1)
              
    
    