
class Flight:
    def __init__(
        self,
        des="",
        departure="",
        arrival="",
        duration="",
        equipment="",
        baggage="",
        meal="",
        nonstop="",
        departure_place="",
        departure_terminal="",
        departure_time="",
        arrival_place="",
        arrival_terminal="",
        arrival_time="",
        des_time="",
        economy_class="",
    ):
        self.des = des
        self.departure = departure
        self.arrival = arrival
        self.duration = duration
        self.equipment = equipment
        self.meal = meal
        self.nonstop = nonstop
        self.baggage = baggage
        self.departure_place = departure_place
        self.departure_terminal = departure_terminal
        self.departure_time = departure_time
        self.arrival_place = arrival_place
        self.arrival_terminal = arrival_terminal
        self.arrival_time = arrival_time
        self.des_time = des_time
        self.economy_class = economy_class
    def to_dict(self):
        return {
            "des": self.des,
            "departure": self.departure,
            "arrival": self.arrival,
            "duration": self.duration,
            "equipment": self.equipment,
            "baggage": self.baggage,
            "meal": self.meal,
            "nonstop": self.nonstop,
            "departure_place": self.departure_place,
            "departure_terminal": self.departure_terminal,
            "departure_time": self.departure_time,
            "arrival_place": self.arrival_place,
            "arrival_terminal": self.arrival_terminal,
            "arrival_time": self.arrival_time,
            "des_time": self.des_time,
            "economy_class": self.economy_class,
        }

class Booking:
    def __init__(
        self,
        booking_ref=None,
        date_issue=None,
        passenger_name=None,
        reservation_status=None,
        ticket=None,
        flight1=None,
        flight2=None,
    ):
        self.booking_ref = booking_ref
        self.date_issue = date_issue
        self.passenger_name = passenger_name
        self.reservation_status = reservation_status
        self.ticket = ticket
        self.flight1 = flight1
        self.flight2 = flight2
    def to_dict(self):
        return {
            "booking_ref": self.booking_ref,
            "date_issue": self.date_issue,
            "passenger_name": self.passenger_name,
            "reservation_status": self.reservation_status,
            "ticket": self.ticket,
            "flight1": self.flight1.to_dict() if self.flight1 else None,
            "flight2": self.flight2.to_dict() if self.flight2 else None,
        }