
""""
Thermaltest first written at 8 July 2024, last updated 24 Dec 2025
multiple detection initial, heating and peak
compiled with headache by Asep Yudi - asepyudi2016@gmail.com

HARDWARE;
esp32wroom, sensor 4 ds18b20, nextion intellegent 4.3", pcb,
micro sd card & shield, battery and charger + step up, pin headers,
JST 2.54 4/3/2pins & DC connectors, cables, soldering % tin
SOFTWARE;
Nextion IDE, Thonny IDE, Python - micropython, google email
LIBRARY;
machine, os, nextion, ds18x20, onewire, sdcard, umail, ssl (renamed to ussl)
network, time, ntptime
python -m esptool --chip esp32 erase_flash
desclaimer: library used all free on github or pyPi
Web connect

this is the code for BASIC selector 

"""

# system packages
import time, machine, os, onewire, ds18x20
#from datetime import datetime
import network, gc
global FileLog, FileRes, startStatus, judul, times, record
from nextion import NexText, NexHardware, NexWaveform,NexNumber, NexRtc, NexPage, NexButton, NexVariable
nh = NexHardware(rx_pin=16, tx_pin=17) #pin esp32 for nextion communication
nh.nexInit()                           #nextion comm started
flas=NexText(nh, 0, 23,"mcu") # test for initial device check
flas.show()
#IP=station.ifconfig()  # get ip of nextwork on boot.py
#flas.setText("IP "+ IP[0]) # write first IP on Nextion
time.sleep(2)              # gives time for humman eyes
gc.collect()
# sdcard check
try:
    print("Filesystem check ")
    lisfile=os.listdir("/dt")
    print("list file ",lisfile)
    if lisfile!=[]:
        flas.setText(lisfile[0]) # tell sd card ready
    time.sleep(2)
    
except OSError:
    print('file not detected')
    flas.setText('file not detected')

ds_pin = machine.Pin(4) #sensors pin esp32
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
roms = ds_sensor.scan()
ds_sensor.convert_temp()
sens=""
#added 25Dec25 number of sensor detected...
if len(roms)>1:
    print("sensor detected ", len(roms))
for g in roms:
    sens+=str(ds_sensor.read_temp(g)) +","
    
#samplename="Smp 1","Smp 2","Smp 3","Smp 4","Smp 5","Smp 6"
title=["Elapse","1","2","3","4","5","6"]
FileFin="/dt/ThermalX.csv"
FileLog="/dt/Temp.csv"
FileRes="/dt/Result.csv"
FileWifi="/dt/wifisetup.txt"
FileName="/dt/filename.txt"

Elapse=[0,0,0,0,0,0]
startTest=["","","","","",""]
red=63450
grn=22500
yel=65500
wht=65535
mag=63520
# print(samplename[3], title[0])

flsh=NexPage(nh, 0, 0, "flashscreen")
smpl=NexPage(nh, 1, 0, "samples")
test=NexPage(nh, 2, 0, "test")
kald=NexPage(nh, 3, 0, "setDate")
resul=NexPage(nh, 6, 0, "Result")
testBasic=NexPage(nh, 10, 0, "test_basic")

started1=False
started2=False
started3=False
started4=False
started5=False
started6=False

pgs=2
time.sleep(0.5)
wv = NexWaveform(nh, pgs, 1,"s0")

flas.setText("sensor 1 "+sens[0:5]) #tell sensors reading ready
time.sleep(2)
pgx=10
thn=NexNumber(nh, pgx, 12, "test_basic.n0")
bln=NexNumber(nh, pgx, 13, "test_basic.n1")
tgl=NexNumber(nh, pgx, 14, "test_basic.n2")
jam=NexNumber(nh, pgx, 15, "test_basic.n3")
mnt=NexNumber(nh, pgx, 16, "test_basic.n4")

Bdisp1=NexText(nh, pgx,59,"test_basic.smp1")
Bdisp2=NexText(nh, pgx,4, "test_basic.smp2")
Bdisp3=NexText(nh, pgx,5, "test_basic.smp3")
Bdisp4=NexText(nh, pgx,65, "test_basic.smp4")
Bdisp5=NexText(nh, pgx,102, "test_basic.smp5")
Bdisp6=NexText(nh, pgx,103, "test_basic.smp6")

Bx1=NexNumber(nh,pgx,6, "test_basic.x0")
Bx2=NexNumber(nh,pgx,7, "test_basic.x1")
Bx3=NexNumber(nh,pgx,8, "test_basic.x2")
Bx4=NexNumber(nh,pgx,106,"test_basic.x3")
Bx5=NexNumber(nh,pgx,104,"test_basic.x4")
Bx6=NexNumber(nh,pgx,105,"test_basic.x5")

cmpltd1=NexText(nh,pgx, 109, "test_basic.complt1")
cmpltd2=NexText(nh,pgx, 110, "test_basic.complt2")
cmpltd3=NexText(nh,pgx, 111, "test_basic.complt3")
cmpltd4=NexText(nh,pgx, 112, "test_basic.complt4")
cmpltd5=NexText(nh,pgx, 113, "test_basic.complt5")
cmpltd6=NexText(nh,pgx, 114, "test_basic.complt6")

smpname1=NexText(nh,pgx, 109, "test_basic.smpname1")
smpname2=NexText(nh,pgx, 110, "test_basic.smpname2")
smpname3=NexText(nh,pgx, 111, "test_basic.smpname3")
smpname4=NexText(nh,pgx, 112, "test_basic.smpname4")
smpname5=NexText(nh,pgx, 113, "test_basic.smpname5")
smpname6=NexText(nh,pgx, 114, "test_basic.smpname6")
testBack=NexVariable(nh,pgx, 62,"test_basic.testBack")

