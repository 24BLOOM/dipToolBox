# 数字图像处理大作业

### 																														--图像处理程序

​												  

使用 opencv 与 pyqt5 实现的图像处理小程序，通过左边目录栏进入相应文件夹，双击选择图片；右键单击图片可以另保存图像 ，右键单击已选操作可以删除该操作
![demo.png](demo/demo.png)

注：由于打包时将依赖的库一并打包文件较大，若想要节省空间可将main.exe 和build文件夹删除，在确认电脑包含以下依赖时运行main.py即可。

## 依赖

- opencv* python
- matplotlib
- pyqt5 = 5.10(建议)

## 涉及知识点

1. 图像平滑
2. 腐蚀膨胀
3. 开操作、闭操作
4. 直方图均衡化
5. 图像锐化
6. 阈值分割
7. 梯度算子
8. 边缘检测
9. 频域滤波
10. 空域增强
11. 频域增强



## 已实现功能展示

### 图像旋转

* 左旋![left.png](demo/left.png) 
* 右旋![right.png](demo/right.png)



### 转灰度图

* 右旋![gray.png](demo/gray.png)



### 图像平滑

* 均值滤波![Mean_filtering.png](demo/Mean_filtering.png) 
*  高斯滤波![Gaussian_filter.png](demo/Gaussian_filter.png) 
* 中值滤波![Median_filter.png](demo/Median_filter.png)



### 直方图均衡化

* 均衡化![Equalization.png](demo/Equalization.png)



### 形态学操作

* 腐蚀![i_corrosion.png](demo/i_corrosion.png) 
*  膨胀![i_expand.png](demo/i_expand.png) 
*  闭操作![i_closed_op.png](demo/i_closed_op.png) 
* 开操作![i_open_op.png](demo/i_open_op.png) 
* 形态学边界提取![grad_op.png](demo/grad_op.png)



### 梯度计算

* sobel 算子![grad_sobel.png](demo/grad_sobel.png)
*  laplacian 算子![grad_laplacian.png](demo/grad_laplacian.png)



### 阈值处理

* 二进制阈值化![value2.png](demo/value2.png) 
* 反二进制阈值化![value2.png](demo/value2back.png) 
*  截断阈值化![value3.png](demo/value3.png) 
* 阈值化为 0![value0.png](demo/value0.png)
* 反阈值化为 0![value0back.png](demo/value0back.png)

### 边缘检测

* 边缘检测![side.png](demo/side.png)

### 频域滤波

* 高通![lvbo1.png](demo/lvbo1.png)

* 带通![lvbo1.png](demo/lvbo2.png)

* 低通![lvbo1.png](demo/lvbo3.png)

  



### 亮度调节

* 亮度调节 4![light4.png](demo/light4.png) 
*  亮度调节 30![light30.png](demo/light30.png)