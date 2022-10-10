from operator import indexOf
import re

datos2 = []
windows = []
temp = []
nipToDest = []
time = []
WakeUp = []
with open("C:/Users/juans/OneDrive/ceci/SLD/Pruebas Manuales SLD2-CS/SIP Alta temp Compensacion Inactiva/Escenario5 - SIP High Temp Com Unactive.txt") as fname:
	for lineas in fname:
		datos2.extend(lineas.split())
for index, val in enumerate (datos2): 
    if re.search('Window',val):
        windows.append(datos2[index+2])
    if re.search('Temp',val):
        temp.append(datos2[index+2])
    if re.search('SIPtoNIP',val):
        nipToDest.append(datos2[index+2])
    if re.search('Rx:',val):
        time.append(datos2[index+1])
    if re.search('up',val):
        WakeUp.append(datos2[index+2])
f = open ('WindowsReport.txt', 'w')
f.write('Sync Windows: \n')
for item in windows:
    f.write(("%s\n" % item[0]));
f.write('Temp: \n')
for item in temp:
    f.write(("%s\n" % item[0:2]));
f.write('SIPtoNIP : \n')
for item in nipToDest:
    f.write(("%s\n" % item));
f.write('Time: \n')
for item in time:
    f.write(("%s\n" % item));
f.write('WakeUp status: \n')
for item in WakeUp:
    f.write(("%s\n" % item));
file = open('WindowsReport.txt', 'r')
print(file.read())
