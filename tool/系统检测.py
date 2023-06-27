import datetime

import psutil


def format_size(size):

    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024:
            return f"{size:.2f} {unit}"
        else:
            size /= 1024.0
    return f"{size:.2f} GB"


def mem_method():
    print("--------------内存的使用情况--------------")
    # 获取系统内存信息
    mem = psutil.virtual_memory()

    # 输出内存信息
    print(f"总内存：{mem.total / 1024 / 1024:.2f} MB")
    print(f"可用内存：{mem.available / 1024 / 1024:.2f} MB")
    print(f"已用内存：{mem.used / 1024 / 1024:.2f} MB")
    print(f"内存使用率：{mem.percent:.2f}%")

    # 获取虚拟内存信息
    swap = psutil.swap_memory()

    # 输出虚拟内存信息
    print(f"总虚拟内存：{swap.total / 1024 / 1024:.2f} MB")
    print(f"可用虚拟内存：{swap.free / 1024 / 1024:.2f} MB")
    print(f"已用虚拟内存：{swap.used / 1024 / 1024:.2f} MB")
    print(f"虚拟内存使用率：{swap.percent:.2f}%")


def cpu_method():
    print("--------------CPU的使用情况--------------")
    # 获取CPU核心数
    cpu_count = psutil.cpu_count(logical=False)
    print(f"CPU核心数：{cpu_count}")
    # 获取CPU使用率
    cpu_usage = psutil.cpu_percent(interval=1)
    print(f"CPU使用率：{cpu_usage}%")
    # 获取CPU频率
    cpu_freq = psutil.cpu_freq()
    print(f"CPU最大频率：{cpu_freq.max:.2f} MHz")
    print(f"CPU最小频率：{cpu_freq.min:.2f} MHz")
    print(f"CPU当前频率：{cpu_freq.current:.2f} MHz")

    load_avg = psutil.getloadavg()
    print(f"1分钟内系统负载：{load_avg[0]:.2f}")
    print(f"5分钟内系统负载：{load_avg[1]:.2f}")
    print(f"15分钟内系统负载：{load_avg[2]:.2f}")


def dick_method():
    print("--------------磁盘的使用情况--------------")
    # 获取磁盘分区信息
    partitions = psutil.disk_partitions()

    # 遍历磁盘分区信息，获取每个分区的容量信息
    for partition in partitions:
        print(f"设备名：{partition.device}")
        print(f"挂载点：{partition.mountpoint}")
        print(f"文件系统类型：{partition.fstype}")
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            # 如果获取磁盘使用情况时出现权限错误，跳过该分区
            continue
        print(f"总容量：{partition_usage.total / (1024 * 1024 * 1024):.2f} GB")
        print(f"已使用容量：{partition_usage.used / (1024 * 1024 * 1024):.2f} GB")
        print(f"可用容量：{partition_usage.free / (1024 * 1024 * 1024):.2f} GB")
        print(f"使用率：{partition_usage.percent}%")
        print()


def network_method():
    # 获取网络连接信息
    net_connections = psutil.net_connections()
    net_io_counters = psutil.net_io_counters()
    # 获取总的发送字节数
    print("总的发送字节数：", format_size(net_io_counters.bytes_sent))
    # 获取总的接收字节数
    print("总的接收字节数：", format_size(net_io_counters.bytes_recv))

    # 输出网络连接信息
    print("当前网络连接数量：", len(net_connections))
    # for conn in net_connections:
    #     print("本地地址：", conn.laddr)
    #     print("远程地址：", conn.raddr)
    #     print("状态：", conn.status)
    #     print("进程ID：", conn.pid)


def other_method():
    # 获取当前用户登录的信息
    print(psutil.users())

    # 获取设备开机时间
    data1 = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime('%Y-%m-%d %H:%M:%S')
    print("该设备启动时间为", data1)

    # 获取设备开始时长
    datenow = datetime.datetime.now() - datetime.datetime.fromtimestamp(psutil.boot_time())
    print("设备开机时长为",str(datenow))

# 获取进程信息
def pid_mem_method():
    # 定义要监控的进程数目
    num_processes = 3

    # 获取所有进程信息列表
    all_processes = []
    for process in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            # 获取进程信息
            process_info = process.as_dict(attrs=['pid', 'name', 'cpu_percent', 'memory_percent'])
            # 加入到列表中
            all_processes.append(process_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    # 根据 内存占用进行排序
    sorted_processes = sorted(all_processes, key=lambda x: x['memory_percent'], reverse=True)

    # 输出前 num_processes 个进程信息
    for i, process in enumerate(sorted_processes[:num_processes]):
        print(f'进程{i + 1}：')
        print(f'进程ID：{process["pid"]}')
        print(f'进程名称：{process["name"]}')
        print(f'进程CPU占用率：{process["cpu_percent"]}%')
        print(f'进程内存占用率：{process["memory_percent"]}%')
        print('\n')

def pid_cpu_method():
    # 定义要监控的进程数目
    num_processes = 3

    # 获取所有进程信息列表
    all_processes = []
    for process in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            # 获取进程信息
            process_info = process.as_dict(attrs=['pid', 'name', 'cpu_percent', 'memory_percent'])
            # 加入到列表中
            all_processes.append(process_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    # 根据 CPU占用率排序
    sorted_processes = sorted(all_processes, key=lambda x: x['cpu_percent'], reverse=True)

    # 输出前 num_processes 个进程信息
    for i, process in enumerate(sorted_processes[:num_processes]):
        print(f'进程{i + 1}：')
        print(f'进程ID：{process["pid"]}')
        print(f'进程名称：{process["name"]}')
        print(f'进程CPU占用率：{process["cpu_percent"]}%')
        print(f'进程内存占用率：{process["memory_percent"]}%')
        print('\n')


mem_method()
cpu_method()
dick_method()
network_method()
other_method()
pid_cpu_method()
pid_mem_method()