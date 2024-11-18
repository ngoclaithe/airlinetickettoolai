import re
import hashlib
def parse_description(description):
    match = re.search(r"(.+? - .+?)\s+([A-Z]{3} \d{2} \w+ \d{4})", description)
    
    if match:
        flight_number_airline = match.group(1).strip()  
        flight_time = match.group(2).strip()            
        return flight_number_airline, flight_time

    return description, ""

def parse_departure(departure):
    datetime_match = re.search(r"\d{2}\s\w{3}\s\d{2}:\d{2}", departure)

    if datetime_match:
        date_time = datetime_match.group(0).strip()

        departure = departure.replace(date_time, "").replace("\n", " ").strip()
        departure = re.sub(r"\s+", " ", departure)

        match = re.match(
            r"^(.*?)(?:,\s*(TERMINAL \d+))?\s*(TERMINAL \d+)?\s*$", departure.strip()
        )

        if match:
            location = match.group(1).strip() if match.group(1) else ""
            terminal = match.group(2) if match.group(2) else match.group(3) or ""
            terminal = terminal.strip() if terminal else ""
            return location, terminal, date_time

    return None

def parse_arrival(arrival):
    datetime_match = re.search(r"\d{2}\s\w{3}\s\d{2}:\d{2}", arrival)
    if datetime_match:
        date_time = datetime_match.group(0).strip()

        arrival = arrival.replace(date_time, "").replace("\n", " ").strip()
        arrival = re.sub(r"\s+", " ", arrival)

        match = re.match(
            r"^(.*?)(?:,\s*(TERMINAL \d+))?\s*(TERMINAL \d+)?\s*$", arrival.strip()
        )

        if match:
            location = match.group(1).strip() if match.group(1) else ""
            terminal = match.group(2) if match.group(2) else match.group(3) or ""
            terminal = terminal.strip() if terminal else ""
            return location, terminal, date_time

    return None

def check_flight_pattern(data1, data2):
    missing_info = []

    patterns = [
        "DEPARTURE", "ARRIVAL", "RESERVATION", 
        "BAGGAGE ALLOWANCE", "NON STOP", "EQUIPMENT", "MEAL"
    ]

    for i, data in enumerate([data1, data2], start=1):
        for pattern in patterns:
            if not any(re.search(pattern, line) for line in data):
                missing_info.append(f"Thiếu {pattern} trong info phiếu bay {i}")
    print(missing_info)
    return missing_info

def extract_flight_info(data):
    flight_info = {}
    flight_info['Description'] = data[0].replace('FLIGHT', '').strip()
    flight_info['Equipment'] = data[2].replace('EQUIPMENT:', '').strip()

    lines = data[1].strip().split('\n')
    
    departure_info = []
    arrival_info = []
    is_departure = False
    is_arrival = False

    for line in lines:
        line = line.strip()
        
        if line.startswith('DEPARTURE:'):
            is_departure = True
            departure_info.append(line.replace('DEPARTURE:', '').strip())
        elif line.startswith('ARRIVAL:'):
            is_departure = False
            is_arrival = True
            arrival_info.append(line.replace('ARRIVAL:', '').strip())
        elif is_departure:
            departure_info.append(line)
        elif is_arrival:
            if 'FLIGHT BOOKING REF' in line:
                arrival_info.append(line.split('FLIGHT BOOKING REF')[0].strip())
                is_arrival = False  
            else:
                arrival_info.append(line)

        if 'DURATION:' in line:
            parts = line.split('DURATION:')
            flight_info['Economy Class'] = parts[0].strip().replace('RESERVATION CONFIRMED, ', '')
            flight_info['Duration'] = parts[1].strip()
        elif 'BAGGAGE ALLOWANCE:' in line:
            flight_info['Baggage'] = line.replace('BAGGAGE ALLOWANCE:', '').strip()
        elif 'MEAL:' in line:
            flight_info['Meal'] = line.replace('MEAL:', '').strip()
        elif 'NON STOP' in line:
            flight_info['NonStop'] = line.replace('NON STOP', '').strip()

    flight_info['Departure'] = '\n'.join(departure_info).strip()
    flight_info['Arrival'] = '\n'.join(arrival_info).strip()

    return flight_info
def abbreviated_place_name(place):
    if place.strip().upper() == "HANOI, VN (NOI BAI INTL)":
        return "HN"
    parts = place.strip().split(",")[0].strip().split()
    abbreviation = ''.join([part[0].upper() for part in parts])
    
    return abbreviation
def abbreviate_airport_name(input_str):
    airport_codes = {
        "HANOI": "HAN",
        "HOCHIMINHCITY": "SGN",
        "DANANG": "DAD",
        "PHUQUOC": "PQC",
        "NHATRANG": "CXR",
        "BUONMATHUOT": "BMV",
        "CAMAU": "CAH",
        "CANTHO": "VCA",
        "CHULAI": "VCL",
        "CONDAO": "VCS",
        "DALAT": "DLI",
        "DIENBIEN": "DIN",
        "DONGHOI": "VDH",
        "HAIPHONG": "HPH",
        "HUE": "HUI",
        "PLEIKU": "PXU",
        "QUYNHON": "UIH",
        "RACHGIA": "VKG",
        "THANHHOA": "THD",
        "TUYHOA": "TBB",
        "VANDON": "VDO",
        "VINH": "VII"
    }

    cleaned_str = input_str.replace(" ", "").upper()

    for city, code in airport_codes.items():
        if city in cleaned_str:
            return code
    return input_str
def md5_hash(text):
    return hashlib.md5(text.encode()).hexdigest()
