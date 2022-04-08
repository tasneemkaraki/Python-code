from tkinter import filedialog
from tkinter import *
dire = ["START", "BYTE", "RESB" , "WORD" , "RESW", "LTORG", "END"]
intfile = open("intmdte_file.mdt","w+") 
symFile = open("SYMTAB.txt","w+")
ErrorFile = open("Error.txt","w+")
ErrorFile = open("Error.txt","w+")
Littab= open("LITTAB.txt", "w+")


SYMTAB = {}
littab = {}
litpool = {}
label = ""
op = ""
error = 0
opttab = {}
opfile = open("OPTAB.txt", "r")
for line in opfile:
    opttab[line[0:10].split(' ')[0]] = line[11:20].strip()
programname = ""
startaddress = 0
filename = open("cource_file.asm", "r") 
assembly = filename.readlines()
fline = assembly[0]         
if fline[11:20].strip() == "START":
    startaddress = int(fline[21:38].strip(),16)
    locCount = startaddress  
    programname =  fline[0:10].strip()
    space = 10-len(str((locCount)))
    intfile.write(hex(locCount)[2:]+" "*space+fline)
    intfile.flush()

else:
    locCount = 0


for i, line in enumerate(assembly):
    op = line[11:20].strip()
    if(op!= "END" and op != "START"):
        
        if line[0] != '.':  
            if(op == "LTORG"): 
                intfile.write(" "*10+line)
            else :
                space = 10-len(str((locCount)))
                intfile.write(hex(locCount)[2:]+" "*space+line)

            label = line[0:10].strip()
            if label != "":
                if label in SYMTAB: 
                    error = 1
                    print("There is MULTIPLE DECLARATION in the LABEL :"+" "+label)
                    ErrorFile.write("There is MULTIPLE DECLARATION in the LABEL :"+" " + label)
                    ErrorFile.write("\n")
                    break
                else:
                    SYMTAB[label] = hex(locCount)[2:]
                    symFile.write(SYMTAB[label]+" "*10)
                    symFile.write(line[0:7].strip())
                    symFile.write("\n")
            found = 0 
            if op in opttab:
                found = 1
                locCount += 3
            else:
                operand = 0

            if (found == 0 and op in dire):
                
                if op == "RESB":
                    operand = line[21:38].strip()
                    locCount = locCount + int(operand)
                elif op == "WORD":
                    locCount =  locCount + 3
                elif op == "BYTE":
                        operand = line[21:38].strip()
                        if operand[0] == 'X':
                           locCount = locCount + int((len(operand)-3)/2)
                        elif operand[0] == 'C':
                            locCount = locCount + (len(operand)-3)
                elif op == "RESW":
                    operand = line[21:38].strip()
                    locCount = locCount + 3 * int(operand)
                elif op == "LTORG":
                    for i in littab:
                        littab[i][2] = hex(locCount)[2:] 
                        space = 10-len(str((locCount)))
                        intfile.write(hex(locCount)[2:]+" "*space+"*"+" "*7+"="+i+"\n")
                        locCount += int(littab[i][1])
                    littab = {}
                       
        
            literalList = []
            if line[21:22] == '=':
                exist = 1
                literal = line[22:38].strip()
                if literal[0]== 'X':
                    hexco = literal[2:-1]
                elif literal[0]=='C':
                    hexco = literal[2:-1].encode("utf-8").hex()
                
                else:
                    print("NOT Valid Literal : "+" "+line[22:38].strip())
                    ErrorFile.write("NOT Valid Literal : "+" "+line[22:38].strip())
                    ErrorFile.write("\n")
                    break

                if literal in litpool:
                    exist = 0
                
                else:
                    literalList=[hexco,len(hexco)/2, 0]
                    littab[literal]= literalList
                    litpool[literal]= literalList
                    Littab.write(str(litpool[literal])) 
                    Littab.write("\n") 
            opcode = line[11:20].strip()
            if (opcode not in opttab and opcode not in dire and opcode!="LTORG"):
                print("NOT Valid OPCODE: "+" "+line[11:20].strip())
                ErrorFile.write("NOT Valid OPCODE: "+" "+line[11:20].strip())
                ErrorFile.write("\n")
                break
if op == "END":
    intfile.write(" "*10+line)
if littab:   
    for i in littab:
        littab[i][2] = hex(locCount)[2:]
        space = 10-len(str((locCount)))
        intfile.write(hex(locCount)[2:]+" "*space+"*"+" "*7+"="+i+"\n")
        locCount += int(littab[i][1])
opfile.close()
intfile.close()
filename.close()
programLength = 0
lastaddress=locCount
programLength = int(lastaddress) - int(startaddress)
proglen = hex(int(programLength))[2:].format(int(programLength))
loc = hex(int(locCount))[2:].format(int(locCount))


#gui part 

file = Tk()
file.title("sic assembler with literal") 
file.geometry('600x600')
text1 = open('SYMTAB.txt').read()
prognam = Label(file ,text = "Program Name :" + programname, font='time 18 bold italic', fg='green')
prognam.pack()
programLength = Label(file ,text = " Program Langth :" + str(proglen) , font='time 18 bold italic ', fg='green')
programLength.pack()
programLength = Label(file ,text = " Location Counter :" + str(loc) , font='time 18 bold italic ', fg='green')
programLength.pack()
tit = Label(file, text=" Symbol Table:", font='time 18 bold italic underline')
tit.pack()
symbol = Text(file, height=120, width=120 ,font='time 18 bold italic'  )
symbol.configure(background = "silver")
symbol.insert(END,SYMTAB)
symbol.pack()
lit = Label(file, text=" Literal  :", font='time 18 bold italic underline')
lit.pack()
liter = Text(file, height=120, width=120 ,font='time 18 bold italic'  )
liter.insert(END,littab)
liter.pack()


file.mainloop()