pgNo=1

gOrder = NexText(nh, pgNo, 74,"samples.komando")

ordTest=NexText(nh, 2, 65,"test.actTest") 
mcuEls1=NexText(nh, 2, 3, "test.els1")
dispEls=NexText(nh, 2, 59,"test.elaps")

#BordTest=NexText(nh, 2, 93,"test_basic.actTest")
BmcuEls1=NexText(nh, 2, 3 ,"test_basic.els1")   #disp elaps
BdispEls=NexText(nh, 2, 58,"test_basic.elaps")
#mcuEls2=NexText(nh, 10, 3,"test2.els1") test_basic


#ordTest2=NexText(nh, 10, 77,"test2.actTest")
ordLizt=NexText(nh, 6, 16,"list.listProg")
#mcuEls1.setText("")
#BmcuEls1.setText("")
#mcuEls2.setText("") 

status=NexNumber(nh,0,30,"flashscreen.testStatus")
runFlas=NexText(nh, 0, 29, "flashscreen.run")
sensTx=NexText(nh, 0, 40, "flashscreen.sens")
fileSt=NexText(nh, 0, 31,"flashscreen.neofile")
sensTx.setText(len(roms))
runSmpl=NexText(nh, 1, 77, "samples.run")
runTest=NexText(nh, 2, 76, "test.run")

pgr=9
inTemp1=NexText(nh,pgr,7, "Result.inTemp1")
inTemp2=NexText(nh,pgr,8, "Result.inTemp2")
inTemp3=NexText(nh,pgr,9, "Result.inTemp3")
inTemp4=NexText(nh,pgr,10,"Result.inTemp4")
inTemp5=NexText(nh,pgr,55,"Result.inTemp5")
inTemp6=NexText(nh,pgr,65,"Result.inTemp6")

pkTemp1=NexText(nh,pgr,12, "Result.pkTemp1")
pkTemp2=NexText(nh,pgr,13, "Result.pkTemp2")
pkTemp3=NexText(nh,pgr,14, "Result.pkTemp3")
pkTemp4=NexText(nh,pgr,15, "Result.pkTemp4")
pkTemp5=NexText(nh,pgr,56, "Result.pkTemp5")
pkTemp6=NexText(nh,pgr,66, "Result.pkTemp6")

pkTime1=NexText(nh,pgr,17, "Result.pkTime1")
pkTime2=NexText(nh,pgr,18, "Result.pkTime2")
pkTime3=NexText(nh,pgr,19, "Result.pkTime3")
pkTime4=NexText(nh,pgr,20, "Result.pkTime4")
pkTime5=NexText(nh,pgr,57, "Result.pkTime5")
pkTime6=NexText(nh,pgr,67, "Result.pkTime6")

setIni1=NexText(nh,pgr,22, "Result.setIni1")
setIni2=NexText(nh,pgr,23, "Result.setIni2")
setIni3=NexText(nh,pgr,24, "Result.setIni3")
setIni4=NexText(nh,pgr,25, "Result.setIni4")
setIni5=NexText(nh,pgr,58, "Result.setIni5")
setIni6=NexText(nh,pgr,68, "Result.setIni6")

setFin1=NexText(nh,pgr,27, "Result.setFin1")
setFin2=NexText(nh,pgr,28, "Result.setFin2")
setFin3=NexText(nh,pgr,29, "Result.setFin3")
setFin4=NexText(nh,pgr,30, "Result.setFin4")
setFin5=NexText(nh,pgr,59, "Result.setFin5")
setFin6=NexText(nh,pgr,69, "Result.setFin6")

calor1=NexText(nh,pgr,32, "Result.calor1")
calor2=NexText(nh,pgr,33, "Result.calor2")
calor3=NexText(nh,pgr,34, "Result.calor3")
calor4=NexText(nh,pgr,35, "Result.calor4")
calor5=NexText(nh,pgr,60, "Result.calor5")
calor6=NexText(nh,pgr,70, "Result.calor6")

str1d1=NexText(nh,pgr,38, "Result.str1d1")
str1d2=NexText(nh,pgr,39, "Result.str1d2")
str1d3=NexText(nh,pgr,40, "Result.str1d3")
str1d4=NexText(nh,pgr,41, "Result.str1d4")    
str1d5=NexText(nh,pgr,61, "Result.str1d5")
str1d6=NexText(nh,pgr,71, "Result.str1d6")

str3d1=NexText(nh,pgr,42, "Result.str3d1")
str3d2=NexText(nh,pgr,43, "Result.str3d2")
str3d3=NexText(nh,pgr,44, "Result.str3d3")
str3d4=NexText(nh,pgr,45, "Result.str3d4")
str3d5=NexText(nh,pgr,62, "Result.str3d5")
str3d6=NexText(nh,pgr,72, "Result.str3d6")

str28d1=NexText(nh,pgr,47, "Result.str28d1")
str28d2=NexText(nh,pgr,48, "Result.str28d2")
str28d3=NexText(nh,pgr,49, "Result.str28d3")
str28d4=NexText(nh,pgr,50, "Result.str28d4")
str28d5=NexText(nh,pgr,63, "Result.str28d5")
str28d6=NexText(nh,pgr,73, "Result.str28d6")

flas.setText("Device Ready...")
time.sleep(1)

