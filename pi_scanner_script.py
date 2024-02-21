#!/usr/bin/env python3

NULL_CHAR = chr(0)

#Release keys write_report(NULL_CHAR*8)

def write_report(report):
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write(report.encode())

string = "10254"


for x in [*string]:
        if int(x) == 0:
                write_report(NULL_CHAR*2+chr(39)+NULL_CHAR*5)
                write_report(NULL_CHAR*8)
        else:
                x = 29+int(x)
                write_report(NULL_CHAR*2+chr(x)+NULL_CHAR*5)
                write_report(NULL_CHAR*8)


write_report(NULL_CHAR*2+chr(40)+NULL_CHAR*5)
write_report(NULL_CHAR*8)

