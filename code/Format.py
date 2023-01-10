HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'


def printHeader(line: str, end='\n'):
    print(f"{HEADER}{line}{RESET}", end=end)

def printTest(line: str):
    print(f"{OKBLUE}{line}{RESET}")

def printText(line: str):
    print(f"{OKCYAN}{line}{RESET}")

def printWarning(line: str):
    print(f"{WARNING}WARNING: {RESET}{line}")

def printError(line: str):
    print(f"{FAIL}ERROR: {RESET}{line}")

def printPass():
    print(f"{OKGREEN}PASS{RESET}", end='')

def printFail():    
    print(f"{FAIL}FAIL{RESET}", end='')

