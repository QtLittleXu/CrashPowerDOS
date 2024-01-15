import os

gcc = '/i686_elf_tools/bin/i686-elf-gcc.exe -I include/ -std=gnu99 -ffreestanding -O2 -c'
asm = '/i686_elf_tools/bin/i686-elf-as.exe'
nasm = "nasm -f elf32"
ld = '/i686_elf_tools/bin/i686-elf-ld.exe'

cd = os.getcwd()

out = "target"

def clean():
    print("Clean target flolder")
    for file in os.listdir(cd + "\\target"):
        os.remove(cd + "\\target\\" + file)
    return 0

def build_boot():
    print("Building boot source code...")
    status = True
    for file in os.listdir(cd + '\\boot'):
        if status and file == 'boot.asm' :
            cmd = cd + asm +" " + cd+"\\boot\\"+file + " -o "+cd+"\\target\\"+file.split(".")[0]+".o"
            status = False
        else :
            cmd = nasm +" " + cd+"\\boot\\"+file + " -o "+cd+"\\target\\"+file.split(".")[0]+".o"
        e = os.system(cmd)
        if e != 0 :
            return -1
    return 0

def build_driver():
    print("Building driver source code...")
    for file in os.listdir(cd + '\\driver'):
        cmd = cd + gcc +" " + "driver\\"+file + " -o "+"target\\"+file.split(".")[0]+".o"
        e = os.system(cmd)
        if e != 0 :
            return -1
    return 0

def build_kernel():
    print("Building kernel source code...")
    for file in os.listdir(cd + '\\kernel'):
        cmd = cd + gcc +" " + "kernel\\"+file + " -o "+"target\\"+file.split(".")[0]+".o"
        e = os.system(cmd)
        if e != 0 :
            return -1
    return 0

def build_data():
    print("Building data source code...")
    for file in os.listdir(cd + '\\data'):
        cmd = cd + gcc +" " + "data\\"+file + " -o "+"target\\"+file.split(".")[0]+".o"
        e = os.system(cmd)
        if e != 0 :
            return -1
    return 0

def linker():
    print("Linking IR...")
    source_file = ""
    for file in os.listdir(cd + '\\target'):
        source_file = source_file + " target\\" + file
    return os.system(cd + "/i686_elf_tools/bin/i686-elf-gcc.exe -T linker.ld -o isodir\\sys\\kernel.elf -ffreestanding -O2 -nostdlib " + source_file + " -lgcc")

clean()
a = build_boot()
if a != 0:
    exit(-1)
a = build_driver()
if a != 0:
    exit(-1)
a = build_kernel()
if a != 0:
    exit(-1)
a = build_data()
if a != 0:
    exit(-1)
a = linker()
if a != 0:
    exit(-1)

os.system("qemu-system-i386 -kernel isodir\\sys\\kernel.elf")
