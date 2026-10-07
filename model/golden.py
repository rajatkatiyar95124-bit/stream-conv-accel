import numpy as np

def conv3x3_golden(img, kernel, bias, shift=0):
    """
    img    : 2D uint8 array (H x W)
    kernel : 3x3 int8 array
    bias   : int
    shift  : arithmetic right shift applied before ReLU/saturation
    Returns (H-2) x (W-2) uint8 array (valid-only, no padding).
    """
    H, W = img.shape
    out = np.zeros((H - 2, W - 2), dtype=np.uint8)
    k = kernel.astype(np.int32)
    for r in range(H - 2):
        for c in range(W - 2):
            win = img[r:r+3, c:c+3].astype(np.int32)
            acc = int(np.sum(win * k)) + bias   # fits in 20-bit signed
            acc >>= shift
            acc = max(acc, 0)                   # ReLU
            out[r, c] = min(acc, 255)           # saturate to 8 bits
    return out

if __name__ == "__main__":
    rng = np.random.default_rng(0)
    img = rng.integers(0, 256, (8, 8), dtype=np.uint8)
    sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.int8)
    print(img)
    print(conv3x3_golden(img, sobel_x, bias=0))