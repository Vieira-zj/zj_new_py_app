# %%
# 图像旋转
import cv2
import numpy as np
import matplotlib.pyplot as plt

np.__version__, cv2.__version__

# %%
# PART1: image pre-handler
img_path = 'data/img_rotate.png'
img = cv2.imread(img_path, 1)
img.shape  # 3通道

# %%
plt.imshow(img)

# %%
# 将图片的边缘设置为白色
height, width = img.shape[0:2]
for i in range(width):
    img[0, i] = [255] * 3
    img[height - 1, i] = [255] * 3
for j in range(height):
    img[j, 0] = [255] * 3
    img[j, width - 1] = [255] * 3

plt.imshow(img)

# %%
# 去掉灰色线（即噪声）
for i in range(height):
    for j in range(width):
        if list(img[i, j]) == [204, 213, 204]:
            img[i, j] = [255] * 3

plt.imshow(img)

# %%
# 把图片转换为灰度模式
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# 中值滤波
blur = cv2.medianBlur(gray, 3)
# 二值化
ret, thresh = cv2.threshold(blur, 200, 255, cv2.THRESH_BINARY)
print(thresh.shape)  # 1通道
thresh[25, :]

# %%
plt.imshow(thresh)

# %%
img_path = '/tmp/test/char_after_bin.png'
cv2.imwrite(img_path, thresh)
print('image pre-handler done.')


# %%
# PART2: image rotate
img_path = '/tmp/test/char_after_bin.png'
img = cv2.imread(img_path, 0)
print(img.shape)
img[25, :]

# %%
plt.imshow(img)

# %%
angle = 0.0
contours, _ = cv2.findContours(img, 2, 2)

for cnt in contours:
    # 最小外界矩形的宽度和高度
    width, height = cv2.minAreaRect(cnt)[1]
    if width*height > 100:
        rect = cv2.minAreaRect(cnt)
        # 获取最小外接矩形的4个顶点
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        if 0 not in box.ravel():
            # 获取旋转角度
            theta = cv2.minAreaRect(cnt)[2]
            if abs(theta) <= 45:
                print('image rotate: %.2f.' % abs(theta))
                angle = theta

# %%
# 对图片旋转angle角度
h, w = img.shape
center = (w // 2, h // 2)
M = cv2.getRotationMatrix2D(center, angle, 1.0)
rotated = cv2.warpAffine(
    img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

plt.imshow(rotated)

# %%
cv2.imwrite('/tmp/test/char_after_rotate.png', rotated)
print('opencv image rotate done.')

# %%
