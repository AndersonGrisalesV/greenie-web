#!/usr/bin/env python3

import psutil
import datetime
import time
import schedule
import openpyxl
import platform


def main():
    pid = int(input("Enter process ID: "))
    
    # Schedule the warning and monitoring tasks
    # schedule.every(1).second.do(warning)
    schedule.every(5).seconds.do(monitor, pid)
  
    # detected_gpus = detect_gpus()

    # if detected_gpus:
    #     print("Detected GPUs:")
    #     for gpu in detected_gpus:
    #         print(f"Type: {gpu['type']}, Index: {gpu['index']}, Name: {gpu['name']}")
    # else:
    #     print("No GPUs detected.")

    
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except Exception as e:
        print("An error occurred:", e)



def monitor(pid):
    current_time = datetime.datetime.now().strftime("%Y%m%d - %H:%M:%S")
    
    p = psutil.Process(pid)
    cpu = p.cpu_percent(interval=1) / psutil.cpu_count()
    memory_mb = p.memory_info().rss / (1024 * 1024)
    memory = p.memory_percent()  
    memory_formatted = f"{memory:.2f}"
    gpu_usage = 0
 

    
    print("1. Cpu usage is: ", cpu, "%")
    print("2. Memory utilization is: ", memory_formatted, "%")
    # print("3. Gpu usage is: ",  gpus, "%")

    path = "Monitor_Result.xlsx"
    
    try:
        file = openpyxl.load_workbook(path)
    except FileNotFoundError:
        file = openpyxl.Workbook()
    
    sheet = file.active
    if sheet.cell(1, 1).value is None:
        sheet.cell(column=1, row=1, value="Date & Time")
        sheet.cell(column=2, row=1, value="Process ID")
        sheet.cell(column=3, row=1, value="Process CPU Usage %")
        sheet.cell(column=4, row=1, value="Process Memory Usage")
        sheet.cell(column=5, row=1, value="Memory usage %")
        sheet.cell(column=6, row=1, value="GPU Usage %")
    
    row_data = [current_time, pid, cpu, memory_mb, memory_formatted, gpu_usage]
    sheet.append(row_data)
    
    file.save(path)

# def detect_gpus():
#     gpus = []

#     # Detect NVIDIA GPUs using nvidia-ml-py
#     try:
#         nvidia_smi.nvmlInit()
#         device_count = nvidia_smi.nvmlDeviceGetCount()
#         for i in range(device_count):
#             gpu_info = {
#                 "type": "NVIDIA",
#                 "index": i,
#                 "name": nvidia_smi.nvmlDeviceGetName(nvidia_smi.nvmlDeviceGetHandleByIndex(i)).decode("utf-8")
#             }
#             gpus.append(gpu_info)
#     except nvidia_smi.NVMLError:
#         pass
#     finally:
#         nvidia_smi.nvmlShutdown()



if __name__ == "__main__":
    main()
