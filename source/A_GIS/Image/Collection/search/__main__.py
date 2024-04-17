import A_GIS
import sys

# Initialize A_GIS components and retrieve images
images, image_files = A_GIS.Image.glob(paths=sys.argv[1:])
encoder = A_GIS.Image.Encoder.init()
encoded_images = A_GIS.Image.Encoder.encode(encoder=encoder, images=images)
collection = A_GIS.Image.Collection.init()
collection = A_GIS.Image.Collection.insert(collection=collection, ids=image_files, encodings=encoded_images)
results = A_GIS.Image.Collection.search(collection=collection, encodings=[encoded_images[0]])

for i,id in enumerate(results[0].ids):
    print(i,id,results[0].distances[i])

print( ' '.join(results[0].ids) )