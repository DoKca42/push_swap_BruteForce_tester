import os
import subprocess
import random
import statistics

class colors:
    reset = '\033[0m'
    bold = '\033[01m'
    disable = '\033[02m'
    underline = '\033[04m'
    reverse = '\033[07m'
    strikethrough = '\033[09m'
    invisible = '\033[08m'

    class fg:
        black = '\033[30m'
        red = '\033[31m'
        green = '\033[32m'
        orange = '\033[33m'
        blue = '\033[34m'
        purple = '\033[35m'
        cyan = '\033[36m'
        lightgrey = '\033[37m'
        darkgrey = '\033[90m'
        lightred = '\033[91m'
        lightgreen = '\033[92m'
        yellow = '\033[93m'
        lightblue = '\033[94m'
        pink = '\033[95m'
        lightcyan = '\033[96m'

    class bg:
        black = '\033[40m'
        red = '\033[41m'
        green = '\033[42m'
        orange = '\033[43m'
        blue = '\033[44m'
        purple = '\033[45m'
        cyan = '\033[46m'
        lightgrey = '\033[47m'

def push_swap(a, b, operation):
    if operation == 'sa':
        if len(a) >= 2:
            a[0], a[1] = a[1], a[0]
    elif operation == 'sb':
        if len(b) >= 2:
            b[0], b[1] = b[1], b[0]
    elif operation == 'ss':
        if len(a) >= 2:
            a[0], a[1] = a[1], a[0]
        if len(b) >= 2:
            b[0], b[1] = b[1], b[0]
    elif operation == 'pa':
        if b:
            a.insert(0, b.pop(0))
    elif operation == 'pb':
        if a:
            b.insert(0, a.pop(0))
    elif operation == 'ra':
        if a:
            a.append(a.pop(0))
    elif operation == 'rb':
        if b:
            b.append(b.pop(0))
    elif operation == 'rr':
        if a:
            a.append(a.pop(0))
        if b:
            b.append(b.pop(0))
    elif operation == 'rra':
        if a:
            a.insert(0, a.pop())
    elif operation == 'rrb':
        if b:
            b.insert(0, b.pop())
    elif operation == 'rrr':
        if a:
            a.insert(0, a.pop())
        if b:
            b.insert(0, b.pop())
    return a, b

