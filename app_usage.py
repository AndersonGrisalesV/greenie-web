#!/usr/bin/env python3

import psutil
import datetime
import time
import schedule
import openpyxl
import platform
from tqdm import tqdm
from time import sleep
import signal
import sys

# Define a simple linear model parameters
# These values are purely for demonstration purposes and are not accurate
CPU_POWER_COEFFICIENT = 0.02  # Coefficient to relate CPU usage to power consumption
BASE_POWER = 10  # Base power consumption

def estimate_power_usage(cpu_usage):
    # Estimate power consumption based on CPU usage using a simple linear model
    estimated_power = BASE_POWER + (CPU_POWER_COEFFICIENT * cpu_usage)
    return estimated_power

def main():
    pid = int(input("Enter process ID: "))
    
    def exit_program(signal, frame):
        # print("\nExiting the program...")
        sys.exit(0)
    
    # Set up the signal handler for Ctrl + C
    signal.signal(signal.SIGINT, exit_program)
    
    # Schedule the monitoring task
    p = psutil.Process(pid)
    process_name = p.name() 
    schedule.every(5).seconds.do(monitor_with_progress, pid, process_name)
  
    try:
        
        while True:
            schedule.run_pending()
            time.sleep(1)
    except Exception as e:
        print("An error occurred:", e)

def monitor_with_progress(pid, process_name):
    print("Monitoring process:", process_name)
    sleep(1)
    with tqdm(total=100, desc='% CPU USAGE: ', position=0) as cpubar, tqdm(total=100, desc='% GPU USAGE: ', position=1) as gpubar, tqdm(total=100, desc='% RAM USAGE: ', position=2) as rambar, tqdm(total=100, desc='% POWER CONSUMPTION: ', position=3) as powerconbar:
        try:
            while True:
                current_time = datetime.datetime.now().strftime("%Y%m%d - %H:%M:%S")
                p = psutil.Process(pid)
                process_name = p.name() 
                cpu = p.cpu_percent(interval=1) / psutil.cpu_count()
                cpu_usage = p.cpu_percent(interval=1) / psutil.cpu_count()
                memory = p.memory_percent()  
                memory_formatted = f"{memory:.2f}"
                gpu_usage = 0

            

                cpubar.n = cpu
                gpubar.n = gpu_usage
                rambar.n = memory
                powerconbar.n = cpu_usage

                cpubar.refresh()
                gpubar.refresh()
                rambar.refresh()
                powerconbar.refresh()


                path = "Monitor_Result.xlsx"

                try:
                    file = openpyxl.load_workbook(path)
                except FileNotFoundError:
                    file = openpyxl.Workbook()

                sheet = file.active
                if sheet.cell(1, 1).value is None:
                    sheet.cell(column=1, row=1, value="Date & Time")
                    sheet.cell(column=2, row=1, value="Process ID")
                    sheet.cell(column=3, row=1, value="Process Name")
                    sheet.cell(column=4, row=1, value="% - CPU Usage")
                    sheet.cell(column=5, row=1, value="% - GPU Usage")
                    sheet.cell(column=6, row=1, value="% - Memory usage")
                    sheet.cell(column=7, row=1, value="% - Estimated Power Consumption")  # Added column

                row_data = [current_time, pid, process_name, cpu, gpu_usage, memory_formatted, cpu_usage]
                sheet.append(row_data)

                file.save(path)

                
        except KeyboardInterrupt:
            print("\nMonitoring stopped.")
        print("Press Ctrl + C to exit")
    

if __name__ == "__main__":
    main()
