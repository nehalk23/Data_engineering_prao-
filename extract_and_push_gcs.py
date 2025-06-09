import requests
import csv
from google.cloud import storage
import os

# OPTIONAL: If you haven't set credentials globally
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/your-service-account-key.json"

# API endpoint for batsmen rankings
url = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1/rankings/batsmen"

# Query parameter for Test format
querystring = {"formatType": "test"}

# API headers
headers = {
    "x-rapidapi-key": "9b428a58efmsh38a0101cc560ba5p1f1b8cjsn8543f5dba29b",
    "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
}

# Send request
response = requests.get(url, headers=headers, params=querystring)

# Check API response
if response.status_code == 200:
    json_data = response.json()

    # Extract 'rank' list
    data = json_data.get('rank', [])

    if data:
        csv_filename = 'batsmen_rankings2.csv'
        field_names = ['rank', 'name', 'country']

        # Save data to CSV
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=field_names)
            writer.writeheader()
            for entry in data:
                writer.writerow({
                    'rank': entry.get('rank', ''),
                    'name': entry.get('name', ''),
                    'country': entry.get('country', '')
                })

        print(f"✅ Batsmen rankings written to '{csv_filename}'")

        # Upload to GCS
        try:
            bucket_name = 'dl-agent'
            destination_blob_name = csv_filename

            storage_client = storage.Client()
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(destination_blob_name)
            blob.upload_from_filename(csv_filename)

            print(f"✅ File uploaded to GCS bucket '{bucket_name}' as '{destination_blob_name}'")
        except Exception as e:
            print("❌ Error uploading to GCS:", e)
    else:
        print("⚠️ No 'rank' data found in API response.")
else:
    print(f"❌ Failed to fetch data. Status code: {response.status_code}")