def MakeAll():
    files = os.listdir()
    if "Makefile" not in files:
        print(colors.fg.yellow + colors.bold+"WARNING:"+colors.reset+colors.fg.yellow+" Makefile not found")
        print(colors.fg.darkgrey + "* Skip make")
    else:
        result = subprocess.run(['make', 're'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            if len(result.stdout) == 0:
                print(colors.fg.yellow + colors.bold+"WARNING:"+colors.reset+colors.fg.yellow+" Makefile rule error")
            else:
                print(colors.fg.lightred + colors.bold+"FAIL:"+colors.reset+colors.fg.lightred+" Makefile failed to compile (check your code)")
                return 1
            print(colors.fg.darkgrey + "* Skip make")
    files = os.listdir()
    if "push_swap" not in files:
        print(colors.fg.lightred + colors.bold+"FAIL:"+colors.reset+colors.fg.lightred+" 'push_swap' executable file not found")
        return 1

def LineChecker(a, result, test_nb, compare):
    if len(a) <= 3 and len(result) >= 3:
        print(colors.reset+colors.fg.yellow + str(test_nb) + ". So many instructions, '"+str(len(result))+"' instructions for 3 numbers (max 3)")
        print(colors.fg.darkgrey +"   "+ str(compare)+"\n")
        return 1
    elif len(a) <= 5 and len(result) >= 12:
        print(colors.reset+colors.fg.yellow + str(test_nb) + ". So many instructions, '"+str(len(result))+"' instructions for 5 numbers (max 12)")
        print(colors.fg.darkgrey +"   "+ str(compare)+"\n")
        return 1
    elif len(a) <= 100 and len(result) >= 700:
        print(colors.reset+colors.fg.yellow + str(test_nb) + ". So many instructions, '"+str(len(result))+"' instructions for 100 numbers (max 700)")
        print(colors.fg.darkgrey +"   "+ str(compare)+"\n")
        return 1
    elif len(a) <= 500 and len(result) >= 5500:
        print(colors.reset+colors.fg.yellow + str(test_nb) + ". So many instructions, '"+str(len(result))+"' instructions for 500 numbers (max 5500)")
        print(colors.fg.darkgrey+"   "+ str(compare)+"\n")
        return 1
    else:
        return 0

def Reader(cmd, result, test_nb, stats_op):
    cmd.remove('./push_swap')
    compare = cmd.copy()
    a = cmd.copy()
    b = []
    i = 0
    possibility = ['sa', 'sb', 'ss', 'pa', 'pb', 'ra', 'rb', 'rr', 'rra', 'rrb', 'rrr']
    for line in result:
        line = line.strip()
        if line in possibility:
            a, b = push_swap(a, b, line)
            i += 1
        else:
            print(colors.fg.red + str(test_nb) + ". KO [Invalid character]")
            return 2

    if sorted(compare) == a:
        stats_op.append(i)
        return LineChecker(a, result, test_nb, compare)
    else:
        print(colors.fg.red + str(test_nb) + ". KO")
        print(colors.fg.red +"   "+ str(cmd))
        return 2

def GenerateRdm(typeval, nb):
    if typeval == 0:
        rdmvls = random.sample(range(-2147483648, 2147483647), nb)
    elif typeval == 1:
        rdmvls = random.sample(range(0, 2147483647), nb)
    else:
        rdmvls = random.sample(range(-2147483648, 0), nb)
    return rdmvls

def RunPushSwap(test_nb, cmd, stats_op):
    try:
        result = subprocess.run([str(i) for i in cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
        return Reader(cmd, result.stdout.decode('utf-8').splitlines(), test_nb, stats_op)
    except subprocess.TimeoutExpired:
        print(colors.fg.red+str(test_nb)+". Failed by time out")
        print(colors.fg.red +"   "+ str(cmd))
        return 2

def RunPushSwapFail(cmd, test_nb, type_res, std):
    try:
        result = subprocess.run([str(i) for i in cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
        res_stdout = result.stdout.decode('utf-8').splitlines()
        res_stderr = result.stderr.decode('utf-8').splitlines()
        if type_res == 0:
            if len(res_stderr) == 0 and len(res_stdout) == 0:
                return 0
            else:
                std["stdout"] += result.stdout.decode('utf-8')
                std["stderr"] += result.stderr.decode('utf-8')
                return 2
        else:
            if len(res_stdout) == 0 and len(res_stderr) == 1 and res_stderr[0] == "Error":
                return 0
            else:
                std["stdout"] += result.stdout.decode('utf-8')
                std["stderr"] += result.stderr.decode('utf-8')
                return 2
    except subprocess.TimeoutExpired:
        print(colors.fg.red+str(test_nb)+". Failed by time out")
        print(colors.fg.red +"   "+ str(cmd))
        return 2

def DispResume(fail, stats_op, num):
    if fail == 0:
        print(colors.fg.green + colors.bold + "===== " + str(num)+" Numbers =====\n"+ colors.reset + colors.fg.green +" - All tests passed (with max points)")
    elif fail == 1:
        print(colors.fg.yellow + colors.bold + "===== " + str(num)+" Numbers =====\n"+ colors.reset + colors.fg.yellow +" - All tests passed (but without max points)")
    else:
        print(colors.fg.red + colors.bold + "===== " + str(num)+" Numbers =====\n"+ colors.reset + colors.fg.red +" Failed")
    print(colors.fg.pink +"    min: "+str(min(stats_op))+"   max: "+str(max(stats_op)) + "   median: "+str(int(statistics.median(stats_op))))
    print(colors.reset +"\n")

def DispResumeFail(fail):
    if fail == 0:
        print(colors.fg.green + colors.bold + "===== Special cases =====\n" + colors.reset + colors.fg.green +" - All tests passed")
    else:
        print(colors.fg.red + colors.bold + "===== Special cases =====\n" + colors.reset + colors.fg.red +" - Failed")
    print(colors.reset +"\n")

def Tester(i, val, ch, test):
    fail = 0
    out = 0
    stats_op = []
    a = 0
    while a < test:
        cmd = GenerateRdm(ch, val)
        cmd.insert(0, './push_swap')
        out = RunPushSwap(i, cmd, stats_op)
        if out > fail:
            fail = out
        a += 1
        i += 1
    DispResume(fail, stats_op, val)
    return i


def FailTest(cmd, i, type_res, err_msg, fail):
    std = {"stdout": "", "stderr": ""}
    correc_stdout = ""
    correc_stderr = ""
    out = RunPushSwapFail(cmd, i, type_res, std)
    if out > 0:
        print(colors.fg.red + str(i) + err_msg)
        print(colors.fg.purple + "Your program: ")
        print(colors.fg.yellow + "   stdout: " + std["stdout"].replace("\n", "\\n"))
        print(colors.fg.darkgrey + "   stderr: " + std["stderr"].replace("\n", "\\n"))
        if type_res == 1:
             correc_stderr = "Error\n"
        print("")
        print(colors.fg.purple +"Expected: " + colors.reset)
        print(colors.fg.yellow + "   stdout: " + correc_stdout.replace("\n", "\\n"))
        print(colors.fg.darkgrey + "   stderr: " + correc_stderr.replace("\n", "\\n"))
        print("")
    if out > fail:
        fail = out
    return fail

def FailTester(i):
    fail = 0

    # ===  empty  ===
    fail = FailTest(['./push_swap'], i, 0, ". Failed (bad output), If no parameter is specified, the program should ont display anything", fail)
    i += 1

    # ===  duplicate  ===
    fail = FailTest(['./push_swap', 5, 4, 120, 885, -7, 120], i, 1, ". Failed If there are duplicates in the input list the program should return \"Error\" followed by a '\\n' on the "+colors.bold+"error output (stderr)", fail)
    i += 1
    fail = FailTest(['./push_swap', -5, 5644, 5, -5, 84561], i, 1, ". Failed If there are duplicates in the input list the program should return \"Error\" followed by a '\\n' on the "+colors.bold+"error output (stderr)", fail)
    i += 1

    # ===  not numbers  ===
    fail = FailTest(['./push_swap', 450, 22, 13, 'a', 1860], i, 1, ". Failed If some parameters are not numbers in the input list the program should return \"Error\" followed by a '\\n' on the "+colors.bold+"error output (stderr)", fail)
    i += 1
    fail = FailTest(['./push_swap', '\n', 566465, 65165, 4647, 1, -4564], i, 1, ". Failed If some parameters are not numbers in the input list the program should return \"Error\" followed by a '\\n' on the "+colors.bold+"error output (stderr)", fail)
    i += 1

    # ===  out of int range  ===
    fail = FailTest(['./push_swap', 984, 88, -31, 2147483648, 45], i, 1, ". Failed If some numbers don't fit in an int in the input list the program should return \"Error\" followed by a '\\n' on the "+colors.bold+"error output (stderr)", fail)
    i += 1
    fail = FailTest(['./push_swap', -2147483649, 98, 4665, 124, 768], i, 1, ". Failed If some numbers don't fit in an int in the input list the program should return \"Error\" followed by a '\\n' on the "+colors.bold+"error output (stderr)", fail)
    i += 1
    DispResumeFail(fail)
    return i

print(colors.bold + colors.fg.green+"/* ************************************************************************ *\\")
print(colors.bold + colors.fg.green+"/*"+"\x1b[35m"+"   _____   _____   ____             _       ______                        "+colors.bold + colors.fg.green+"*\\")
print(colors.bold + colors.fg.green+"/*"+"\x1b[35m"+"  |  __ \ / ____| |  _ \           | |     |  ____|                       "+colors.bold + colors.fg.green+"*\\")
print(colors.bold + colors.fg.green+"/*"+"\x1b[35m"+"  | |__) | (___   | |_) |_ __ _   _| |_ ___| |__ ___  _ __ ___ ___ _ __   "+colors.bold + colors.fg.green+"*\\")
print(colors.bold + colors.fg.green+"/*"+"\x1b[35m"+"  |  ___/ \___ \  |  _ <| '__| | | | __/ _ \  __/ _ \| '__/ __/ _ \ '__|  "+colors.bold + colors.fg.green+"*\\")
print(colors.bold + colors.fg.green+"/*"+"\x1b[35m"+"  | |     ____) | | |_) | |  | |_| | ||  __/ | | (_) | | | (_|  __/ |     "+colors.bold + colors.fg.green+"*\\")
print(colors.bold + colors.fg.green+"/*"+"\x1b[35m"+"  |_|    |_____/  |____/|_|   \__,_|\__\___|_|  \___/|_|  \___\___|_|     "+colors.bold + colors.fg.green+"*\\")
print(colors.bold + colors.fg.green+"/*"+"\x1b[35m"+"                                                                          "+colors.bold + colors.fg.green+"*\\")
print(colors.bold +colors.fg.green+"/* ************************************************************************ *\\")


#print(colors.bold + colors.fg.green+"/* ***************************************************************************************************************************************** *\\")
#print(colors.bold + colors.fg.green+"/*"+"\x1b[35m"+"    _______    ______         _______                         __                ________                                                   "+colors.bold + colors.fg.green+"*\\")
#print(colors.bold + colors.fg.green+"/*"+"\x1b[35m"+"   /       \  /      \       /       \                       /  |              /        |                                                  "+colors.bold + colors.fg.green+"*\\")
#print(colors.bold + colors.fg.green+"/*"+"\x1b[35m"+"   $$$$$$$  |/$$$$$$  |      $$$$$$$  |  ______   __    __  _$$ |_     ______  $$$$$$$$/______    ______    _______   ______    ______     "+colors.bold + colors.fg.green+"*\\")
#print(colors.bold + colors.fg.green+"/*"+"\x1b[35m"+"   $$ |__$$ |$$ \__$$/       $$ |__$$ | /      \ /  |  /  |/ $$   |   /      \ $$ |__  /      \  /      \  /       | /      \  /      \    "+colors.bold + colors.fg.green+"*\\")
#print(colors.bold + colors.fg.green+"/*"+"\x1b[35m"+"   $$    $$/ $$      \       $$    $$< /$$$$$$  |$$ |  $$ |$$$$$$/   /$$$$$$  |$$    |/$$$$$$  |/$$$$$$  |/$$$$$$$/ /$$$$$$  |/$$$$$$  |   "+colors.bold + colors.fg.green+"*\\")
#print(colors.bold + colors.fg.green+"/*"+"\x1b[35m"+"   $$$$$$$/   $$$$$$  |      $$$$$$$  |$$ |  $$/ $$ |  $$ |  $$ | __ $$    $$ |$$$$$/ $$ |  $$ |$$ |  $$/ $$ |      $$    $$ |$$ |  $$/    "+colors.bold + colors.fg.green+"*\\")
#print(colors.bold + colors.fg.green+"/*"+"\x1b[35m"+"   $$ |      /  \__$$ |      $$ |__$$ |$$ |      $$ \__$$ |  $$ |/  |$$$$$$$$/ $$ |   $$ \__$$ |$$ |      $$ \_____ $$$$$$$$/ $$ |         "+colors.bold + colors.fg.green+"*\\")
#print(colors.bold + colors.fg.green+"/*"+"\x1b[35m"+"   $$ |      $$    $$/       $$    $$/ $$ |      $$    $$/   $$  $$/ $$       |$$ |   $$    $$/ $$ |      $$       |$$       |$$ |         "+colors.bold + colors.fg.green+"*\\")
#print(colors.bold + colors.fg.green+"/*"+"\x1b[35m"+"   $$/        $$$$$$/        $$$$$$$/  $$/        $$$$$$/     $$$$/   $$$$$$$/ $$/     $$$$$$/  $$/        $$$$$$$/  $$$$$$$/ $$/          "+colors.bold + colors.fg.green+"*\\")
#print(colors.bold + colors.fg.green+"/*"+"\x1b[35m"+"                                                                                                                                           "+colors.bold + colors.fg.green+"*\\")
#print(colors.bold +colors.fg.green+"/* ***************************************************************************************************************************************** *\\")
print("\n")
os.chdir("..")

if MakeAll() != 1:
    print(colors.reset+colors.fg.darkgrey+  " __________________________________________________")
    print(colors.fg.darkgrey+               "│                                                  │")
    print(colors.fg.darkgrey+               "│                  "+colors.reset+ "MANDATORY PART"+colors.fg.darkgrey+"                  │")
    print(colors.fg.darkgrey+               "│                                                  │")
    print(colors.fg.darkgrey+               " ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾ ")
    i = 1
    i = FailTester(i)
    i = Tester(i, 2,    0,  250)
    i = Tester(i, 3,    0,  250)
    i = Tester(i, 5,    0,  250)
    i = Tester(i, 100, 0,  250)
    i = Tester(i, 500, 0,  250)
