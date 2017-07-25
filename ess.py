from time import sleep

SLEEP_TIME = 0.05
SLEEP_TIME_L = 0.08

def printSleep(str):
	print(str)
	sleep(SLEEP_TIME)

def printSleepL(str):
	print(str)
	sleep(SLEEP_TIME_L)

for i in range(5):
	printSleep("   /    /")
	printSleep("  /    /")
	printSleep(" /    /")
	printSleep("|    |")
	printSleep(" \    \\")
	printSleep("  \    \\")
	printSleep("   \    \\")
	printSleep("    |    |")
	printSleep("   /    /")
	printSleep("  /    /")
	printSleep(" /    /")
	printSleep("|    |")
	printSleep(" \    \\")
	printSleep("  \    \\")
	printSleep("   \    \\")
	printSleep("    |    |")

sleep(SLEEP_TIME * 20)

for i in range(5):
	printSleepL("   /    /")
	printSleepL("  /    /")
	printSleepL(" |    |")
	printSleepL("  \    \\")
	printSleepL("   \    \\")
	printSleepL("    |    |")
	printSleepL("   /    /")
	printSleepL("  /    /")
	printSleepL(" |    |")
	printSleepL("  \    \\")
	printSleepL("   \    \\")
	printSleepL("    |    |")
