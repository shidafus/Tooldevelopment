import pyaudio
import wave

# 定义录音参数
chunk = 1024  # 每次读取的音频帧大小
channels = 1  # 声道数
sample_rate = 44100  # 采样率
record_seconds = 5  # 录音时长
output_filename = 'output.wav'  # 输出文件名

# 初始化PyAudio
audio = pyaudio.PyAudio()

# 打开音频流
stream = audio.open(format=pyaudio.paInt16,
                    channels=channels,
                    rate=sample_rate,
                    input=True,
                    frames_per_buffer=chunk)

print("开始录音...")

# 录音数据缓存
frames = []

# 录音
for i in range(0, int(sample_rate / chunk * record_seconds)):
    data = stream.read(chunk)
    frames.append(data)

print("录音结束.")

# 停止音频流
stream.stop_stream()
stream.close()
audio.terminate()

# 保存录音数据为WAV文件
wave_file = wave.open(output_filename, 'wb')
wave_file.setnchannels(channels)
wave_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
wave_file.setframerate(sample_rate)
wave_file.writeframes(b''.join(frames))
wave_file.close()

print(f"录音已保存为'{output_filename}'")