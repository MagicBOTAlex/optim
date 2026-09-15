import skimage.color
import skimage.filters
import skimage.io
import skimage.measure
import skimage.morphology


def main():
    image = skimage.io.imread("candy.jpg")

    if image.ndim == 3:
        image = skimage.color.rgb2gray(image)

    thresholded = image < 0.6

    closed = skimage.morphology.closing(thresholded, skimage.morphology.disk(3))
    eroded = skimage.morphology.erosion(closed, skimage.morphology.disk(6))

    labels = skimage.measure.label(eroded, connectivity=2)
    blobs = skimage.measure.regionprops(labels)

    print(f"shape: {image.shape}")
    print(f"dtype: {image.dtype}")
    print(f"value range: [{image.min():.4f}, {image.max():.4f}]")
    print(f"threshold: 0.6")
    print(f"number of blobs: {len(blobs)}")

    for i, blob in enumerate(blobs, start=1):
        minr, minc, maxr, maxc = blob.bbox
        print(
            f"blob {i}: area={blob.area}, centroid={
                tuple(round(v, 1) for v in blob.centroid)
            }, bbox=({minr}, {minc}, {maxr}, {maxc})"
        )


if __name__ == "__main__":
    main()