def statusTest(stat):
    status.setValue(stat)

#create file log
def createLog(fn,mess):
    try:	
        with open(fn, "w") as f:
            g = f.write(mess)
            time.sleep(0.2)
        return "done"    
    except OSError as er:
        print(er)
        return "fail"
    finally:
        # Make sure the file gets closed
        if 'file' in locals() and not f.closed:
            f.close()
#write log
def writeLog(fns,shorts)->str:
    try:
        with open(fns, "a") as fs:
            n = fs.write(shorts)
            time.sleep(0.2)

        return "done"
    except OSError as er:
        #print(er)
        return "fail"
        
def ifexist(ff):
    try:
        fi=os.stat(ff)[6]
        #print("exist", fi)
        os.remove(ff)
        time.sleep(0.5)
        return "exist"
    
    except OSError as er:
        print(er)

def sorter(samplelist,sampleoutlist, valuelist,outputlist):
    pj=len(samplelist)
    lv=100
    hv=0
    for i in range(0,pj):
        if valuelist[i]>hv:
            hv=valuelist[i]
            outputlist[i]=valuelist[i]
            sampleoutlist[i]=samplelist[i]
    return outputlist,sampleoutlist

def xTime(inTime):
    tm=time.localtime(inTime)
    jam=tm[4]*60+tm[5]
    return jam

def getTgl()->str:
    thx=thn.getValue()
    time.sleep_ms(25)
    blx=bln.getValue()
    time.sleep_ms(25)
    tgx=tgl.getValue()
    time.sleep_ms(25)
    jax=jam.getValue()
    time.sleep_ms(25)
    mnx=mnt.getValue()
    time.sleep_ms(25)
    TGL=str(thx)+"-"+str(blx)+"-"+str(tgx)+" "+str(jax)+":"+str(mnx)
    return TGL

def printTime(inpTime):
    tm=time.localtime(inpTime)
    return str(tm[3])+":"+str(tm[4])+":"+str(tm[5])

def calcSetting(peakTime):
    if peakTime>0:
        initial=int(peakTime*0.3)
        finales=int(peakTime*0.62)
    else:
        initial=1
        finales=1
        
    return initial, finales

def calcHeatCap(initTemp, pkTime, peakTemp):
    if pkTime>0:
        calr = int((peakTemp-initTemp)*1000/pkTime) 
        heatcp = 0.5*(peakTemp-initTemp)/pkTime
    else:
        calr=1
        heatcp=1
    return calr, heatcp

def str28Cool(inTemp,pkTemp,pkTime,clTemp,clTime):
    if pkTime>0:
        hitCp = 0.5*(pkTemp-inTemp)/pkTime
        st3d=(hitCp/41+10*hitCp/pkTime)/1.4
        kulrate =0.5 * (pkTemp-clTemp) * (clTime-pkTime)
        str28Kul=int(st3d+kulrate/(kulrate/(clTime-pkTime)))
    else:
        str28Kul=1
    return str28Kul

def strength(heatcap,pkTime):
    if pkTime>0:
        str1d= int((heatcap/41+10*heatcap/pkTime)/2)
        str3d= int(str1d*2/1.4)
        str28= int(str1d+str3d)
    else:
        str1d=1 
        str3d=1 
        str28=1        
    return str1d,str3d, str28

def dispInit(idVal,initVal):
    tx="init "+str(idVal)
    if idVal==0:
        inTemp1.setText(initVal)
        time.sleep(0.2)
        cmpltd1.setText(tx)
        time.sleep(0.2)
    if idVal==1:
        inTemp2.setText(initVal)
        time.sleep(0.2)
        cmpltd2.setText(tx)
        time.sleep(0.2)
    if idVal==2:
        inTemp3.setText(initVal)
        time.sleep(0.2)
        cmpltd3.setText(tx)
        time.sleep(0.2)
    if idVal==3:
        inTemp4.setText(initVal)
        time.sleep(0.2)
        cmpltd4.setText(tx)
        time.sleep(0.2)
    if idVal==4:
        inTemp5.setText(initVal)
        time.sleep(0.2)
        cmpltd5.setText(tx)
        time.sleep(0.2)
    if idVal==5:
        inTemp6.setText(initVal)
        time.sleep(0.2)
        cmpltd6.setText(tx)
        time.sleep(0.2)

