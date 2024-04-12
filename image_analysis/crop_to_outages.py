from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist

def find_optimal_clusters(data, max_k=10):
    distortions = []
    for k in range(1, max_k + 1):
        kmeans = KMeans(n_clusters=k)
        kmeans.fit(data)
        distortions.append(sum(np.min(cdist(data, kmeans.cluster_centers_, 'euclidean'), axis=1)) / data.shape[0])
    
    # You can further refine this method to choose the best K, e.g., using the Elbow method
    # For simplicity, we'll choose K where the reduction in distortion diminishes
    k_optimal = 1 + next(i for i, diff in enumerate(np.diff(distortions)) if diff > -0.1)
    return min(k_optimal, max_k)

def find_red_areas(image_path, crop_size=(100, 100)):
    # Load the image
    image = Image.open(image_path)

    # Ensure the image is in RGBA format
    if image.mode != 'RGBA':
        image = image.convert('RGBA')

    # Convert to NumPy array
    data = np.array(image)

    # Define the pure red color
    pure_red = np.array([255, 0, 0, 255])

    # Find pixels that match pure red
    red_pixel_indices = np.argwhere(np.all(data == pure_red, axis=-1))

    if len(red_pixel_indices) == 0:
        return []  # No red pixels found

    # Find optimal number of clusters
    num_clusters = find_optimal_clusters(red_pixel_indices)

    # Cluster the red pixels to find centers
    kmeans = KMeans(n_clusters=num_clusters)
    kmeans.fit(red_pixel_indices)
    centers = kmeans.cluster_centers_

    # Prepare the cropped images
    cropped_images = []
    for center in centers:
        x, y = int(center[1]), int(center[0])
        left = max(x - crop_size[0] // 2, 0)
        upper = max(y - crop_size[1] // 2, 0)
        right = min(left + crop_size[0], image.width)
        lower = min(upper + crop_size[1], image.height)
        crop = image.crop((left, upper, right, lower))
        cropped_images.append(crop)

    return cropped_images

# Usage
cropped_images = find_red_areas('image_analysis/cubesat_output/03-16-2024_23:41/outage_map.png')
for i, img in enumerate(cropped_images):
    img.show()
    img.save(f'cropped_image_{i}.png')  # Uncomment to save the images