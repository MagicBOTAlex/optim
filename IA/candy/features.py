import math

import numpy as np
import skimage.color
import skimage.io
import skimage.measure
import skimage.morphology


def main():
    color = skimage.io.imread("candy.jpg")
    gray = skimage.color.rgb2gray(color)

    thresholded = gray < 0.6
    closed = skimage.morphology.closing(thresholded, skimage.morphology.disk(3))
    eroded = skimage.morphology.erosion(closed, skimage.morphology.disk(6))

    labels = skimage.measure.label(eroded, connectivity=2)
    blobs = skimage.measure.regionprops(labels)

    b_means = []
    print(f"number of blobs: {len(blobs)}")
    print(
        "blob,mean_r,mean_g,mean_b,std_r,std_g,std_b,area,perimeter,circularity"
    )

    for i, blob in enumerate(blobs, start=1):
        rows, cols = blob.coords.T
        r = color[rows, cols, 0]
        g = color[rows, cols, 1]
        b = color[rows, cols, 2]
        b_means.append(b.mean())

        perimeter = blob.perimeter
        circularity = 2 * math.sqrt(math.pi * blob.area) / perimeter

        print(
            f"{i},{r.mean():.1f},{g.mean():.1f},{b.mean():.1f},"
            f"{r.std():.1f},{g.std():.1f},{b.std():.1f},"
            f"{blob.area},{perimeter:.1f},{circularity:.4f}"
        )

    b_threshold = np.quantile(b_means, 0.75)
    print(f"B mean threshold (0.75 quantile): {b_threshold:.1f}")


if __name__ == "__main__":
    main()