def dispPeak(idVal,peakVal,peakTime,initial,final,Kalor,str1,str3,str28):
    tx="peak "+str(idVal)
    if idVal==0:
        pkTemp1.setText(peakVal)
        time.sleep(0.2)
        pkTime1.setText(peakTime)
        time.sleep(0.2)
        setIni1.setText(initial)
        time.sleep(0.2)
        setFin1.setText(final)
        time.sleep(0.2)
        calor1.setText(Kalor)
        time.sleep(0.2)
        str1d1.setText(str1)
        time.sleep(0.2)
        str3d1.setText(str3)
        time.sleep(0.2)
        str28d1.setText(str28)
        time.sleep(0.2)
        cmpltd1.setText(tx)
        time.sleep(0.2)

    if idVal==1:
        pkTemp2.setText(peakVal)
        time.sleep(0.2)
        pkTime2.setText(peakTime)
        time.sleep(0.2)
        setIni2.setText(initial)
        time.sleep(0.2)
        setFin2.setText(final)
        time.sleep(0.2)
        calor2.setText(Kalor)
        time.sleep(0.2)
        str1d2.setText(str1)
        time.sleep(0.2)
        str3d2.setText(str3)
        time.sleep(0.2)
        str28d2.setText(str28)
        time.sleep(0.2)
        cmpltd2.setText(tx)
        time.sleep(0.2)

    if idVal==2:
        pkTemp3.setText(peakVal)
        time.sleep(0.2)
        pkTime3.setText(peakTime)
        time.sleep(0.2)
        setIni3.setText(initial)
        time.sleep(0.2)
        setFin3.setText(final)
        time.sleep(0.2)
        calor3.setText(Kalor)
        time.sleep(0.2)
        str1d3.setText(str1)
        time.sleep(0.2)
        str3d3.setText(str3)
        time.sleep(0.2)
        str28d3.setText(str28)
        time.sleep(0.2)
        cmpltd3.setText(tx)
        time.sleep(0.2)

    if idVal==3:
        pkTemp4.setText(peakVal)
        time.sleep(0.2)
        pkTime4.setText(peakTime)
        time.sleep(0.2)
        setIni4.setText(initial)
        time.sleep(0.2)
        setFin4.setText(final)
        time.sleep(0.2)
        calor4.setText(Kalor)
        time.sleep(0.2)
        str1d4.setText(str1)
        time.sleep(0.2)
        str3d4.setText(str3)
        time.sleep(0.2)
        str28d4.setText(str28)
        time.sleep(0.2)
        cmpltd4.setText(tx)
        time.sleep(0.2)

    if idVal==4:
        pkTemp5.setText(peakVal)
        time.sleep(0.2)
        pkTime5.setText(peakTime)
        time.sleep(0.2)
        setIni5.setText(initial)
        time.sleep(0.2)
        setFin5.setText(final)
        time.sleep(0.2)
        calor5.setText(Kalor)
        time.sleep(0.2)
        str1d5.setText(str1)
        time.sleep(0.2)
        str3d5.setText(str3)
        time.sleep(0.2)
        str28d5.setText(str28)
        time.sleep(0.2)
        cmpltd5.setText(tx)
        time.sleep(0.2)

    if idVal==5:
        pkTemp6.setText(peakVal)
        time.sleep(0.2)
        pkTime6.setText(peakTime)
        time.sleep(0.2)
        setIni6.setText(initial)
        time.sleep(0.2)
        setFin6.setText(final)
        time.sleep(0.2)
        calor6.setText(Kalor)
        time.sleep(0.2)
        str1d6.setText(str1)
        time.sleep(0.2)
        str3d6.setText(str3)
        time.sleep(0.2)
        str28d6.setText(str28)
        time.sleep(0.2)
        cmpltd6.setText(tx)
        time.sleep(0.2)


def dispCool(idVal,cooVal):
    tx="cool "+str(idVal)
    if idVal==0:
        cmpltd1.setText(tx)
        time.sleep(0.2)
        str28d1.setText(cooVal)
        time.sleep(0.2)

    if idVal==1:
        cmpltd2.setText(tx)
        time.sleep(0.2)
        str28d2.setText(cooVal)
        time.sleep(0.2)

    if idVal==2:
        cmpltd3.setText(tx)
        time.sleep(0.2)
        str28d3.setText(cooVal)
        time.sleep(0.2)

    if idVal==3:
        cmpltd4.setText(tx)
        time.sleep(0.2)
        str28d4.setText(cooVal)
        time.sleep(0.2)

    if idVal==4:
        cmpltd5.setText(tx)
        time.sleep(0.2)
        str28d5.setText(cooVal)
        time.sleep(0.2)

    if idVal==5:
        cmpltd6.setText(tx)
        time.sleep(0.2)
        str28d6.setText(cooVal)
        time.sleep(0.2)

def checksystem():
    Chklst=""
    def getSD():
        try:
        #print("SD card Filesystem check")
            os.listdir("/dt")
            print("sd card stat",jk)
            if jk==None:
                return "ok"
            else:
                return "no sd card"

        except OSError:
            print('card not detected')
            
    def getReading():
        vi=[0,0,0,0,0,0]
        lz=0
        try:
            sdSTR=""
            for rom in roms:
                vi[lz]=ds_sensor.read_temp(rom)
                if vi[lz]>0:
                    lz+=1
                    time.sleep_ms(300)
            return lz
        except OSError:
            print('sensor unplugged ')
            return 'sensor unplugged'
        
    chck=NexText(nh, 0, 26,"checklist")
    senNomre=getReading()
    chSd=getSD()
    if station.active(True):
        ChkLst="WiFi : Ok "+ "\r\n"
    else :
        ChkLst="WiFi : Not Ok "+ "\r\n"
    station.active(False)
    Chklst+="Display ; OK "+"\r\n"
    Chklst+=" Sensor ; "+ str(senNomre) +"\r\n"
    Chklst+=" sd card ; " + str(chSd) +"\r\n"
    chck.setText(Chklst)
    time.sleep(0.2)
    if senNomre>0 and chSd=="ok":
        return "ok"

