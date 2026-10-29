from datetime import datetime, date
from gcsa.google_calendar import GoogleCalendar
from voice import Voice
import subprocess

EMAIL = "yourbuddymrcoat@gmail.com"

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

    subprocess.run(["ffmpeg", "-i", wav, "-acodec pcm_s16le -ac 1 -ar 8000 /var/lib/asterisk/sounds/custom/wakeup-message.wav"])

def main(scheduled=date.today()):
    calendar = GoogleCalendar(EMAIL)
    # Read events within a specific timeframe
    events = calendar.get_events(time_min=scheduled, time_max=scheduled + datetime.timedelta(days=1))
    generate_script(events)


if __name__ == "__main__":
    main()
