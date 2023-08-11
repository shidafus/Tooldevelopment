from datetime import datetime, timedelta
import re, sys


class LogAnalyzer:
    def __init__(self, filename=sys.argv[1] if len(sys.argv) > 1 else 'c.log',
                 pattern=sys.argv[2] if len(sys.argv) > 2 else r'\d{4}\d{2}\d{2}\d{2}\d{2}\d{2}'):
        self.filename = filename
        self.pattern = pattern
        self.data = {}
        self.data1 = {}

    def open_file(self):
        with open(self.filename, mode='r', encoding='utf-8') as file:
            files = file.readlines()
        return files

    def get_date(self, file):
        for line in file:
            time = re.search(self.pattern, line)
            timedata = time.group()
            parts = line.split()
            size = int(parts[8])
            self.data[timedata] = size
        return self.data

    def sort_data(self, data):
        data_keys = sorted(data)
        for i in data_keys:
            self.data1[i] = data[i]
        del data
        return self.data1

    def analyze(self):
        # 打开文件
        file = self.open_file()

        # 获取文件内容
        self.data = self.get_date(file)

        # 按照日志时间排序
        self.data1 = self.sort_data(self.data)

        # 输出每5分钟，走出的流量
        current_timestamp = None
        time_interval = timedelta(minutes=5)
        data_size = 0

        for k, v in self.data1.items():
            # 把datetime类型的字符串格式 转化为 datetime格式
            timestamp = datetime.strptime(k, '%Y%m%d%H%M%S')
            # 定义工具变量
            if current_timestamp is None:
                current_timestamp = timestamp

            # 计算时间间隔
            time_difference = timestamp - current_timestamp

            # 如果时间间隔超过5分钟，输出当前时间段的数据大小并重置数据大小和时间戳
            if time_difference >= time_interval:
                print(f"{current_timestamp} - {data_size / 1024 ** 2} MB")
                current_timestamp = timestamp
                data_size = 0
            else:
                data_size += v


if __name__ == "__main__":
    # 创建LogAnalyzer对象
    log_analyzer = LogAnalyzer()

    # 调用analyze方法进行日志分析
    log_analyzer.analyze()