def getsamplesready():
    statusTest(2)
    runSmpl.Set_background_color_bco(0)
    opss=NexText(nh,1,81,"samples.neofile")
    print("get list of samples, time prepared and save")
    ordLizt.setText("prepare..")

    judul="x"
    times=""
    record=""
    startStatus=""
    ngelay=0.35
    time.sleep(ngelay)
    statusTest(2)
        
    runSmpl.Set_background_color_bco(yel)

    judul="Elapse, unit,"+getSampleName()+"\n"
    times="start time, "+getStartTime()+"\n"
    time.sleep(0.2)
    statusTest(2)
    record="rec time, "+getRecTime()+"\n"
    time.sleep(0.2)
    startStatus="sample state "+getStat()+"\n"
    time.sleep(0.2)        
    print("Judul ", judul)   

    time.sleep(3)
    print(times)
    print(record)
    print(startStatus)
    
    statusTest(2)
    opsi=opss.getText()
    if opsi=="New File":
        resp=""
        resp=ifexist(FileLog)
        if resp=="exist":
            createLog(FileLog, judul)
            
        resR=""
        resR=ifexist(FileRes)
        if resR=="exist":
            createLog(FileRes, judul)
            
        resF=""
        resF=ifexist(FileFin)
        if resF=="exist":
            createLog(FileFin, judul)
        time.sleep(0.1)
        
        runSmpl.Set_background_color_bco(0)
        time.sleep(0.1)
        
    writeLog(FileLog, judul)
    time.sleep(0.5)
    writeLog(FileLog,times)
    runSmpl.Set_background_color_bco(yel)
    time.sleep(0.05)
    writeLog(FileLog,record)
    gOrder.setText("Files saved!")
    time.sleep(2)    
    ordLizt.setText("files saved...")
    time.sleep(0.5)
    lizt.show()

def getBSampleName()->str:
      
    #trial this one, check 24Dec25
    sample1=""
    while sample1=="" or sample1==None:
        sample1=smpname1.getText()
        time.sleep(0.05)

    sample2=""
    while sample2=="" or sample2==None:
        sample2=smpname2.getText()
        time.sleep(0.05)
        
    sample3=""
    while sample3=="" or sample3==None:
        sample3=smpname3.getText()
        time.sleep(0.05)
        
    sample4=""
    while sample4=="" or sample4==None:
        sample4=smpname4.getText()
        time.sleep(0.05)

    sample5=""
    while sample5=="" or sample5==None:
        sample5=smpname5.getText()
        time.sleep(0.05)
        
    sample6=""
    while sample6=="" or sample6==None:
        sample6=smpname6.getText()
        time.sleep(0.05)
                
    smpname=sample1 +","+ sample2 +","+ sample3 +","+ sample4 +","+ sample5 +","+ sample6
    return smpname  #, listSample


def main_menu():
    zOrder=""   
    while True:
        statusTest(0)
        zOrder=gOrder.getText()
        print("zOrder", zOrder)
    
        if zOrder=="mcu-reset": #page 0 button reset
        #sld=0
            flas.setText("mcu-reset done")
            time.sleep(0.2)
            gOrder.setText("mcu-reset done")
            time.sleep(0.2)
            machine.reset()
        
        elif zOrder=="check system":
            sis=checksystem()
            time.sleep(0.2)
            if sis=="ok":
                flas.setText("System check Ok")
                gOrder.setText("Initial")
                time.sleep(0.2)

            elif zOrder=="reset display":
                print("display reset")
                gOrder.setText("reset done")      
                time.sleep(0.2)
        
        elif zOrder=="Initial":
            statusTest(0)
            smpl.show()
            time.sleep(0.3)
            gOrder.setText("Initialized")
            stSmpl=NexText(nh,1,79,"samples.run")
            stSmpl.Set_background_color_bco(red)
            time.sleep(0.2)
            stSmpl.Set_background_color_bco(0)
            time.sleep(0.2)           
            
        elif zOrder=="sample save":
            time.sleep(0.2)
            getsamplesready()
            gOrder.setText("files saved")
        
        elif zOrder=="back sample":
            smpl.show()
            time.sleep(0.2)
            gOrder.setText("samples...")
                   
        elif zOrder== "files":
            time.sleep(0.2)
            files.show()
            gOrder.setText("page file")
        
        elif zOrder== "set date":
            time.sleep(0.2)
            kald.show()
            gOrder.setText("setting date")
        
        elif zOrder== "back list":
            lizt.show()
            time.sleep(0.2)
            gOrder.setText("back log")
        
        elif zOrder== "get content":
        #files.show()
            getFileContent(FileLog)
            gOrder.setText("get")
        
        elif zOrder== "get result":
        #files.show()
            getFileContent(FileRes)
            gOrder.setText("get")

        elif zOrder== "delete content":
        #files.show()
            time.sleep(1)
            gOrder.setText("del")
        #gOrder.setText("")

        elif zOrder== "save date":
            kald.show()
            gOrder.setText("date saved")
        
        elif zOrder== "get date":
            kald.show()
            time.sleep(1)
            gOrder.setText("getting date")
               
        elif zOrder== "testing":
            #ordLizt.setText("test on going")
            time.sleep(1)
            gOrder.setText("....")
            sensorReading()
            test.show()
            #break
      
        elif zOrder=="abort":
            flsh.show()
        #    time.sleep(1)
        #    gOrder.setText("aborting...")
        elif zOrder=="tabel":
            #getTabel()
            time.sleep(1)
            gOrder.setText("show table")
    
        elif zOrder=="get time":
            getTimefromNetwork()
            gOrder.setText("get network time")
        
        else:
            print("no order -> click to start")
        
        time.sleep(0.5)   
    
