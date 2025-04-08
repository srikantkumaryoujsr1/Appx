import time
import math
import os
from pyrogram.errors import FloodWait

from datetime import datetime,timedelta

class Timer:
    def __init__(self, time_between=5):
        self.start_time = time.time()
        self.time_between = time_between

    def can_send(self):
        if time.time() > (self.start_time + self.time_between):
            self.start_time = time.time()
            return True
        return False



#lets do calculations
def hrb(value, digits= 2, delim= "", postfix=""):
    """Return a human-readable file size.
    """
    if value is None:
        return None
    chosen_unit = "B"
    for unit in ("KiB", "MiB", "GiB", "TiB"):
        if value > 1000:
            value /= 1024
            chosen_unit = unit
        else:
            break
    return f"{value:.{digits}f}" + delim + chosen_unit + postfix

def hrt(seconds, precision = 0):
    """Return a human-readable time delta as a string.
    """
    pieces = []
    value = timedelta(seconds=seconds)
    

    if value.days:
        pieces.append(f"{value.days}d")

    seconds = value.seconds

    if seconds >= 3600:
        hours = int(seconds / 3600)
        pieces.append(f"{hours}h")
        seconds -= hours * 3600

    if seconds >= 60:
        minutes = int(seconds / 60)
        pieces.append(f"{minutes}m")
        seconds -= minutes * 60

    if seconds > 0 or not pieces:
        pieces.append(f"{seconds}s")

    if not precision:
        return "".join(pieces)

    return "".join(pieces[:precision])



timer = Timer()

# Powered By Ankush
async def progress_bar(current, total, reply, start, message_thread_id):
    if timer.can_send():
        now = time.time()
        diff = now - start
        if diff < 1:
            return
        else:
            perc = f"{current * 100 / total:.1f}%"
            elapsed_time = round(diff)
            speed = current / elapsed_time
            remaining_bytes = total - current
            if speed > 0:
                eta_seconds = remaining_bytes / speed
                eta = hrt(eta_seconds, precision=1)
            else:
                eta = "-"
            sp = str(hrb(speed)) + "/s"
            tot = hrb(total)
            cur = hrb(current)
            bar_length = 11
            completed_length = int(current * bar_length / total)
            remaining_length = bar_length - completed_length
            progress_bar = "▓" * completed_length + "▒" * remaining_length

            try:
                await reply.edit(f'\n ╭──⌯📤𝐔𝐩𝐥𝐨𝐚𝐝𝐢𝐧𝐠📤⌯──╮ \n├✦ {progress_bar}|﹝{perc}﹞ \n├✦ 𝐬𝐩𝐞𝐞𝐝 ➠ {sp} \n├✦ 𝐏𝐫𝐨𝐜𝐞𝐬𝐬𝐞𝐝 ➠ {cur}\n├✦ 𝐒𝐢𝐳𝐞 ➛ 𝐄𝐓𝐀 ➠ {tot} - {eta} \n╰─═❤️ᴍʀ_ʜᴀᴄᴋᴇʀ❤️═─╯\n', reply_to_message_id=message_thread_id) 
            except FloodWait as e:
                time.sleep(e.x)
