""""
Thermaltest first written at 8 July 2024, last updated 10 Dec 2025
compiled with headache by Asep Yudi asepyudi2016@gmail.com

HARDWARE;
esp32wroom, sensor 6 ds18b20, nextion intellegent 4.3", pcb,
micro sd card & shield, battery and charger + step up, pin headers,
JST 2.54 4/3/2pins & DC connectors, cables, soldering % tin
SOFTWARE;
Nextion IDE, Thonny IDE, Python - micropython, google email, github
LIBRARY;
machine, os, nextion, ds18x20, onewire, sdcard, umail, ssl (renamed to ussl)
network, time, ntptime
python -m esptool --chip esp32 erase_flash
desclaimer: library used all free on github or pyPi
Web connect

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
lizt=NexPage(nh, 6, 0, "list")
#files=NexPage(nh, 7, 0, "filesonsd")
#wifis=NexPage(nh, 8, 0, "WiFi")
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

disp1=NexText(nh, pgs,63,"test.smp1")
disp2=NexText(nh, pgs,4, "test.smp2")
disp3=NexText(nh, pgs,5, "test.smp3")
disp4=NexText(nh, pgs,6, "test.smp4")
disp5=NexText(nh, pgx,83, "test.smp5")
disp6=NexText(nh, pgx,85, "test.smp6")

x1=NexNumber(nh,pgs,7, "test.x0")
x2=NexNumber(nh,pgs,8, "test.x1")
x3=NexNumber(nh,pgs,9, "test.x2")
x4=NexNumber(nh,pgs,10,"test.x3")
x5=NexNumber(nh,pgs,81,"test.x4")
x6=NexNumber(nh,pgs,82,"test.x5")

cmpltd1=NexText(nh,pgs, 67, "test.complt1")
cmpltd2=NexText(nh,pgs, 68, "test.complt2")
cmpltd3=NexText(nh,pgs, 69, "test.complt3")
cmpltd4=NexText(nh,pgs, 70, "test.complt4")
cmpltd5=NexText(nh,pgs, 81, "test.complt5")
cmpltd6=NexText(nh,pgs, 80, "test.complt6")

pgNo=1
sample1cn=NexText(nh, pgNo, 6,"samples.smpname1")
sample2cn=NexText(nh, pgNo, 7,"samples.smpname2")
sample3cn=NexText(nh, pgNo, 8,"samples.smpname3")
sample4cn=NexText(nh, pgNo, 9,"samples.smpname4")
sample5cn=NexText(nh, pgNo, 82,"samples.smpname5")
sample6cn=NexText(nh, pgNo, 85,"samples.smpname6")
    
sTtime1cn=NexText(nh, pgNo, 24,"samples.tmSmp1")
sTtime2cn=NexText(nh, pgNo, 25,"samples.tmSmp2")
sTtime3cn=NexText(nh, pgNo, 26,"samples.tmSmp3")
sTtime4cn=NexText(nh, pgNo, 27,"samples.tmSmp4")
sTtime5cn=NexText(nh, pgNo, 87,"samples.tmSmp5")
sTtime6cn=NexText(nh, pgNo, 89,"samples.tmSmp6")
    
rctime1cn=NexText(nh, pgNo, 35,"samples.start1")
rctime2cn=NexText(nh, pgNo, 36,"samples.start2")
rctime3cn=NexText(nh, pgNo, 37,"samples.start3")
rctime4cn=NexText(nh, pgNo, 38,"samples.start4")
rctime5cn=NexText(nh, pgNo, 88,"samples.start5")
rctime6cn=NexText(nh, pgNo, 90,"samples.start6")
    
runSt1=NexNumber(nh, pgNo, 53, "samples.nPrep1")
runSt2=NexNumber(nh, pgNo, 54, "samples.nPrep2")
runSt3=NexNumber(nh, pgNo, 55, "samples.nPrep3")
runSt4=NexNumber(nh, pgNo, 56, "samples.nPrep4")
runSt5=NexNumber(nh, pgNo, 95, "samples.nPrep5")
runSt6=NexNumber(nh, pgNo, 96, "samples.nPrep6")
gOrder = NexText(nh, pgNo, 74,"samples.komando")

ordTest=NexText(nh, 2, 65,"test.actTest")
mcuEls1=NexText(nh, 2, 3, "test.els1")
dispEls=NexText(nh, 2, 59,"test.elaps")

#BordTest=NexText(nh, 2, 93,"test_basic.actTest")
#BmcuEls1=NexText(nh, 2, 3, "test_basic.els1")
#BdispEls=NexText(nh, 2, 62,"test_basic.elaps")
#mcuEls2=NexText(nh, 10, 3,"test2.els1") test_basic


#ordTest2=NexText(nh, 10, 77,"test2.actTest")
ordLizt=NexText(nh, 6, 16,"list.listProg")
#mcuEls1.setText("")
#BmcuEls1.setText("")
#mcuEls2.setText("")

status=NexNumber(nh,0,30,"flashscreen.testStatus")
runFlas=NexText(nh, 0, 29, "flashscreen.run")
fileSt=NexText(nh, 0, 31,"flashscreen.neofile")
runSmpl=NexText(nh, 1, 77, "samples.run")
runTest=NexText(nh, 2, 76, "test.run")
#BrunTest=NexText(nh, 2, 82, "test_basic.run")
#runDate=NexText(nh, 3, 31, "setDate.run")
#runList=NexText(nh, 6, 42, "list.run")
#runFile=NexText(nh, 7, 20, "filesonsd.run")
#runWiFi=NexText(nh, 8, 15, "WiFi.run")
#runRslt=NexText(nh, 9, 54, "Result.run")


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
            #print(mess, "written")
        return "done"    
    except OSError as er:
        print(er)
        return "fail"

#write log
def writeLog(fns,shorts)->str:
    try:
        with open(fns, "a") as fs:
            n = fs.write(shorts)
            #print(shorts, n, "written")
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
        
def xTime(inTime):
    tm=time.localtime(inTime)
    jam=tm[4]*60+tm[5]
    return jam

def printTime(inpTime):
    tm=time.localtime(inpTime)
    return str(tm[3])+":"+str(tm[4])+":"+str(tm[5])

def getStat():
    rStat1==""
    while rStat1=="" or rStat1==None:
        rStat1=runSt1.getValue()
        time.sleep(0.1)
    rStat2==""    
    while rStat2=="" or rStat2==None:
        rStat2=runSt2.getValue()
        time.sleep(0.1)
    rStat3==""
    while rStat3=="" or rStat3==None:
        rStat3=runSt3.getValue()
        time.sleep(0.1)
    rStat4==""     
    while rStat4=="" or rStat4==None:
        rStat4=runSt4.getValue()
        time.sleep(0.1)
    rStat5==""    
    while rStat5=="" or rStat5==None:
        rStat5=runSt5.getValue()
        time.sleep(0.1)    
    Stat6==""    
    while rStat6=="" or rStat6==None:
        rStat6=runSt6.getValue()
        time.sleep(0.1)    
    return str(rStat1)+","+str(rStat2)+","+str(rStat3)+","+str(rStat4)+","+str(rStat5)+","+str(rStat6)

#trial this one, check 27Dec25
def getRecTime()->str:
    rctime1=""
    while rctime1=="" or rctime1==None:
        rctime1=rctime1cn.getText()
        time.sleep(0.05)

    rctime2=""
    while rctime2=="" or rctime2==None:
        rctime2=rctime2cn.getText()
        time.sleep(0.05)

    rctime3=""
    while rctime3=="" or rctime3==None:
        rctime3=rctime3cn.getText()
        time.sleep(0.05)
        
    rctime4=""
    while rctime4=="" or rctime4==None:
        rctime4=rctime4cn.getText()
        time.sleep(0.05)
        
    rctime5=""
    while rctime5=="" or rctime5==None:
        rctime5=rctime5cn.getText()
        time.sleep(0.05)

    rctime6=""
    while rctime6=="" or rctime6==None:
        rctime6=rctime6cn.getText()
        time.sleep(0.05)
        
    smpnamx=rctime1 +","+ rctime2 +","+ rctime3 +","+ rctime4 +","+ rctime5 +","+ rctime6
    return smpnamx

#trial this one, check 27Dec25
def getSampleName()->str:
    sample1=""
    while sample1=="" or sample1==None:
        sample1=sample1cn.getText()
        time.sleep(0.05)

    sample2=""
    while sample2=="" or sample2==None:
        sample2=sample2cn.getText()
        time.sleep(0.05)
        
    sample3=""
    while sample3=="" or sample3==None:
        sample3=sample3cn.getText()
        time.sleep(0.05)
        
    sample4=""
    while sample4=="" or sample4==None:
        sample4=sample4cn.getText()
        time.sleep(0.05)

    sample5=""
    while sample5=="" or sample5==None:
        sample5=sample5cn.getText()
        time.sleep(0.05)
        
    sample6=""
    while sample6=="" or sample6==None:
        sample6=sample6cn.getText()
        time.sleep(0.05)
                
    smpname=sample1 +","+ sample2 +","+ sample3 +","+ sample4 +","+ sample5 +","+ sample6
    return smpname

def getStartTime()->str:
    sTtime1=""
    while sTtime1=="" or sTtime1==None:
        sTtime1=sTtime1cn.getText()
        time.sleep(0.05)

    sTtime2=""
    while sTtime2=="" or sTtime2==None:
        sTtime2=sTtime2cn.getText()
        time.sleep(0.05)

    sTtime3=""
    while sTtime3=="" or sTtime3==None:
        sTtime3=sTtime3cn.getText()
        time.sleep(0.05)
        
    sTtime4=""
    while sTtime4=="" or sTtime4==None:
        sTtime4=sTtime4cn.getText()
        time.sleep(0.05)
        
    sTtime5=""
    while sTtime5=="" or sTtime5==None:
        sTtime5=sTtime5cn.getText()
        time.sleep(0.05)
        
    sTtime6=""
    while sTtime6=="" or sTtime6==None:
        sTtime6=sTtime6cn.getText()
        time.sleep(0.05)

    return sTtime1+","+sTtime2+","+sTtime3+","+sTtime4+","+sTtime5+","+sTtime6

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
        #if len(ch)<0:
        #    return "no sd card"
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
    
def filesonsd(code_perintah):
    
    fld=NexText(nh,7,7,"filecontent")
    fld.setText(lisfile)
    sdcd=NexText(nh,7,6,"sdcard")
    actfileCn=NexText(nh, 7, 4, "actfile")
    xfl=""
    suruh=""
    #fld.setText("del")
    time.sleep(1)
    ge=""
    if suruh=='load content':
        try:
        #sd = sdcard.SDCard(spi, machine.Pin(5))  # Compatible with ESP32 
        #vfs = os.VfsFat(sd)
        #os.mount(vfs, "/sd")
        #print("SD card Filesystem check ok")
        #sdcd.setText("SD card Filesystem check ok")
        #print(os.listdir("/sd")) 

            with open("/sd/ThermalX.csv", "r") as fs:
                for rw in fs:
                    ge = fs.readline().rstrip("\n")
                    xfl += ge +"\r\n"  #"\r\n"
            #csvdt.append(rw.rstrip('\n').rstrip('\r').split(dlm))
            
                print(ge)
        #print(xfl)
        #print(csvdt)
        #fld.setText(ge)
                fs.close()
                fld.setText(xfl)
            return "exit"
                #break
        
        except OSError as err:
            print('card not detected', err)
            sdcd.setText("SD card not detected") 
      

def getFileContent(namafile):
    fld=NexText(nh,7,7,"filecontent")
    ge=""
    
    xfl=""
    sd = sdcard.SDCard(spi, machine.Pin(5))
    vfs = os.VfsFat(sd)
    #os.mount(vfs, "/sd")
    #try:
    with open(namafile, "r") as fs:
        for rw in fs:
            ge = fs.readline()
            #xfl += rw +"\r\n"
            xfl += ge +"\r\n"
            #csvdt.append(rw.rstrip('\n').rstrip('\r').split(dlm))
            print(ge)
    print(xfl)
        #print(csvdt)
        #fld.setText(ge)
    fs.close()
    fld.setText(xfl)        


def main_menu():
    zOrder=""   
    while True:
        statusTest(0)
        zOrder=gOrder.getText()
        print("zOrder", zOrder)
    
        if zOrder=="mcu-reset": #page 0 button reset
        #sld=0
            flas.setText("mcu-reset done")
            time.sleep(2)
            gOrder.setText("mcu-reset done")
            time.sleep(1)
            machine.reset()
        
        elif zOrder=="check system":
            sis=checksystem()
            time.sleep(3)
            if sis=="ok":
                flas.setText("System check Ok")
                gOrder.setText("Initial")
                time.sleep(2)

            elif zOrder=="reset display":
                print("display reset")
                gOrder.setText("reset done")      
                time.sleep(2)
        
        elif zOrder=="Initial":
            statusTest(0)
            smpl.show()
            time.sleep(0.3)
            gOrder.setText("Initialized")
            stSmpl=NexText(nh,1,79,"samples.run")
            stSmpl.Set_background_color_bco(red)
            time.sleep(1)
            stSmpl.Set_background_color_bco(0)
            time.sleep(1)            
            
        elif zOrder=="sample save":
            time.sleep(0.1)
            getsamplesready()
            #gOrder.setText("files saved")
        
        elif zOrder=="back sample":
            smpl.show()
            time.sleep(1)
            gOrder.setText("samples...")
                   
        elif zOrder== "files":
            time.sleep(1)
            files.show()
            gOrder.setText("page file")
        
        elif zOrder== "set date":
            time.sleep(1)
            kald.show()
            gOrder.setText("setting date")
        
        elif zOrder== "back list":
            lizt.show()
            time.sleep(1)
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

def sensorReading():
    dvState=NexText(nh, 0, 28,"flashscreen.divmode")
    statusTest(1)
    runSmpl.Set_background_color_bco(0)
    ordTest.setText("Testing ...")
    #dvState=NexText(nh, 0, 28,"flashscreen.divmode")
    vi =[0,0,0,0,0,0]
    v0 =[0,0,0,0,0,0]
    dix=[0,0,0,0,0,0]

    ini=[0,0,0,0,0,0]  #initial temporary temperature 
    iti=[0,0,0,0,0,0]  #initial time
    itm=[0,0,0,0,0,0]  #initial temperature
    itt=[0,0,0,0,0,0]  #initial temporary time
    
    cmm=[0,0,0,0,0,0]    #cooling temporary temperature
    ctm=[0,0,0,0,0,0]   #cooling temperature
    ctt=[0,0,0,0,0,0]   #cooling temporary time
    cti=[0,0,0,0,0,0]  #cooling time 

    htm=[0,0,0,0,0,0]    #start heating temperature
    hti=[0,0,0,0,0,0]  #start heating time 
    htt=[0,0,0,0,0,0]   #start heating temporary time

    ptm=[0,0,0,0,0,0] #peak temperature
    ptt=[0,0,0,0,0,0]   #peak temporary time
    pti=[0,0,0,0,0,0]  #peak time
    mx =[0,0,0,0,0,0]   #temporary max temperature

    
    time.sleep(0.1)
    dvState.getText()
    #if written so no need to add. sign is here
    wr_init=False
    wr_heat=False
    wr_peak=False
    wr_cool=False
    all_done=False
    wr_all_done=False
    completed=False
    wr_completed=False
    tex=["","","","","",""]
    st_intm="initial temp, oC,"
    st_inti="initial time, min,"
    st_httm="heating temp, oC,"
    st_htti="heating time, min,"
    st_pktm="peak temp, oC,"
    st_pkti="peak time, min,"
    st_cltm="cool temp, oC,"
    st_clti="cool time, min,"
    st_stin="setting initial, min,"
    st_stfn="setting final, min,"
    st_calr="calor, cal/g,"
    st_str1="str 1 day, kg/cm2"
    st_str3="str 3 days, kg/cm2"
    st_str28="str 28 days, kg/cm2"
    
    if dvState!="Continue":
        cmpltd1.setText(" ")
        cmpltd2.setText(" ")
        cmpltd3.setText(" ")
        cmpltd4.setText(" ")
        #cmpltd5.setText(" ")
        #cmpltd6.setText(" ") 
    
    #sign for achieving the points below
    iTr=[False, False, False, False, False, False] #inital true
    pTr=[False, False, False, False, False, False] #peak true
    cTr=[False, False, False, False, False, False] #cooling true
    hTr=[False, False, False, False, False, False] #heating true 
    #flk=[False, False, False, False, False, False] #cooling flat true
    dix=[0.00,0.00,0.00,0.00,0.00,0.00]
    cmplt=0
    doneX=False
    uStart=25

    u=0
    Display_elapse=dispEls.getText()
    
    if Display_elapse!="":
        elaps=int(Display_elapse)
        
    else:
        elaps=0
    runSmpl.Set_background_color_bco(wht)
    voStr=""
    delta1=5
    initRate=0.1
    now=time.time()
    awal=xTime(now)
    ref1=xTime(now)
    ref2=xTime(now)
    actual_gap1=0
    actual_gap2=0
    #=70
    xSleep=5
    xRange=20*60*60/xSleep

    xStr=""
    roms = ds_sensor.scan()

    for y in range(0,2):
        sStr0=""
        d=0
        ds_sensor.convert_temp()
        for rom in roms:
            v0[d]=ds_sensor.read_temp(rom)
            sStr0 += str(v0[d]) +","
            #vi[d]=v0[d]
            d+=1
            time.sleep(0.3)
        print("reading to avoid value -127 and 85", sStr0)

    #check reading
    xStr=printTime(now)+","+str(elaps)+","+sStr0[0:-1]+"\n"
    print("first on start", xStr)
        #dWr=writeLog(FileLog,xStr)
        
    a=0
    can1=round(float(v0[a])*24/10,0) #round is newly added 2 jul
    x1.setValue(can1)
    time.sleep(0.1)
    dix[a]=round(v0[a],2)
    disp1.setText(str(dix[a]))
    time.sleep(0.1)
        
    a=1
    can2=float(v0[a])*24/10
    x2.setValue(can2)
    time.sleep(0.1)
    dix[a]=round(v0[a],2)
    disp2.setText(str(dix[a]))
    time.sleep(0.1)
        
    a=2
    can3=float(v0[a])*24/10
    x3.setValue(can3)
    time.sleep(0.1)
    dix[a]=round(v0[a],2)
    disp3.setText(str(dix[a]))
    time.sleep(0.1)
        
    a=3
    can4=float(v0[a])*24/10
    x4.setValue(can4)
    time.sleep(0.1)
    dix[a]=round(v0[a],2)
    disp4.setText(str(dix[a]))
    time.sleep(0.1)
                        
    a=4
    can5=float(v0[a])*24/10
    x5.setValue(can5)
    time.sleep(0.1)
    dix[a]=round(v0[a],2)
    disp5.setText(str(dix[a]))
    time.sleep(0.1)
    
    a=5
    can6=float(v0[a])*24/10
    x6.setValue(can6)
    time.sleep(0.1)
    dix[a]=round(v0[a],2)
    disp6.setText(str(dix[a]))
    time.sleep(0.1)

    ordTest.setText("testing..")
    #ordTest2.setText("testing..")
    mcuEls1.setText(elaps)
    #mcuEls2.setText(elaps)
        
    gOrder.setText("test on") 
        
    actTime=printTime(now)
    lapTime=0
        
    strPeakTrue=""
    strInitTrue=""
    print('duration', xRange)
    init=0
    heat=0
    peak=0
    cool=0
    
    setini =[0,0,0,0,0,0]
    setfin =[0,0,0,0,0,0]
    calor  =[0,0,0,0,0,0]
    heat_rt=[0,0,0,0,0,0]
    cool_rt=[0,0,0,0,0,0]
    str1d  =[0,0,0,0,0,0]
    str3d  =[0,0,0,0,0,0]
    str28d =[0,0,0,0,0,0]

    while elaps<xRange :
        strPeakTrue=""
        strInitTrue=""
        NOW=time.time()
        cTime=xTime(NOW)
        lapTime=printTime(NOW)
        if cTime-ref1>=delta1:
            vrder=gOrder.getText()
            runSmpl.Set_background_color_bco(wht)
            ref1=cTime
            if vrder=="abort":
                flas.show()
                gOrder.setText("...")
                break
            elif vrder=="send result":
                resul.show()
                gOrder.setText("...")
                break
            elif vrder=="back list":
                lizt.show()
                gOrder.setText("...")
                break 
            ref1=cTime
                    
        mcuEls1.setText(elaps)
        #mcuEls2.setText(elaps)
        ds_sensor.convert_temp() # must in loop       
        strSave=""
        sdSTR=lapTime+","+str(elaps)+","
        lz=0
        for rom in roms:
            vi[lz]=ds_sensor.read_temp(rom)
            if vi[lz]>0 and vi[lz]!=85:
                sdSTR += str(vi[lz]) +","
            else:
                sdSTR += ",,"
            time.sleep_ms(300)
            lz+=1
                    
        strSave=sdSTR[0:-1]+"\n"
        stSens=writeLog(FileLog,strSave)
        #xx=writeLog(FileLog,strSave)
        if stSens=="done":
            print("sensors saved ", stSens, strSave)

        can1=round(float(vi[0])*24/10,0) #round is newly added 2 jul
        x1.setValue(can1)
        time.sleep(0.1)
        dix[0]=round(vi[0],1)
        disp1.setText(str(dix[0]))
        time.sleep(0.1)

        can2=float(vi[1])*24/10
        x2.setValue(can2)
        time.sleep(0.1)
        dix[1]=round(vi[1],1)
        disp2.setText(str(dix[1]))
        time.sleep(0.1)

        can3=float(vi[2])*24/10
        x3.setValue(can3)
        time.sleep(0.1)
        dix[2]=round(vi[2],1)
        disp3.setText(str(dix[2]))
        time.sleep(0.1)

        can4=float(vi[3])*24/10
        x4.setValue(can4)
        time.sleep(0.1)
        dix[3]=round(vi[3],1)
        disp4.setText(str(dix[3]))
        time.sleep(0.1)

        can5=float(vi[4])*24/10
        x5.setValue(can5)
        time.sleep(0.1)
        dix[4]=round(vi[4],1)
        disp5.setText(str(dix[4]))
        time.sleep(0.1)

        can6=float(vi[5])*24/10
        x6.setValue(can6)
        time.sleep(0.1)
        dix[5]=round(vi[5],1)
        disp6.setText(str(dix[5]))
        time.sleep(0.1)

        runSmpl.Set_background_color_bco(grn)
        
        #and vi[y]>0 and vi[y]!=85
        y=0
        cmplt=0
        for t in v0:

                    
            #find initial (lowest temp)    
            if elaps>=30 and iTr[y]==False:
                if vi[y]<v0[y]:
                    ini[y]=vi[y]
                    itt[y]=elaps
                    
                    if ini[y]>vi[y] or ini[y]<v0[y] and iTr[y]==False:
                        iTr[y]=True
                        iti[y]=itt[y]
                        itm[y]=ini[y]
                        tex[y]="ini"
                        ordTest.setText("Initial point sample "+str(y+1) )
                        init+=1
                    elif ini[y]>v0[y] and hTr[y]==True:
                        iTr=True
                        iti=0
                        itm[y]=v0[y]
                    
            if elaps>=30 and hTr[y]==False: #and iTr[y]==True and hTr[y]==False and cTr[y]==False
                if vi[y]>v0[y]:
                    htt[y]=vi[y]
                if (vi[y]-v0[y]>0.2 or vi[y]-v0[y]<=0.5)  and pTr[y]==False:
                    hTr[y]=True
                    htm[y]=htt[y]
                    hti[y]=elaps
                    tex[y]="ini-heat"
                    ordTest.setText("Heating point sample "+str(y+1))
                    heat+=1


            if elaps>=60 and pTr[y]==False:
                if vi[y]>mx[y]:
                    mx[y]=vi[y]
                    ptt[y]=elaps
                    #hTr[y]==True and
                if mx[y]-vi[y]>0.2 and cTr[y]==False and pTr[y]==False: 
                    pTr[y]=True
                    ptm[y]=mx[y]
                    pti[y]=ptt[y]
                    tex[y]="ini-heat-peak"
                    ordTest.setText("Peak point sample "+str(y+1) )
                    setini[y]=int(0.3*iti[y])  #int(0.3*pti[t]) 0.62
                    setfin[y]=int(0.62*iti[y])
                    calor[y]=int((ptm[y]-htm[y])*1000/(pti[y]-hti[y])) # calorific released equal to temp * time 
                    heat_rt[y]=0.5*(ptm[y]-htm[y])*(pti[y]-hti[y])
                    str1d[y]= int(heat_rt[y]/41+10*heat_rt[y]/(pti[y]-hti[y]))/2
                    str3d[y]= int(str1d[y]*2/1.4)    #str3d[t-2]=int(str1d[t-2]*2/1.4)
                    peak+=1
                
                
                #if pTr[y]==True and vi[y]>ptm[y]:
                #   pTr[y]=False
                #    mx[y]=vi[y]
                 #   peak=peak-1  hTr[y]==True and
            if elaps>pti[y]+60:
                if cTr[y]==False and pTr[y]==True and v0[y]-vi[y]>0.2:
                    ctt[y]=elaps
                    cmm[y]=vi[y]
                
                #cooling happened
                elif cTr[y]==False and pTr[y]==True and (v0[y]-vi[y]>0.1 or v0[y]-vi[y]<=0.2):
                    cTr[y]=True
                    ctm[y]=cmm[y]
                    cti[y]=ctt[y]
                    tex[y]="ini-heat-peak-cool"
                    ordTest.setText("Cooling point sample "+str(y+1) )             
                    cool_rt[y]=0.5(ptm[y]-ctm[y])*(cti[y]-pti[y])
                    str28d[y]=int(str3d[t-2]+cool_rt[y]/(cool_rt[y]/(cti[y]-pti[y])))              
                    cool+=1
                    cmplt+=1
                #New 25-08   
                #other idea if gap current vs gap prev  still almost the same (both need definition)
            if y==0:
                cmpltd1.setText(tex[y])
            if y==1:
                cmpltd2.setText(tex[y])
            if y==2:
                cmpltd3.setText(tex[y])
            if y==3:
                cmpltd4.setText(tex[y])
            if y==4:
                cmpltd5.setText(tex[y])
            if y==5:
                cmpltd6.setText(tex[y])
            if iTr[y]==True:    
                v0[y]=vi[y]
            y+=1
                
            #debug each loop reading 
            print("complete elaps ", y, elaps, lapTime)
            print("init ", ini, itt, init, heat, peak, cool)
            print("heat ", htm, hti)
            print("peak ", ptm, pti)
            print("cool ", ctm, cti)
            runSmpl.Set_background_color_bco(red)
            print("loop ", init, heat, peak, cool,cmplt)
            #add 25-08 to write once dud
            if init==len(vi) and wr_init==False:
                i=0
                for z in itm:
                    st_intm+=str(itm[i])+","
                    st_inti+=str(iti[i])+","
                    i+=1
                runSmpl.Set_background_color_bco(red)
                print("init all ", itm, iti)
                writeLog(FileRes,st_intm[:-1]+"\n")
                writeLog(FileRes,st_inti[:-1]+"\n")
                time.sleep(1)
                ordTest.setText("Initial temp defined ...")
                inTemp1.setText(ini[0])
                inTemp2.setText(ini[1])
                inTemp3.setText(ini[2])
                inTemp4.setText(ini[3])
                wr_init=True
                
            if heat==len(vi) and wr_heat==False:
                runSmpl.Set_background_color_bco(red)
                print("heat all ", htm, hti)
                i=0
                for z in htm:
                    st_httm+=str(htm[i])+","
                    st_htti+=str(hti[i])+","
                    i+=1
                writeLog(FileRes,st_httm[:-1]+ str(htm)+"\n")
                writeLog(FileRes,st_htti[:-1]+ str(hti)+"\n")
                time.sleep(1)
                ordTest.setText("heating temp defined ...")
                wr_heat=True
            if peak==len(vi) and wr_peak==False:
                runSmpl.Set_background_color_bco(red)
                print("peak all ", ptm, pti)
                i=0
                for z in ptm:                
                    st_pktm+=str(ptm[i])+","
                    st_pkti+=str(pti[i])+","
                    st_stin+=str(setini[i])+","
                    st_stfn+=str(setfin[i])+","
                    st_calr+=str(calor[i])+","
                    st_str1+=str(str1d[i])+","
                    st_str3+=str(str3d[i])+","
                    i+=1
                writeLog(FileRes,st_pktm[:-1]+"\n")
                writeLog(FileRes,st_pkti[:-1]+"\n")
                writeLog(FileRes,st_calr[:-1]+"\n")
                writeLog(FileRes,st_stin[:-1]+"\n")
                writeLog(FileRes,st_stfn[:-1]+"\n")
                writeLog(FileRes,st_str1[:-1]+"\n")
                writeLog(FileRes,st_str3[:-1]+"\n")
                                 
                ordTest.setText("peak temp defined ...")
                time.sleep(1)
                pkTemp1.setText(ptm[0])
                pkTemp2.setText(ptm[1])
                pkTemp3.setText(ptm[2])
                pkTemp4.setText(ptm[3])
                
                pkTime1.setText(pti[0])
                pkTime2.setText(pti[1])
                pkTime3.setText(pti[2])
                pkTime4.setText(pti[3])
                
                setIni1.setText(setini[0])
                setIni2.setText(setini[1])
                setIni3.setText(setini[2])
                setIni4.setText(setini[3])
                
                setFin1.setText(setfin[0])
                setFin2.setText(setfin[1])
                setFin3.setText(setfin[2])
                setFin4.setText(setfin[3])
                
                calor1.setText(calor[0])
                calor2.setText(calor[1])
                calor3.setText(calor[2])
                calor4.setText(calor[3])
                
                str1d1.setText(str1d[0])
                str1d2.setText(str1d[1])
                str1d3.setText(str1d[2])
                str1d4.setText(str1d[3])
                
                str3d1.setText(str3d[0])
                str3d2.setText(str3d[1])
                str3d3.setText(str3d[2])
                str3d4.setText(str3d[3])
                wr_peak=True
                
            if cool==len(vi) and wr_cool==False:
                runSmpl.Set_background_color_bco(red)
                print("cool all ", ctm, cti)
                i=0
                for z in ptm:
                    st_cltm+=str(ctm[i])+","
                    st_clti+=str(cti[i])+","
                    st_str28+=str(str28d[i])+","
                    i+=1
                writeLog(FileRes, st_str28[:-1]+"\n")                   
                writeLog(FileRes, st_cltm[:-1]+"\n")
                writeLog(FileRes, st_clti[:-1]+"\n")
                time.sleep(1)
                ordTest.setText("cooling temp defined ...")
                
                str28d1.setText(str28d[0])
                str28d2.setText(str28d[1])
                str28d3.setText(str28d[2])
                str28d4.setText(str28d[3])
                wr_cool=True
                
            if cmplt==len(vi):
                doneX=True
                #break
            
        #just for sign     
        print("done ",init,heat,peak,cool,cmplt)
        if wr_peak==True and wr_init==True and wr_heat==True and all_done==False:
            ordTest.setText("Testing Done !")
            all_done=True
        if completed==False and wr_cool==True   :
            ordTest.setText("Testing Completed !")
            completed=True
        #combine logger and resut on the top of final file ready for download
        if all_done==True and wr_all_done==False and wr_completed==False and completed==True:
            fl_fin=open(FileFin,"a")
            fl_log=open(FileLog,"r")
            fl_res=open(FileRes,"r")
            temp_res=fl_res.read()
            temp_log=fl_log.read()
            fl_fin.write(temp_res)
            fl_fin.write(temp_log)
            fl_fin.close()
            fl_log.close()
            fl_res.close()
            ordTest.setText("Test result ready !")
            wr_all_done=True
            
        if wr_completed==False and wr_all_done==True:
            ordTest.setText("Test result completed !")
            os.remove(FileFin)
            createLog(FileFin, judul)
            fl_fin=open(FileFin,"a")
            fl_log=open(FileLog,"r")
            fl_res=open(FileRes,"r")
            temp_res=fl_res.read()
            temp_log=fl_log.read()
            fl_fin.write(temp_res)
            fl_fin.write(temp_log)
            fl_fin.close()
            fl_log.close()
            fl_res.close()            
            wr_completed=True
        
        elaps+=xSleep
        time.sleep(xSleep*60)
    
