import re
from xml.etree import ElementTree as ET
from datetime import datetime, date, timedelta

import requests
from icalendar import Calendar, Event

params = {
    'ajax': 1,
    'ajax_token': 'blabalablalbablalbababllbalal',
    'action': 'loadPlanningCourse',
    'id_class': 0,
    'dataType': 'xml',
    'firstDisplay': True,
}


def webhook_notifier(type: str, url: str):
    """
    Send a notification to the specified service with the ics file in
    attachment.
    """
    if type == 'discord':
        print('Send a notification on Discord.')
        requests.post(
            url=url,
            data={
                'content': '🚀 A new version of the timetable is available 💪'
            },
            files={'file': open('calendar.ics', 'r')},
        )
    elif type is None:
        return
    else:
        print('Unknown service, no notification sent.')


def edt2ics(
    url: str,
    days_limit=999,  # Big number of days by default
    notifier_type: str = None,
    notifier_url: str = None,
):
    """
    Retrieves the timetable of the specified classroom for the specified
    period.
    """
    # Retrieve the ajax token
    token_retrieve = requests.post(url, params).json()['result']
    params['ajax_token'] = re.search(r"!=(\S+)\]", token_retrieve).group(1)
    params['id_class'] = re.search(r"\d+$", url).group(0)

    # Retrieve the planning with the new AJAX token
    edt_retrieve = requests.post(url, params).json()['result']

    # Parse the xml and create a python readable object
    edt = ET.fromstring(edt_retrieve)

    # Variables for managing the days limit
    today = datetime.today()
    limit_date = today + timedelta(days=+days_limit)

    # Create a new calendar
    cal = Calendar()

    for evt in edt:
        evt = {
            'course': evt.attrib['title'],
            'teacher': evt.attrib['teacher'],
            'date_start': datetime.strptime(
                evt.attrib['start'], '%Y-%m-%d %H:%M:%S'
            ),
            'date_end': datetime.strptime(
                evt.attrib['end'], '%Y-%m-%d %H:%M:%S'
            ),
        }

        # fmt: off
        # (Disable black because it's not make petty things here :/)
        # Don't record the event if is already passed or if is after the
        # limit date.
        if (
            evt['date_start'] > today and evt['date_start'] > limit_date or
            evt['date_start'] < today
        ):
            continue

        # fmt: on
        # Create iCalendar event and add it to the global calendar
        cal_event = Event(

        )
        cal_event.add('DTSTART', evt['date_start'])
        cal_event.add('DTEND', evt['date_end'])

        if evt['teacher'] != ' ':
            summary = '{} - {}'.format(evt['course'], evt['teacher'])
        else:
            summary = evt['course']

        cal_event.add('SUMMARY', summary)
        cal.add_component(cal_event)

    # Make a diff if the file already exists and/or write new changes
    with open('calendar.ics', 'a+', encoding='utf-8') as f:
        f.seek(0)  # Put the cursor on the top
        file_content = f.read()
        # Convert CRLF to LF (for the condition)
        ical = cal.to_ical().decode('utf-8').replace('\r\n', '\n')

        # Writes the new file if the content have differences and if the new
        # ical variable have events in there
        if file_content != ical and ical != 'BEGIN:VCALENDAR\nEND:VCALENDAR\n':
            print('Writing a new ICS file.')
            f.truncate(0)
            f.write(ical)
            webhook_notifier(notifier_type, notifier_url)
        else:
            print('No updates found, nothing to do.')

        f.close()


# Execute the script when is spawned by python directly
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('url', type=str, help='URL of the teamtable')
    parser.add_argument(
        '--days-limit',
        dest='days_limit',
        type=int,
        default=999,  # Big number of days by default
        help='Days limit the script it retrieve',
    )
    parser.add_argument(
        '--notifier',
        type=str,
        help='Specify the messaging service used for notifying (see the doc)',
    )
    parser.add_argument(
        '--notifier-url',
        dest='notifier_url',
        type=str,
        help='Webhook link for sending the notification to the '
        'messaging service',
    )

    args = parser.parse_args()

    edt2ics(
        url=args.url,
        days_limit=args.days_limit,
        notifier_type=args.notifier,
        notifier_url=args.notifier_url,
    )
