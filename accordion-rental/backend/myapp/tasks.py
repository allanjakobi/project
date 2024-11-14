from background_task import background
from django.utils import timezone
from .models import Rendipillid

@background(schedule=30)  # 30 seconds (30 sec)
def reset_instrument_status(instrument_id):
    print("RESET STARTED")
    try:
        instrument = Rendipillid.objects.get(instrumentId=instrument_id)
        # Check if the instrument is still "Reserved"
        if instrument.status == "Reserved":
            instrument.status = "Available"
            instrument.save()
            print("RESET successful")
            print(f"Instrument {instrument_id} status reset to 'Available'")
    except Rendipillid.DoesNotExist:
        print(f"Instrument {instrument_id} does not exist.")
