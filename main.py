from datetime import datetime, date, timedelta
from gcsa.google_calendar import GoogleCalendar
from voice import Voice
import subprocess, sys

def generate_script(events):
    num_events = 0
    script_events = ""
    for event in events:
        num_events += 1
        start = event.start.strftime("%I %M %p")
        if event.start.strftime("%M")=="00":
            start = event.start.strftime("%I %p")

        print(event.summary, event.start)
        script_events += "You have " + event.summary + " at " + start + ". "

    _script = "You have " + str(num_events) + " events today. " + script_events
    script = _script.replace(" 0", " ")
    print(script)
    wav = Voice.say_to_wav(script)

    subprocess.run(["ffmpeg", "-y" "-i", wav, "-acodec", "pcm_s16le", "-ac", "1", "-ar", "8000", "/var/lib/asterisk/sounds/custom/wakeup-message.wav"])

def main(scheduled=date.today()):
    calendar = GoogleCalendar()

    # Read events within a specific timeframe
    events = calendar.get_events(time_min=scheduled, time_max=scheduled + timedelta(days=1))
    generate_script(events)

if __name__ == "__main__":
    date_format = "%Y-%m-%d+%H:%M:%S"
    dt_back = 0
    if len(sys.argv) > 0:
        try:
            dt_back = datetime.strptime(sys.argv[1], date_format)
        except Exception as e:
            print("Failed to unstringify date: ", e)
            sys.exit(1)
        main(dt_back)
    else:
        main()
