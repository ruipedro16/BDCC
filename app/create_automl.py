## This script filters the automl.csv file
from google.cloud import bigquery

animals = ['Dolphin', 'Fox', 'Horse', 'Butterfly', 'Cat', 'Dog', 'Bee', 'Pig', 'Goose', 'Sea turtle']
PROJECT_ID = 'big-data-project1-347618'
print("Overwritting automl.csv")
f = open("automl.csv", "w")

gsurl = "gs://project1-openimages/images/"
BQ_CLIENT = bigquery.Client(project=PROJECT_ID)


## for each animal get 100 imageIds
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
    print("asd")
    count = 0
    for row in results:
        if count >= 100:
            break
        
        imageId = row[0] ## get the imageId

        text = ""
        if count < 80:
            text +="TRAIN,"
        elif count >= 80 and count <90:
            text +="VALIDATION,"
        else:
            text +="TEST,"
        text+=gsurl+imageId+".jpg,"+animal+"\n"
        f.write(text)
        count = count + 1

