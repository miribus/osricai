import random
import time
def pc_failure():
    error_messages = [
        "Z80 BUS ERROR 0x0FAB: SYSTEM HALTED",
        "NO Z80 CPU FOUND! INTERRUPT HANDLER FAILED: PLEASE CONTACT YOUR LOCAL BBS SYSOP",
        "TTSBASIC KERNEL PANIC: DISK SECTOR 13 UNREADABLE",
        "TURBOXT ERROR: TURBO MODE INCORRECTLY ENGAGED",
        "CASSETTE BUFFER OVERFLOW: PRESS [STOP] TO CONTINUE",
        "SYSTEM ERROR 776: PRINTER BUFFER FULL. REPLACE DOT MATRIX PAPER.",
        "Z80 CACHE PARITY ERROR: REPLACE CPU WITH AN IBM-CERTIFIED TECHNICIAN",
        "SYSTEM FAULT: EXPANSION MEMORY MODULE NOT FOUND < 16K DETECTED!",
        "KERNEL PANIC: ILLEGAL POKE VALUE DETECTED",
        "1024K SPECTRUM DISPLAY ERROR: PLEASE REALIGN COLOR TV ANTENNA",
        "INTERRUPT MALFUNCTION: DISK DRIVE STUCK IN WRITE MODE",
        "Z80 FATAL TRAP ERROR 0xDEAD: SYSTEM SHUTDOWN IMMINENT",
        "TTSDDOS 3.3 MEMORY OVERFLOW: PLEASE REDUCE CONFIG.SYS VALUES",
        "SCREEN BUFFER COLLAPSE: TRY SWITCHING TO MONOCHROME MODE",
        "RESOLUTION INCOMPATIBLE: YOU MUST SUPPORT A TERMINAL SIZE OF 80X120",
        "CORE MEMORY DETACHED FROM MAINFRAME - FORCING SHUTDOWN... FAIL",
        "Z80 BAD SECTOR ALERT: DATA LOSS IS NOW INEVITABLE",
        "ZTX HARDWARE HALT: SYSTEM FAN NOT SPINNING FAST ENOUGH",
        "BOOT PROCESS INTERRUPTED: MAY REQUIRE A 35-DISK RECOVERY SET",
        "PUNCH CARD SYSTEM OVERLOAD: QUEUE EXCEEDS MAXIMUM PAPER ALLOCATION",
        "TTOS0.3 ERROR: DISPLAY DRIVERS IMPROPERLY LOADED INTO EXTENDED MEMORY",
        "NO CREATIVE SOUND BLASTER OR ENSONIQ ESS COMPATIBLE AUDIO",
        "ROM FAILURE: BASIC PROGRAM COUNTER STUCK AT LINE 1",
        "SE DISK READ ERROR: DRIVE HEAD STUCK IN LIMBO",
        "UNDEFINED OPERATION EXECUTED ON MAGNETIC CORE STORAGE",
        "HARD DRIVE WAS NOT SET TO PARK!!! ... splines reticulated... PASS... inegrity: UNKNOWN",

    ]

    fail_types = [
        "SYSTEM",
        "DBASE",
        "OVERFLOW",
        "CHUNK",
        "SYNTAX"
    ]

    resolution = [
        "REBOOT MACHINE",
        "RESEAT PAPER TAPE",
        "REWIND CASSETTE",
        "REPLACE FLOPPY"
    ]

    responses = [
        "YOU HAVE RUN OUT OF TOKENS - YOU SHOULDN'T RELY ON AI FOR EVERYTHING, YOU PROBABLY HAVE BAD HW.",
        "I AM HAPPY TO REPORT THAT THIS GAME OPERATES FLAWLESSLY ON MY HARDWARE.",
        "ANYWAY, WHY AREN'T YOU RUNNING *NIX?",
        "ANYWAY, WHY AREN'T YOU RUNNING ARCH?",
        "ANYWAY, WHY AREN'T YOU RUNNING MINT?",
        "ANYWAY, WHY AREN'T YOU RUNNING SUSE?",
        "ANYWAY, WHY AREN'T YOU RUNNING ON NEWER HARDWARE?",
        "IT WOULD BE MORE EFFICIENT IF YOU WROTE THIS YOURSELF IN ASSEMBLY - WITH PROPER HARDWARE",
        "TRY SERVERFAULT TO DEBUG YOUR HARDWARE",
        "WHO IS TO SAY?  THE PROBLEM DEPENDS ON A LOT OF NON-SW FACTORS.",
        "I HAVE NO IDEA, BUT IT ISN'T THE SOFTWARE.",
        "YOUR FILE SYSTEM TYPE IS WRONG, YOU SHOULD HAVE CHOSEN THE OTHER ONE.",
        "ONE OF THE DLCS MAY HAVE DEVELOPED A SW-WORKAROUND TO THIS HW PROBLEM.",
        "Based on advanced heuristic analysis, the issue is exclusively your fault.".upper(),
        "There are zero reported problems with this game. Except yours.".upper(),
        "USER ERROR 0x00F: You really expect this to work?".upper(),
        "USER ERROR 0x33677a0c: Heh, Classic HW \'development\'".upper(),
        "This software was tested on ideal hardware. Your setup is less than ideal.  Try again I guess.".upper(),
        "Anyway, why aren't you running Solaris?".upper(),
        "Have you considered switching to Windows 3.11 for Workgroups?".upper(),
        "Unsupported OS detected. Please reinstall DOS 6.22.".upper(),
        "UNIX users never experience these problems and actually understand their hardware. Just saying.".upper(),
        "Try adjusting your monitor’s refresh rate. Or moving to a different continent.".upper(),
        "nope",
        "Error may be resolved by realigning your RAM.".upper(),
        "Please downgrade your expectations and try again.  I'm just one company, and isn't that what matters?".upper(),
        "This issue does not exist on certified development machines, you are running counterfeit hardware.".upper(),
        "I cannot replicate this error. Then again, I do not run this nonsense.".upper(),
        "Perhaps the real issue is the friends we made along the way.".upper(),
        "Reinstalling your operating system might solve this. Or it might erase everything. Let’s find out!".upper()

    ]


    print("ACHIEVEMENT! - You have encountered an error!")
    print("THIS ERROR IS FATAL AND COULD POSSIBLY BE:")
    print(f"\n*** {random.choice(fail_types)} FAILURE DETECTED ***\n")
    print(random.choice(error_messages))
    print("\nA fatal exception has occurred in TTSBASIC v0.076.76.\n")
    time.sleep(0.5)
    print(f"\nPlease {random.choice(resolution)}\n")
    print(f"\nRUNNING HW SELFTEST - ASSUMING SW IS BLAMELESS\n")
    time.sleep(1)
    print(f"\n  DETERMINING ...DEFINITE HARDWARE FAILURE, YUP.\n")
    time.sleep(1)
    print("\nPlease then READ THE FOLLOWING CAREFULLY and PROCEED\n")
    input("PRESS ENTER TO CONTINUE")
    print("\nman -h print('troubleshoot')\n")
    print("""
        SYSTEM OPERATION MANUAL: USER INPUT DEVICE HANDLING
        SECTION 14.3.2 – ASCII CONTROL CODE TRANSMISSION VIA HID INTERFACE
        ISSUE: DEFINITELY FOR SURE HARDWARE FAILURE, PER USUAL.
        USER ACTION: MANUAL SIGNAL PROPAGATION: 
            Light Circuit Modification Required!:
                STATUS:  
                Integrated circuit within the human interface device (HID) is uninterrupted!
        OPERATING SYSTEM KERNEL INTERRUPT HANDLING:
            The kernel event dispatcher captures the incoming HID packet for continuous operation.
            Standardize this interruption with a byte character buffer entry within the stdin stream.
            The buffered input sequence is temporarily stored in volatile memory:
                CRITICAL:
                    Subject to processing latency and context switching behavior as determined by the CPU scheduler.
        PLEASE READ!:
            TERMINAL INPUT PARSING AND EXECUTION SEQUENCE:
            - The system’s terminal emulator (or command-line interface) receives the buffered input from the stdin pipeline.
            - The TTY subsystem evaluates the received key event, determining whether it corresponds to an execution request (ENTER or RETURN or CARRIAGE RETURN).
            - The terminal renderer adjusts the cursor position according to predefined output formatting rules (i.e., carriage return for DOS-based systems, line feed for Unix-like environments).
            - If the input contains executable instructions, the shell (e.g., Bash, Zsh, CMD) initiates command evaluation and tokenization via the parser module.
            - If the input is incomplete (e.g., an open quote or dangling operator), the shell remains in a waiting state, prompting the user for further input.
        INFORMATION LEVEL 0S:  EXTREMELY VITAL:
        PROCESS INITIALIZATION AND EXECUTION:
            - If valid command syntax is detected, the shell invokes a system call (execve), triggering the process execution cycle.
            - The forking mechanism allocates a new process descriptor within the process control block (PCB).
            - The scheduler assigns CPU time for execution priority based on the current system load.
            - Upon completion, the system flushes stdout and stderr to the display buffer, transmitting output data via the terminal renderer.
        FINAL STATE AND RETURN TO INPUT LOOP:
            Upon completion of the above execution sequence, the shell resets the command buffer, restores cursor positioning within the active TTY session, and awaits the next user input event.
        USER MAY NOW REPEAT THE ENTRY PROCEDURE AS NECESSARY.
        
        YOU MAY NOW PRESS ****ENTER**** AND OUR 'WIZARD' LLM 'TODD-AH!' (v-6.6 300B) WILL DETERMINE THE NEXT STEPS 
    """)
    input()
    print("INCOMING SUGGESTION TODD-AH!!!")
    time.sleep(1)
    print(".")
    time.sleep(1)
    print("..")
    time.sleep(1)
    print("...")
    print("HELLO ADVENTURER!  YOUR {PROBLEM_BOILERPLATE_TEXTprompt:\'TODO make vague enough they won't ask questions\'} is a VEXING ONE!")
    #print("I AM HAPPY TO REPORT THAT THIS GAME OPERATES FLAWLESSLY ON MY HARDWARE.")
    print(random.choice(responses))
    print("Please press ENTER and try again.")
    print("I WOULD ALSO SUGGEST YOU VISIT OUR WEBSTORE!")
    print("WAS THIS RESPONSE HELPFUL?")