## Copies images from example bucket to ours , warning this takes a while
import os
from google.cloud import bigquery
from google.cloud import storage

BQ_CLIENT = bigquery.Client()


animals = ['Dolphin', 'Fox', 'Horse', 'Butterfly', 'Cat', 'Dog', 'Bee', 'Pig', 'Goose', 'Sea turtle']

## for each animal queries the image names
for animal in animals:
    print("Querying animal " + animal)
    results = BQ_CLIENT.query(
            '''
            SELECT imageId
            FROM  `big-data-project1-347618.dataset1.classes`
            JOIN  `big-data-project1-347618.dataset1.labels` USING(label)
            WHERE description = '{0}'
            ORDER BY Description ASC
        '''.format(animal)).result()
    print("Inserting images in other bucket")
    for row in results:
        imageId = row[0]
        ## Copies from one bucket to another
        #print(imageId)
        os.system("gsutil cp gs://bdcc_open_images_dataset/images/"+imageId+".jpg gs://project1-openimages/images/"+imageId+".jpg")



#PROJECT = os.environ.get('GOOGLE_CLOUD_PROJECT')
#BQ_CLIENT = bigquery.Client()

#BUCKET_NAME = "project1-openimages"
#print('Initialising access to storage bucket')
#APP_BUCKET = storage.Client().bucket(BUCKET_NAME)




