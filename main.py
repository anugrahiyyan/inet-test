import subprocess
import re
import time
import datetime

downtime_count = 0

def get_ping_time():
    try:
        output = subprocess.check_output(["ping", "-c", "1", "google.com"], universal_newlines=True)
        reply_lines = [line for line in output.splitlines() if "time=" in line]
        if reply_lines:
            ip_address = reply_lines[0].split()[2].strip("()")
            match = re.search(r"time=(\d+\.?\d*) ms", output)
            if match:
                avg_ping = float(match.group(1))
                return avg_ping, ip_address
            else:
                print("Ping failed. Could not find 'time=' in output.")
                return None, None
        else:
            print("Ping failed. No replies received.")
            return None, None
    except subprocess.CalledProcessError as e:
        current_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        print(f"[{current_time}] Error detected: Please Check the Main Cable or Hub!!")
        return None, None

def send_beep_alert():
    try:
        subprocess.run(['beep', '-f', '1000', '-l', '500'], check=True)
    except Exception as e:
        print(f"Beep alert failed: {e}")

if __name__ == "__main__":
    while True:
        ping_time, ip_address = get_ping_time()
        if ping_time is not None:
            if ping_time > 990:
                current_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                print(f"[{current_time}] Count: {downtime_count} | Ping : {ping_time} ms | <<---Critical--->> | ==========> Sending to system alert...")
                send_beep_alert()
            elif ping_time > 550:
                current_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                print(f"[{current_time}] Count: {downtime_count} | Ping : {ping_time} ms | <<---Warning--->>")
                send_beep_alert()
            else:
                downtime_count = 0
                current_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                print(f"[{current_time}] Connected to --> {ip_address} {ping_time} ms | Should we sleep yet ? || <<---Good--->> ||")
        else:
            current_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            downtime_count += 1
            print(f"[{current_time}] Downtime count: {downtime_count} | WHAT THE HELL, Look at your INTERNET dude. It's Totally Shutdown || <<---Critical--->> || ==========> Sending to system alert...")
            send_beep_alert()

        time.sleep(5 if ping_time is None else 1)
