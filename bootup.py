import psutil
import time
import random
import keyboard

def fake_storage_test(total_storage_mb, sector_size=4):
    """Fake storage test, checking sectors for integrity."""
    print("\nDISK INITIALIZATION SEQUENCE...")
    time.sleep(1)
    print(f"Primary Storage Device: {total_storage_mb} MB Detected")
    print("Initiating Sector Integrity Scan...\n")

    tested = 0
    while tested < total_storage_mb:
        print(f"[PRESS CTRL+S to skip] Checking sector {tested}-{tested + sector_size} MB... ", end="")
        time.sleep(random.uniform(0.05, 0.15))  # Simulated delay
        if random.randint(0, 100) < 7:  # Occasionally fake a bad sector
            print("[WARNING] Bad sector detected. Recovering...")
            time.sleep(0.5)
            print("Recovery complete.") if random.randint(0, 100) > 30 else print("[FAILURE] Sector permanently damaged.")
        else:
            print(" OK")

        tested += sector_size

        # Allow early termination with Ctrl+D
        if keyboard.is_pressed('ctrl+s'):
            print("\n[USER OVERRIDE] Storage Test Aborted! Proceeding to Startup...\n")
            print("\n... PLEASE NOTE YOU WILL BE RUNNING WITH UNVERIFIED PROBABLY DEFECTIVE HARDWARE...\n")
            print("\n... THIS WILL BE RECORDED...\n")
            print("\nACHIEVEMENT!:  EXTREME RISK TAKER! REPORT ANY ERRORS TO localhost")
            break
    if tested == total_storage_mb:
        print("\nFILESYSTEM TEST:  OK... However the rest of your hardware could still cause a problem.")

    print("\nStorage Test Complete. Booting OSRICAI...\n")
    time.sleep(2)

def get_disk_space():
    """Retrieve total disk space in MB to simulate an old-school BIOS storage check."""
    disk_info = psutil.disk_usage('/')
    disk_mb = disk_info.total // (1024 * 1024)  # Convert bytes to MB
    return disk_mb

def get_system_memory():
    """Retrieve system memory in KB (for retro effect)."""
    mem_bytes = psutil.virtual_memory().total
    mem_kb = mem_bytes // 1024  # Convert to KB for that old-school effect
    return mem_kb

def fake_memory_test(total_memory_kb, block_size=256):
    """Fake memory test, 256 bytes at a time."""
    print("\nTTS-BIOS v0.99 (C) TURBOXT SYSTEMS 1976-1980\n")
    print(f"System RAM Detected: {total_memory_kb} KB")
    print("Initiating Memory Test...\n")

    tested = 0
    passes = 0
    while tested < total_memory_kb:
        print(f"[PRESS CTRL+S to skip] Testing block {tested}-{tested + block_size} KB... PASS", end="")
        time.sleep(random.uniform(0.45, 0.75))  # Simulated delay
        if random.randint(0, 100) < 5:  # Occasionally fake an issue
            print("[WARNING] Non-critical memory allocation inconsistency detected")
        else:
            print(" OK")
        tested += block_size
        passes += 1

        # Allow early termination with Ctrl+S
        if keyboard.is_pressed('ctrl+s'):
            print("\n[USER OVERRIDE] Testing Aborted! Proceeding to Startup...\n")
            print("\n... PLEASE NOTE YOU WILL BE RUNNING WITH UNVERIFIED PROBABLY DEFECTIVE HARDWARE...\n")
            print("\n... THIS WILL BE RECORDED...\n")
            print("\nACHIEVEMENT!:  Playing on untested hardware, don't blame me!")
            break

    if tested == total_memory_kb:
        print("\nALL MEMORY TEST:  OK... However the rest of your hardware could still cause a problem.")

    print("\nMemory Test Complete. Booting OSRICAI...\n")
    time.sleep(2)

def fake_bootloader():
    print("TURBOXT BOOTLOADER v1.42")
    time.sleep(.5)
    print("Loading Kernel...        █ Done!")
    time.sleep(.5)
    print("Verifying Objects...     ██ Done!")
    time.sleep(.5)
    print("Verifying Attributes...  ███ Done!")
    time.sleep(.5)
    print("Compiling Shaders...     ████ Done!")
    time.sleep(.5)
    print("ReCompiling Kernel...    █████ Done!")
    time.sleep(.5)
    print("Detecing Screen Size...  ██████ Full 9600t support!")
    time.sleep(.5)
    print("Optimizing FileSystem... ██████████ Done!")
    time.sleep(.5)
    print("Starting OSRICAI Dungeon Systems HW SCAN...\n")
    time.sleep(.5)

