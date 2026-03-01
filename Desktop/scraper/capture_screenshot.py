#!/usr/bin/env python3
import subprocess
import time
import mss
import os

time.sleep(2)

with mss.mss() as sct:
    filename = sct.shot(mon=-1, output='screenshot-main.png')
    print(f"Screenshot saved to: {filename}")
