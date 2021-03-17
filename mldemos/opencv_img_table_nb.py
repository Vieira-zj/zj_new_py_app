# %%
# 识别图片中的表格数据
import cv2
import numpy as np
import uuid
import matplotlib.pyplot as plt

cv2.__version__, np.__version__

# %%
image = cv2.imread('data/img_table.png', 1)
image.shape

# %%
# STEP1. 识别表格中的横线
# 把图片转换为灰度模式
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray.shape

# %%
# 图像二值化
ret, thresh1 = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
# 进行两次中值滤波
blur = cv2.medianBlur(thresh1, 3)
blur = cv2.medianBlur(blur, 3)

plt.imshow(blur)

# %%
# 横向直线列表
horizontal_lines = []
h, w = blur.shape

for i in range(h - 1):
    # 找到两条记录的分隔线段，以相邻两行的平均像素差大于120为标准
    if abs(np.mean(blur[i, :] - np.mean(blur[i+1, :]))) > 120:
        horizontal_lines.append([0, i, w, i])
        cv2.line(image, (0, i), (w, i), (0, 255, 0), 2)

horizontal_lines = horizontal_lines[1:]
horizontal_lines

# %%
plt.imshow(image)

# %%
# STEP2. 识别表格中的竖线
# Canny边缘检测
edges = cv2.Canny(gray, 30, 240)

# Hough直线检测
maxLineGap = 30
minLineLength = 500
lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100,
                        minLineLength, maxLineGap).tolist()
# 手动添加两条竖直直线
lines.append([[13, 937, 13, 102]])
lines.append([[756, 937, 756, 102]])
sorted_lines = sorted(lines, key=lambda x: x[0])
len(sorted_lines)

# %%
# 纵向直线列表
vertical_lines = []
for line in sorted_lines:
    for x1, y1, x2, y2 in line:
        if x1 == x2:
            vertical_lines.append((x1, y1, x2, y2))
            cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)

vertical_lines

# %%
plt.imshow(image)

# %%
# STEP3. 识别图片中的单元格
# 顶点列表
vertex = []
for v_line in vertical_lines:
    for h_line in horizontal_lines:
        vertex.append((v_line[0], h_line[1]))

len(vertex)

# %%
# 绘制顶点
for point in vertex:
    cv2.circle(image, point, 1, (255, 0, 0), 2)

plt.imshow(image)

# %%
# 截取单元格
rects = []
for i in range(0, len(vertical_lines) - 1, 2):
    for j in range(len(horizontal_lines) - 1):
        rects.append((vertical_lines[i][0], horizontal_lines[j][1],
                      vertical_lines[i + 1][0], horizontal_lines[j + 1][1]))

len(rects)

# %%
for rect in rects[15:25]:
    cell = gray[rect[1]:rect[3], rect[0]:rect[2]]
    cv2.imwrite('/tmp/test/cell_%d.png' % uuid.uuid1(), cell)

print('table cells saved.')

# %%
