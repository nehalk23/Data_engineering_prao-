import requests
import csv  # ✅ Required for writing to CSV

url = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1/rankings/batsmen"
querystring = {"formatType": "test"}

headers = {
    "x-rapidapi-key": "9b428a58efmsh38a0101cc560ba5p1f1b8cjsn8543f5dba29b",
    "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

if response.status_code == 200:
    data = response.json().get('rank', [])  # Extracting the 'rank' list
    csv_filename = 'batsmen_rankings2.csv'

    if data:
        field_names = ['rank', 'name', 'country']  # Fields to include in CSV

        # Write data to CSV
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=field_names)
            writer.writeheader()  # Optional: include headers in the CSV
            for entry in data:
                writer.writerow({field: entry.get(field) for field in field_names})

        print(f"✅ Data fetched successfully and written to '{csv_filename}'")
    else:
        print("⚠️ No data available from the API.")
else:
    print("❌ Failed to fetch data:", response.status_code)
