import bootup
import movements_monsters

# bootup.fake_bootloader()
print("SYSTEM TESTS STARTING... PRESS CTRL+S to skip")
# mem = bootup.get_system_memory()
# stor = bootup.get_disk_space()
# bootup.fake_memory_test(mem)
# bootup.fake_storage_test(stor)

screen = """
     ██████╗ ███████╗██████╗ ██╗ ██████╗ █████╗ ██╗
    ██╔═══██╗██╔════╝██╔══██╗██║██╔════╝██╔══██╗██║
    ██║   ██║███████╗██████╔╝██║██║     ███████║██║
    ██║   ██║╚════██║██╔══██║██║██║     ██╔══██║██║
    ╚██████╔╝███████║██║  ██║██║╚██████╔██║  ██║██║
     ╚═════╝ ╚══════╝╚═╝     ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝
--------------------------------------------------------
        ENDLESS ADVENTURES IN 9600t
--------------------------------------------------------
PRESS ENTER TO CONTINUE  |  SYSTEM REPAIR MAY BE REQUIRED
"""
print("Starting OSRICAI Dungeon Systems - PRESENTS...\n")
input(screen)
movements_monsters.rungame()


