
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
    @staticmethod
    def from_dict(data):
        return Flight(
            des=data.get("des", ""),
            departure=data.get("departure", ""),
            arrival=data.get("arrival", ""),
            duration=data.get("duration", ""),
            equipment=data.get("equipment", ""),
            baggage=data.get("baggage", ""),
            meal=data.get("meal", ""),
            nonstop=data.get("nonstop", ""),
            departure_place=data.get("departure_place", ""),
            departure_terminal=data.get("departure_terminal", ""),
            departure_time=data.get("departure_time", ""),
            arrival_place=data.get("arrival_place", ""),
            arrival_terminal=data.get("arrival_terminal", ""),
            arrival_time=data.get("arrival_time", ""),
            des_time=data.get("des_time", ""),
            economy_class=data.get("economy_class", ""),
        )
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

    @staticmethod
    def from_dict(data):
        flight1 = Flight.from_dict(data["flight1"]) if data.get("flight1") else None
        flight2 = Flight.from_dict(data["flight2"]) if data.get("flight2") else None
        return Booking(
            booking_ref=data.get("booking_ref"),
            date_issue=data.get("date_issue"),
            passenger_name=data.get("passenger_name"),
            reservation_status=data.get("reservation_status"),
            ticket=data.get("ticket"),
            flight1=flight1,
            flight2=flight2,
        )
        
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