import subprocess
import re
import time
import datetime
import os

downtime_count = 0
last_status = None  # Track the last status to avoid repetitive alerts

def get_ping_time():
    try:
        output = subprocess.check_output(["ping", "-c", "3", "google.com"], universal_newlines=True)
        reply_lines = [line for line in output.splitlines() if "from" in line]

        if reply_lines:
            ip_address_match = re.search(r'\(([\d.]+)\)', reply_lines[0])
            if ip_address_match:
                ip_address = ip_address_match.group(1)
                avg_ping_match = re.search(r'time=(\d+\.?\d*) ms', reply_lines[0])
                if avg_ping_match:
                    avg_ping = float(avg_ping_match.group(1))
                    return avg_ping, ip_address
            return None, None
        return None, None

    except subprocess.CalledProcessError:
        current_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        print(f"[{current_time}] Error detected: Please check the main cable or hub!")
        return None, None

def alert_sound():
    os.system('echo -e "\a"')

if __name__ == "__main__":
    while True:
        ping_time, ip_address = get_ping_time()
        current_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        if ping_time is not None:
            if ping_time > 990:
                if last_status != "critical":
                    print(f"[{current_time}] Ping : {ping_time} ms | <<---Critical--->> | ==========> System alert...")
                    alert_sound()
                downtime_count += 1
                last_status = "critical"
            elif ping_time > 550:
                if last_status != "warning":
                    print(f"[{current_time}] Ping : {ping_time} ms | <<---Warning--->>")
                downtime_count += 1
                last_status = "warning"
            else:
                if last_status != "good":
                    downtime_count = 0
                    print(f"[{current_time}] Connected to --> {ip_address} {ping_time} ms | <<---Good--->>")
                last_status = "good"
        else:
            downtime_count += 1
            if last_status != "down":
                print(f"[{current_time}] Downtime count: {downtime_count} | INTERNET IS DOWN || <<---Critical--->>")
                alert_sound()
            last_status = "down"

        # Adjust sleep time based on network conditions
        if last_status == "good":
            time.sleep(5)  # Longer interval for good status
        else:
            time.sleep(1)  # Shorter interval for critical states
