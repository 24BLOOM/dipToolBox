import numpy as np
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import QListWidgetItem, QPushButton
from flags import *


class MyItem(QListWidgetItem):
    def __init__(self, name=None, parent=None):
        super(MyItem, self).__init__(name, parent=parent)
        self.setIcon(QIcon('icons/color.png'))
        self.setSizeHint(QSize(60, 60))  # size

    def get_params(self):
        protected = [v for v in dir(self) if v.startswith(
            '_') and not v.startswith('__')]
        param = {}
        for v in protected:
            param[v.replace('_', '', 1)] = self.__getattribute__(v)
        return param

    def update_params(self, param):
        for k, v in param.items():
            if '_' + k in dir(self):
                self.__setattr__('_' + k, v)


class GrayingItem(MyItem):
    def __init__(self, parent=None):
        super(GrayingItem, self).__init__(' 灰度化 ', parent=parent)
        self._mode = BGR2GRAY_COLOR

    def __call__(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        return img


class FilterItem(MyItem):

    def __init__(self, parent=None):
        super().__init__('平滑处理', parent=parent)
        self._ksize = 3
        self._kind = MEAN_FILTER
        self._sigmax = 0

    def __call__(self, img):
        if self._kind == MEAN_FILTER:
            img = cv2.blur(img, (self._ksize, self._ksize))
        elif self._kind == GAUSSIAN_FILTER:
            img = cv2.GaussianBlur(
                img, (self._ksize, self._ksize), self._sigmax)
        elif self._kind == MEDIAN_FILTER:
            img = cv2.medianBlur(img, self._ksize)
        return img


class MorphItem(MyItem):
    def __init__(self, parent=None):
        super().__init__(' 形态学 ', parent=parent)
        self._ksize = 3
        self._op = ERODE_MORPH_OP
        self._kshape = RECT_MORPH_SHAPE

    def __call__(self, img):
        op = MORPH_OP[self._op]
        kshape = MORPH_SHAPE[self._kshape]
        kernal = cv2.getStructuringElement(kshape, (self._ksize, self._ksize))
        img = cv2.morphologyEx(img, self._op, kernal)
        return img


class GradItem(MyItem):

    def __init__(self, parent=None):
        super().__init__('图像梯度', parent=parent)
        self._kind = SOBEL_GRAD
        self._ksize = 3
        self._dx = 1
        self._dy = 0

    def __call__(self, img):
        if self._dx == 0 and self._dy == 0 and self._kind != LAPLACIAN_GRAD:
            self.setBackground(QColor(255, 0, 0))
            self.setText('图像梯度 （无效: dx与dy不同时为0）')
        else:
            self.setBackground(QColor(200, 200, 200))
            self.setText('图像梯度')
            if self._kind == SOBEL_GRAD:
                img = cv2.Sobel(img, -1, self._dx, self._dy, self._ksize)
            elif self._kind == SCHARR_GRAD:
                img = cv2.Scharr(img, -1, self._dx, self._dy)
            elif self._kind == LAPLACIAN_GRAD:
                img = cv2.Laplacian(img, -1)
        return img


class ThresholdItem(MyItem):
    def __init__(self, parent=None):
        super().__init__('阈值处理', parent=parent)
        self._thresh = 127
        self._maxval = 255
        self._method = BINARY_THRESH_METHOD

    def __call__(self, img):
        method = THRESH_METHOD[self._method]
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        img = cv2.threshold(img, self._thresh, self._thresh, method)[1]
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        return img


class EdgeItem(MyItem):
    def __init__(self, parent=None):
        super(EdgeItem, self).__init__('边缘检测', parent=parent)
        self._thresh1 = 20
        self._thresh2 = 100

    def __call__(self, img):
        img = cv2.Canny(img, threshold1=self._thresh1,
                        threshold2=self._thresh2)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        return img


class ContourItem(MyItem):
    def __init__(self, parent=None):
        super(ContourItem, self).__init__('频域滤波', parent=parent)
        self._mode = 0
        self._thresh1 = 5
        self._thresh2 = 5

    def __call__(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        R = img.shape
        rows, cols = R[0], R[1]
        crow, ccol = int(rows / 2), int(cols / 2)
        thresh1 = self._thresh1
        thresh2 = self._thresh2
        if self._mode == 0:
            f_B = np.fft.fft2(img)
            fshift_B = np.fft.fftshift(f_B)
            fshift_B[crow-thresh1:crow+thresh1, ccol-thresh1:ccol+thresh1] = 0
            f_ishift_B = np.fft.ifftshift(fshift_B)
            img_back_B = np.fft.ifft2(f_ishift_B)
            img_back_B = np.abs(img_back_B)
            img_back_B = img_back_B.astype(np.float32)
            img_back_B = cv2.cvtColor(img_back_B, cv2.COLOR_GRAY2BGR)
            img_back_B = img_back_B.astype("uint8")
            return img_back_B
        if self._mode == 1:
            f_G = np.fft.fft2(img)
            fshift_G = np.fft.fftshift(f_G)
            mask1 = np.ones((rows, cols), np.uint8)
            mask1[crow-thresh2:crow+thresh2, ccol-thresh2:ccol+thresh2] = 0
            mask2 = np.zeros((rows, cols), np.uint8)
            mask2[crow-thresh1:crow+thresh1, rows-thresh1:rows+thresh1] = 1
            mask_ = mask1*mask2
            fshift_G = fshift_G*mask_
            f_ishift_G = np.fft.ifftshift(fshift_G)
            img_back_G = np.fft.ifft2(f_ishift_G)
            img_back_G = np.abs(img_back_G)
            img_back_G = img_back_G.astype(np.float32)
            img_back_G = cv2.cvtColor(img_back_G, cv2.COLOR_GRAY2BGR)
            img_back_G = img_back_G.astype(np.uint8)
            return img_back_G
        if self._mode == 2:
            f_R = np.fft.fft2(img)
            fshift_R = np.fft.fftshift(f_R)
            mask = np.zeros((rows, cols,), np.uint8)
            mask[crow-thresh1:crow+thresh1, ccol-thresh1:ccol+thresh1] = 1
            fshift_R = fshift_R*mask
            f_ishift_R = np.fft.ifftshift(fshift_R)
            img_back_R = np.fft.ifft2(f_ishift_R)
            img_back_R = np.abs(img_back_R)
            img_back_R = img_back_R.astype(np.float32)
            img_back_R = cv2.cvtColor(img_back_R, cv2.COLOR_GRAY2BGR)
            img_back_R = img_back_R.astype(np.uint8)
            return img_back_R
        img = img.astype(np.float32)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        return img


class EqualizeItem(MyItem):
    def __init__(self, parent=None):
        super().__init__(' 均衡化 ', parent=parent)
        self._blue = True
        self._green = True
        self._red = True

    def __call__(self, img):
        r = cv2.split(img)
        if len(r) <= 1:
            r[0] = cv2.equalizeHist(r[0])
            return cv2.merge((r[0], r[0], r[0]))
        else:
            if self._blue:
                r[0] = cv2.equalizeHist(r[0])
            if self._green:
                r[1] = cv2.equalizeHist(r[1])
            if self._red:
                r[2] = cv2.equalizeHist(r[2])
            return cv2.merge((r[0], r[1], r[2]))


class LightItem(MyItem):
    def __init__(self, parent=None):
        super(LightItem, self).__init__('亮度调节', parent=parent)
        self._alpha = 1
        self._beta = 0

    def __call__(self, img):
        blank = np.zeros(img.shape, img.dtype)
        img = cv2.addWeighted(img, float(self._alpha)/10, blank,
                              1 - (float(self._alpha)/10), self._beta)
        print(self._alpha)
        return img
