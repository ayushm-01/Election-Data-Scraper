import requests
from bs4 import BeautifulSoup
import pandas as pd


def extract_data(soup):
    data = []

    # Extract Parliamentary Constituencies data
    pc_data = soup.find('div', class_='pc-wrap')
    if pc_data:
        data.append({
            "Constituency": "Parliamentary Constituency",
            "State": "",
            "Total Seats": pc_data.find('h1').text.strip()
        })

    # Extract Assembly Constituencies data
    ac_data = soup.find_all('div', class_=['olive-bg', 'pine-bg', 'gry-bg'])
    for item in ac_data:
        state = item.find('h2').text.strip()
        total_seats = item.find('h1').text.strip()
        data.append({
            "Constituency": "Assembly Constituency",
            "State": state,
            "Total Seats": total_seats
        })

    # Extract additional states
    additional_states = soup.find_all('a', class_='btn-big')
    for state in additional_states:
        data.append({
            "Constituency": "Assembly Constituency",
            "State": state.text.strip(),
            "Total Seats": "N/A"
        })

    return data


if __name__ == "__main__":
    URL = "https://results.eci.gov.in"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/91.0.4472.124 Safari/537.36'
    }

    # Fetch webpage content
    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract data
    election_data = extract_data(soup)

    # Create DataFrame
    df = pd.DataFrame(election_data)

    # Display the DataFrame
    print(df)
