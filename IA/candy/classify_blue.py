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

    detected = []
    for i, blob in enumerate(blobs, start=1):
        rows, cols = blob.coords.T
        b_mean = color[rows, cols, 2].mean()
        if b_mean > 65:
            detected.append((i, b_mean))

    print(f"blobs detected as blue (mean B > 65): {len(detected)}")
    for i, b in detected:
        print(f"  blob {i}: mean B = {b:.1f}")


if __name__ == "__main__":
    main()
