import subprocess
import re
import time
import datetime
import os

downtime_count = 0

def get_ping_time():
    try:
        # Ping for Linux (use `-c` for count and `-W` for timeout)
        output = subprocess.check_output(["ping", "-c", "1", "google.com"], universal_newlines=True)
        reply_lines = [line for line in output.splitlines() if "from" in line]
        if reply_lines:
            ip_address_match = re.search(r'from ([\d.]+)', reply_lines[0])
            if ip_address_match:
                ip_address = ip_address_match.group(1)
                avg_ping_match = re.search(r'time=(\d+\.?\d*) ms', reply_lines[0])
                if avg_ping_match:
                    avg_ping = float(avg_ping_match.group(1))
                    return avg_ping, ip_address
            else:
                print("Failed to extract IP address.")
                return None, None
        else:
            print("Ping failed. No replies received.")
            return None, None

    except subprocess.CalledProcessError:
        current_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        print(f"[{current_time}] Error detected: Please check the main cable or hub!")
        return None, None

def alert_sound():
    # Make a beep sound on Linux
    os.system('echo -e "\a"')

if __name__ == "__main__":
    while True:
        ping_time, ip_address = get_ping_time()
        current_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        if ping_time is not None:
            if ping_time > 990:
                print(f"[{current_time}] Count: {downtime_count} | Ping : {ping_time} ms | <<---Critical--->> | ==========> Sending to system alert...")
                alert_sound()
                downtime_count += 1
            elif ping_time > 550:
                print(f"[{current_time}] Count: {downtime_count} | Ping : {ping_time} ms | <<---Warning--->>")
                downtime_count += 1
            else:
                downtime_count = 0
                print(f"[{current_time}] Connected to --> {ip_address} {ping_time} ms | <<---Good--->>")
        else:
            downtime_count += 1
            print(f"[{current_time}] Downtime count: {downtime_count} | INTERNET IS DOWN || <<---Critical--->> ||")
            alert_sound()

        # Wait for 1 second between each ping check or 5 seconds if there's no internet
        time.sleep(1 if ping_time is not None else 5)
