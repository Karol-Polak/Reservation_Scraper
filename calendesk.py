from datetime import date

import requests


API_URL = "https://api.calendesk.com/api/available-slots"

HEADERS = {
    "Accept": "application/json",
    "Origin": "https://www.dorotajoannamejna.com",
    "Referer": "https://www.dorotajoannamejna.com/",
    "X-Requested-With": "XMLHttpRequest",
    "X-Tenant": "evprtw7keq",
    "X-Draft-Uuid": "45e95d6d-23b2-44f9-b370-a224049ffe03",
}


def get_slots():
    params = {
        "used_slots": 1,
        "booked_slots": 0,
        "number_of_days": 70,
        "service_id": 2,
        "employee_ids": 1,
        "start_date": date.today().isoformat(),
        "service_type_id": 1,
        "customer_time_zone": "Europe/Warsaw",
        "location_id": 2,
    }

    response = requests.get(
        API_URL,
        params=params,
        headers=HEADERS,
        timeout=15,
    )

    response.raise_for_status()

    return response.json()