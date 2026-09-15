import skimage.color
import skimage.filters
import skimage.io


def main():
    image = skimage.io.imread("candy.jpg")

    if image.ndim == 3:
        image = skimage.color.rgb2gray(image)

    threshold = skimage.filters.threshold_otsu(image)
    thresholded = image > threshold

    foreground = thresholded.sum()
    background = thresholded.size - foreground

    print(f"shape: {image.shape}")
    print(f"dtype: {image.dtype}")
    print(f"value range: [{image.min():.4f}, {image.max():.4f}]")
    print(f"Otsu threshold: {threshold:.4f}")
    print(f"foreground (1) pixels: {foreground}")
    print(f"background (0) pixels: {background}")


if __name__ == "__main__":
    main()
