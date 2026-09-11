import logging

from calendesk import get_slots
from notifier import notification_exists, send_notification


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


def extract_available_slots(data):
    available_slots = []

    for employee_id, dates in data.items():
        for slot_date, slots in dates.items():
            for slot in slots:
                available_slots.append(
                    {
                        "date": slot_date,
                        "time": slot.get("time"),
                    }
                )

    return available_slots


def build_notification_message(slot):
    return (
        "Pojawił się wolny termin:\n\n"
        f"{slot['date']} {slot['time']}\n\n"
        "Rezerwacja:\n"
        "https://www.dorotajoannamejna.com"
    )


def slot_to_id(slot):
    return f"{slot['date']}|{slot['time']}"


def main():
    try:
        logging.info("Sprawdzam dostępne terminy...")

        data = get_slots()
        data = {
            "2": {
                "2109-01-01": [
                    {
                        "time": "12:14",
                        "used": 0,
                        "booked": False,
                    }
                ]
            }
        }
        available_slots = extract_available_slots(data)

        if not available_slots:
            logging.info("Brak wolnych terminów.")
            return

        logging.info(
            "Znaleziono %s wolnych terminów.",
            len(available_slots),
        )

        for slot in available_slots:
            slot_id = slot_to_id(slot)

            if notification_exists(slot_id):
                logging.info(
                    "Termin %s był już wcześniej zgłoszony.",
                    slot_id,
                )
                continue

            logging.warning(
                "NOWY WOLNY TERMIN: %s",
                slot_id,
            )

            message = build_notification_message(slot)

            send_notification(
                title=f"🚨 Wolny termin: {slot['date']} {slot['time']}",
                body=message,
                slot_id=slot_id,
            )

    except Exception:
        logging.exception(
            "Wystąpił błąd podczas sprawdzania terminów."
        )


if __name__ == "__main__":
    main()