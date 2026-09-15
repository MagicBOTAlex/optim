import skimage.color
import skimage.io


def main():
    image = skimage.io.imread("candy.jpg")

    if image.ndim == 3:
        image = skimage.color.rgb2gray(image)

    thresholded = image < 0.6

    print(f"shape: {image.shape}")
    print(f"dtype: {image.dtype}")
    print(f"value range: [{image.min():.4f}, {image.max():.4f}]")
    foreground = thresholded.sum()
    background = thresholded.size - foreground
    print(f"foreground (1) pixels: {foreground}")
    print(f"background (0) pixels: {background}")


if __name__ == "__main__":
    main()
