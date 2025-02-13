import psutil
from time import sleep

cpuuse = psutil.cpu_percent(interval=1)
ramuse = psutil.virtual_memory().percent
diskuse = psutil.disk_usage('/').percent
bytesent = psutil.net_io_counters().bytes_sent
bytesreceived = psutil.net_io_counters().bytes_recv

mbsent = bytesent /(1024 * 1024)
mbrec = bytesreceived / (1024 * 1024)

i=1
while True:
    print("iteracao " + str(i))
    print("uso da cpu: " + str(cpuuse))
    print("uso da ram: " + str(ramuse))
    print("uso do disco: " + str(diskuse))
    print(f'megabytes enviados: {mbsent:.2f} MB')
    print(f'megabytes recebidos: {mbrec:.2f} MB')
    print()
    i+=1
    if cpuuse>0.75 and cpuuse < 0.85:
        print("ALERTA [MÉDIO] - CPU está com uso alto")
        print()
    elif cpuuse >= 0.85:
        print("ALERTA [CRÍTICO] - Memória próxima do limite de uso!")
        print()
    sleep(5)



