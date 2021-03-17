# %%
# opencv 获取验证码的单个字符
import matplotlib.pyplot as plt
import os
import cv2

cv2.__version__

# %%
# PART1
img_path = 'data/verifycode_chars/1GDH.jpg'
os.path.exists(img_path)

# %%
# 灰度模式读取图片
gray = cv2.imread(img_path, 0)
type(gray), gray.shape

# %%
plt.imshow(gray)

# %%
# 验证码的边缘设置为白色（255）
height, width = gray.shape
for i in range(width):
    gray[0, i] = 255
    gray[height-1, i] = 255
for j in range(height):
    gray[j, 0] = 255
    gray[j, width-1] = 255

plt.imshow(gray)

# %%
# 中值滤波处理 模板大小 3*3
blur = cv2.medianBlur(gray, 3)
plt.imshow(gray)

# %%
# 二值化处理，将图像由灰度模式转化至黑白模式
ret, thresh1 = cv2.threshold(blur, 200, 255, cv2.THRESH_BINARY)
print(thresh1.shape)
thresh1[20, :]

# %%
plt.imshow(thresh1)

# %%
# 提取单个字符
contours, hierarchy = cv2.findContours(thresh1, 2, 2)

for idx, cnt in enumerate(contours):
    x, y, w, h = cv2.boundingRect(cnt)
    if x != 0 and y != 0 and w*h >= 100:
        tmp_split = thresh1[y:y+h, x:x+w]
        cv2.imwrite('/tmp/test/char%d.jpg' % idx, tmp_split)

print('split char saved.')


# %%
# PART2
dir_path = '/tmp/test'
imgs = os.listdir(dir_path)
imgs = [os.path.join(dir_path, img) for img in imgs]
imgs

# %%
# 处理噪声图片
new_imgs = []
for img_path in imgs:
    image = cv2.imread(img_path, 0)
    height, width = image.shape

    corner_list = [image[0, 0] < 127, image[height-1, 0] < 127,
                   image[0, width-1] < 127, image[height-1, width-1] < 127]
    if sum(corner_list) >= 3:
        os.remove(img_path)
    else:
        new_imgs.append(img_path)

new_imgs

# %%
# 处理黏连图片
import uuid

for img_path in new_imgs:
    image = cv2.imread(img_path, 0)
    height, width = image.shape

    parts = 1
    if width >= 64:
        parts = 4
    elif width >= 48:
        parts = 3
    elif width >= 24:
        parts = 2

    if parts == 1:
        continue

    start = 0  # 超始位置
    step = width // parts  # 步长
    for _ in range(parts):
        cv2.imwrite('/tmp/test/char_%d.jpg' %
                    uuid.uuid1(), image[:, start:start+step])
        start += step
    os.remove(img_path)

print('pre-handle char done.')

# %%
new_imgs = os.listdir(dir_path)
new_imgs

# %%
print('opencv verifycode demo done.')
