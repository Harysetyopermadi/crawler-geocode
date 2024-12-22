import pandas as pd
from geopy.geocoders import Nominatim
import folium
from tqdm import tqdm

# Load the dataset
df = pd.read_csv('D:\\Python\\geocode\\public\\data.txt', sep='|')
#df = df.head(100)

# Geocoding function
def get_location_details(latitude, longitude):
    geolocator = Nominatim(user_agent="my_unique_application")
    try:
        location = geolocator.reverse((latitude, longitude), language='en', timeout=10)
        if location:
            address = location.raw.get('address', {})
            full_address = location.address
            city = address.get('city', address.get('town', address.get('village', 'Tidak Diketahui')))
            country = address.get('country', 'Tidak Diketahui')
            return full_address, city, country
        else:
            return None, None, None
    except Exception as e:
        print(f"Error: {e}")
        return None, None, None

# Initialize tqdm for progress bar
tqdm.pandas()

# Apply the geocoding function to the DataFrame with a progress bar
df[['alamat', 'kota', 'Negara']] = df.progress_apply(
    lambda row: pd.Series(get_location_details(row['latitude'], row['longitude'])), axis=1
)

print(df)
df.to_excel('hasil.xlsx')
