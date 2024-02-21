import cv2
import numpy as np


# https://github.com/mtntruong/entropy-otsu/blob/master/implementation/neighbor_valley_emphasis.m
class ValleyEmphasisBinarizer:
    def __init__(self, N: int = 5) -> None:
        self.N = N

    def binarize(self, image: np.ndarray) -> np.ndarray:
        gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        threshold = self.get_threshold(gray_img)

        gray_img[gray_img <= threshold] = 0
        gray_img[gray_img > threshold] = 1
        return gray_img

    def get_threshold(self, gray_img: np.ndarray) -> int:
        c, x = np.histogram(gray_img, bins=255)
        h, w = gray_img.shape
        total = h * w

        sum_val = 0
        for t in range(255):
            sum_val = sum_val + (t * c[t] / total)

        var_max = 0
        threshold = 0

        omega_1 = 0
        mu_k = 0

        for t in range(254):
            omega_1 = omega_1 + c[t] / total
            omega_2 = 1 - omega_1
            mu_k = mu_k + t * (c[t] / total)
            mu_1 = mu_k / omega_1
            mu_2 = (sum_val - mu_k) / omega_2
            sum_of_neighbors = np.sum(c[max(1, t - self.N):min(255, t + self.N)])
            denom = total
            current_var = (1 - sum_of_neighbors / denom) * (omega_1 * mu_1 ** 2 + omega_2 * mu_2 ** 2)
            # Check if new maximum found
            if current_var > var_max:
                var_max = current_var
                threshold = t

        return threshold
