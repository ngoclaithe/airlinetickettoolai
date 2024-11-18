from .flight import Flight
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