def sensorBasic():
    gtx=fileSt.getText()
    time.sleep(0.2)
    
    testBasic.show()
    time.sleep(0.2)
    runTest.Set_background_color_bco(0)
    tex=["","","","","",""]
    
    vi =[0,0,0,0,0,0]
    v0 =[0,0,0,0,0,0]
    dix=[0.00,0.00,0.00,0.00,0.00,0.00]
    dif=[0.00,0.00,0.00,0.00,0.00,0.00]
    
    ini=[0,0,0,0,0,0]  # initial temporary temperature 
    iti=[0,0,0,0,0,0]  # initial time
    itm=[0,0,0,0,0,0]  # initial temperature
    itt=[0,0,0,0,0,0]  # initial temporary time
    
    cmm=[0,0,0,0,0,0]  # cooling temporary temperature
    ctm=[0,0,0,0,0,0]  # cooling temperature
    ctt=[0,0,0,0,0,0]  # cooling temporary time
    cti=[0,0,0,0,0,0]  # cooling time 

    htm=[0,0,0,0,0,0]  # start heating temperature
    hti=[0,0,0,0,0,0]  # start heating time 
    htt=[0,0,0,0,0,0]  # start heating temporary time

    ptm=[0,0,0,0,0,0]  # peak temperature
    ptt=[0,0,0,0,0,0]  # peak temporary time
    pti=[0,0,0,0,0,0]  # peak time
    mx =[0,0,0,0,0,0]  # temporary max temperature
    Npk=[0,0,0,0,0,0]  # some peak
    
    setini =[0,0,0,0,0,0]
    setfin =[0,0,0,0,0,0]
    calor  =[0,0,0,0,0,0]
    heat_rt=[0,0,0,0,0,0]
    cool_rt=[0,0,0,0,0,0]
    str1d  =[0,0,0,0,0,0]
    str3d  =[0,0,0,0,0,0]
    str28d =[0,0,0,0,0,0]
    str28x =[0,0,0,0,0,0]
    
    iTr=[False, False, False, False, False, False] # inital true
    pTr=[False, False, False, False, False, False] # peak true
    cTr=[False, False, False, False, False, False] # cooling true
    hTr=[False, False, False, False, False, False] # heating true 
    u=0
    Display_elapse=BdispEls.getText()
    sStep=1
    init=0
    heat=0
    peak=0
    cool=0
    cmplt=0
    xDelay=3
    xSleep=xDelay # sleep for x, x=5 -> 3
    xRange=20*60*60/xSleep
    peakWrite=False
    heatWrite=False
    judul=getBSampleName()+"\n"
    st_init="Initial temp, oC,"
    st_tini="Initial time, min,"
    st_pktm="peak temp, oC,"
    st_pkti="peak time, min,"
    st_stin="setting initial, min,"
    st_stfn="setting final, min,"
    st_calr="calor, cal/g,"
    st_str1="str 1 day, kg/cm2,"
    st_str3="str 3 days, kg/cm2,"
    st_str28="str 28 days, kg/cm2,"
    st_str28x="str 28x days, kg/cm2,"
    
    testBack.setValue(1)
    if gtx=="New File":
        os.remove(FileLog)
        createLog(FileLog, judul)
        time.sleep(0.2)
        
    #get elapse time from display in case continueing the test
    if Display_elapse!="":
        elaps=int(Display_elapse)
    else:
        elaps=0
        
    #ensure the sensors reading the temp - working correctly
    for y in range(0,2):
        sStr0=""
        d=0
        for rom in roms:
            v0[d]=ds_sensor.read_temp(rom)
            sStr0 += str(v0[d]) +","
            ini[d]=v0[d]
            d+=1
            time.sleep(0.2)
        print("reading to avoid value -127 and 85", sStr0)

    a=0
    #if len(v0[a])>0 ->  to avoid error also use 'try' and 'error' trap
    can1=round(float(v0[a])*24/10,0) #round is newly added 2 jul
    Bx1.setValue(can1)
    time.sleep(0.2)
    dix[a]=round(v0[a],2)
    Bdisp1.setText(str(dix[a]))
    time.sleep(0.2)
    
    a=1
    can2=float(v0[a])*24/10
    Bx2.setValue(can2)
    time.sleep(0.2)
    dix[a]=round(v0[a],2)
    Bdisp2.setText(str(dix[a]))
    time.sleep(0.2)

    a=2
    can3=float(v0[a])*24/10
    Bx3.setValue(can3)
    time.sleep(0.2)
    dix[a]=round(v0[a],2)
    Bdisp3.setText(str(dix[a]))
    time.sleep(0.2)

    a=3
    can4=float(v0[a])*24/10
    Bx4.setValue(can4)
    time.sleep(0.2)
    dix[a]=round(v0[a],2)
    Bdisp4.setText(str(dix[a]))
    time.sleep(0.2)

    a=4
    can5=float(v0[a])*24/10
    Bx5.setValue(can5)
    time.sleep(0.2)
    dix[a]=round(v0[a],2)
    Bdisp5.setText(str(dix[a]))
    time.sleep(0.2)

    a=5
    can6=float(v0[a])*24/10
    Bx6.setValue(can6)
    time.sleep(0.2)
    dix[a]=round(v0[a],2)
    Bdisp6.setText(str(dix[a]))
    time.sleep(0.2)
    
    mcuEls1.setText(elaps)
    time.sleep(0.2)

    lapTime=0
    sorte=[]
    namafiles=getBSampleName()+"\n"
    print("Sample names ;", namafiles)
    testBack.setValue(0)
    
    while elaps<xRange :
        NOW=time.time()
        tglx=getTgl()
        lapTime=printTime(NOW)
        runTest.Set_background_color_bco(mag)           
        BmcuEls1.setText(elaps)
        time.sleep(0.2)
        dStr=lapTime+","+str(elaps)+","
        ds_sensor.convert_temp()       # must in loop       
        strSave=""
        sdSTR=lapTime+","+str(elaps)+","
        lz=0

        for rom in roms:
            vi[lz]=ds_sensor.read_temp(rom)
            if lapTime==0 :
                ini[lz]=vi[lz]
                stSens=writeLog(FileLog,namafiles)
            if vi[lz]>0 and vi[lz]!=85:
                sdSTR += str(vi[lz]) +","
                dif[y]=vi[lz]-v0[lz]
                
                #lowest temp
                if elaps>=10 and iTr[lz]==False:
                    if vi[lz] <= ini[lz]:
                        ini[lz]= vi[lz]
                        iti[lz]= elaps
                    #detect if decreasing or increase    
                    if (ini[lz] - vi[lz]>0.1 or vi[lz]-ini[lz])<0.1 and iTr[lz]==False: #swapped
                        itm[lz] = ini[lz]
                        itt[lz] = iti[lz]
                        htm[lz] = ini[lz] #carry over value to detect heating
                        #added 22 Dec 25
                        dispInit(lz,ini[lz])
                        init+=1
                        iTr[lz] = True
                #if there is low temp after lowest recorded
                if iTr[lz]==True and vi[lz]<ini[lz] and pTr[lz]==False:
                    ini[lz] = vi[lz]
                    itm[lz] = ini[lz]
                    itt[lz] = elaps
                    dispInit(lz,ini[lz])
                if  ini[lz]==0 :
                    ini[lz] = vi[lz]
                    itm[lz] = ini[lz]
                    itt[lz] = elaps
                    dispInit(lz,ini[lz])
                
                #heating        
                if elaps>=20 and hTr[lz]==False and iTr[lz]==True: 
                    if vi[lz]>htm[lz]: #replace
                        htm[lz] = vi[lz]
                    # if current value higher than last value  
                    if (dif[y]>0.2 or dif[y]<=0.5)  and hTr[lz]==False:
                        htt[lz] = htm[lz]
                        hti[lz] = elaps
                        mx[lz]  = htm[lz] #carry over value to detect peak temp
                        #added 22 Dec 25
                        heat+=1
                        hTr[lz]=True
                        
                #added 23Dec2025 to avoid zero at htt[lz]        
                if htt[lz]==0 :
                    htt[lz]=vi[lz]
                    hti[lz]=elaps
                    
                #peak temp     
                if elaps>=40 and pTr[lz]==False:
                    if vi[lz]>mx[lz]:
                        mx[lz]  = vi[lz]
                        ptt[lz] = elaps
                    #if vi[lz]/ini[lz]>1.3:    
                    if mx[lz]-vi[lz]>0.2 and pTr[lz]==False: 
                        pTr[lz] = True
                        pti[lz] = ptt[lz]
                        ptm[lz] = mx[lz]
                        cmm[lz] = mx[lz] #carry over value to detect cooling temp
                        peak+=1
                        Npk[lz]+=1
                        if pti[lz]==0:
                            pti[lz]=10                        
                        print("reach d' peak ", lz, " ", mx[lz], " time ", pti[lz])
                        #tex[y]="ini-heat-peak"
                        setini[lz],setfin[lz]=calcSetting(pti[lz])
                        calor[lz],heat_rt[lz] = calcHeatCap(itm[lz],pti[lz],ptm[lz])
                        str1d[lz],str3d[lz],str28d[lz]=strength(heat_rt[lz],pti[lz])

                        dispPeak(lz, ptm[lz], pti[lz], setini[lz], setfin[lz], calor[lz], str1d[lz], str3d[lz], str28d[lz])
                
                #added 23Dec2025 to avoid zero at ptm[lz]
                if ptm[lz]==0 and hTr[lz]==True:
                    ptm[lz]=vi[lz]
                    pti[lz]=elaps
                    Npk[lz]+=1
                    calor[lz],heat_rt[lz] = calcHeatCap(itm[lz],pti[lz],ptm[lz])
                    str1d[lz],str3d[lz],str28d[lz]=strength(heat_rt[lz],pti[lz])
                    dispPeak(lz, ptm[lz], pti[lz], setini[lz], setfin[lz], calor[lz], str1d[lz], str3d[lz], str28d[lz])
                    
                if vi[lz]>ptm[lz] and pTr[lz]==True:
                    ptm[lz]=vi[lz]
                    pti[lz]=elaps
                    Npk[lz]+=1
                    calor[lz],heat_rt[lz] = calcHeatCap(itm[lz],pti[lz],ptm[lz])
                    str1d[lz],str3d[lz],str28d[lz]=strength(heat_rt[lz],pti[lz])
                    dispPeak(lz, ptm[lz], pti[lz], setini[lz], setfin[lz], calor[lz], str1d[lz], str3d[lz], str28d[lz])
                    
                #26des25 -> less than 1.25-1.5 (1.3) of (peaktemp[lz]-initTemp[lz])/(peakTemp[lz]-vi[lz])    
                #if vi[lz]/ini[lz]>1.2: check historical data long recorded    
                if elaps > pti[lz] + 50 and cTr[lz]== False : # and cTr[y]==False
                    print("looking for cooling temp \n delta v0-v1 ~ ",lz+1, " ", dif[lz], "\n peak temp ", cmm[lz], "\n current val ", vi[lz] )
                    ctt[lz]=elaps
                    cmm[lz]=vi[lz]
                    dif[lz]=v0[lz]-vi[lz]
                    
                    #cooling happened
                    if cTr[lz] == False and abs(dif[lz])<=0.2 :
                        ctm[lz] = cmm[lz]
                        cti[lz] = ctt[lz]
                        cool+=1
                        print("cooling flatten ", lz, " ", ctm[lz], " time ", cti[lz])
                        if cti[lz]==0:
                            cti[lz]=1
                        str28x[lz] = str28Cool(itt[lz],ptm[lz],pti[lz],ctm[lz],cti[lz])
                        cTr[lz] = True
                        dispCool(lz, str28x[lz])
                        
                # added 25dec25, mitigate of early cooling
                #                due to flat temp before peak  
                if cTr[lz] == True and pTr[lz] == True and (cti[lz]<=pti[lz] or ctm[lz]>ptm[lz]):
                    cTr[lz] = False
                    
                if init==6 :
                    cmplt=1
                if heat==6 :
                    cmplt=2
                if peak==6 :
                    cmplt=3
                if cool==6 :
                    cmplt=4        
            else:
                sdSTR += ",,"
            time.sleep_ms(300)
            lz+=1
        
        # reactivate 14-Dec-25
        strSave=sdSTR[0:-1]+"\n"
        stSens=writeLog(FileLog,strSave)
        print(sStep," step 2, sensors saved ", strSave)
        print(" delta x - last x ", dif)
        
        # round is newly added 2-Jul-2025
        can1=float(vi[0])*24/10 
        Bx1.setValue(can1)
        time.sleep(0.2)
        dix[0]=round(vi[0],2)
        Bdisp1.setText(str(dix[0]))
        time.sleep(0.2)
        
        can2=float(vi[1])*24/10
        Bx2.setValue(can2)
        time.sleep(0.2)
        dix[1]=round(vi[1],2)
        Bdisp2.setText(str(dix[1]))
        time.sleep(0.2)
        
        can3=float(vi[2])*24/10
        Bx3.setValue(can3)
        time.sleep(0.2)
        dix[2]=round(vi[2],2)
        Bdisp3.setText(str(dix[2]))
        time.sleep(0.2)
        
        can4=float(vi[3])*24/10
        Bx4.setValue(can4)
        time.sleep(0.2)
        dix[3]=round(vi[3],2)
        Bdisp4.setText(str(dix[3]))
        time.sleep(0.2)
        
        can5=float(vi[4])*24/10
        Bx5.setValue(can5)
        time.sleep(0.2)
        dix[4]=round(vi[4],2)
        Bdisp5.setText(str(dix[4]))
        time.sleep(0.2)
        
        can6=float(vi[5])*24/10
        Bx6.setValue(can6)
        time.sleep(0.2)
        dix[5]=round(vi[5],2)
        Bdisp6.setText(str(dix[5]))
        
        time.sleep(xSleep*10) #dikurangkan supaya kelihatan ada jeda . . .
        
        for y in range(6):
            v0[y] = vi[y]
            dStr += str(v0[y]) +","
           
        #debug each loop reading
        print("complete elaps ", y, elaps, lapTime)
        print("init lowest ", itm, itt) #, init, heat, peak, cool)
        print("heat raising ", htt, hti)
        print("peak temp-time-acc ", ptm, pti,Npk)
        print("cool temp-time", ctm, cti)
        runSmpl.Set_background_color_bco(red)
        print("loop ", init, heat, peak, cool, cmplt)
        time.sleep(xSleep*10)
        
        if heat==6 and peakWrite==False:
            i=0
            for z in itm:
                st_init  +=str(itm[i]) +","
                st_tini  +=str(itt[i]) +","
                st_pktm  +=str(ptm[i]) +","
                st_pkti  +=str(pti[i])+","
                st_stin  +=str(setini[i])+","
                st_stfn  +=str(setfin[i])+","
                i+=1
                
            samplenames=getBSampleName()
            writeLog(FileRes, tglx +",unit,"+samplenames+"\n")
            writeLog(FileRes, st_init[:-1]  +"\n")
            writeLog(FileRes, st_tini[:-1]  +"\n")
            writeLog(FileRes, st_pktm[:-1]  +"\n")
            writeLog(FileRes, st_pkti[:-1]  +"\n")
            writeLog(FileRes, st_stin[:-1]  +"\n")
            writeLog(FileRes, st_stfn[:-1]  +"\n")            
            peakWrite=True
            
        if cTr[0]==True and cTr[1]==True and cTr[2]==True and cTr[3]==True and cTr[4]==True and cTr[5]==True and heatWrite==False:
            heatWrite=True 
            testBack.setValue(2)

            i=0
            for z in ptm:
                st_calr  +=str(calor[i]) +","
                st_str1  +=str(str1d[i]) +","
                st_str3  +=str(str3d[i]) +","
                st_str28 +=str(str28d[i])+","
                st_str28x+=str(str28x[i])+","
                i+=1

            writeLog(FileRes, st_calr[:-1]  +"\n")
            writeLog(FileRes, st_str1[:-1]  +"\n")
            writeLog(FileRes, st_str3[:-1]  +"\n")
            writeLog(FileRes, st_str28[:-1] +"\n")
            writeLog(FileRes, st_str28x[:-1]+"\n")
            testBack.setValue(5)
            
        sStep+=1
        elaps+=xSleep
        #adaptive xSleep
        time.sleep(xSleep*37.7) #from 60 37.8
        runTest.Set_background_color_bco(grn)
        print("v0, last value ", dStr[0:-1]+"\n")
        
