import qrcode

# 生成二维码
img = qrcode.make('https://zzk.cnblogs.com/')

# 保存二维码图片
img.save('qrcode.png')