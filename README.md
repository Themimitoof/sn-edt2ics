# Scholanova EDT2ICS
This script permit anyone studing at Scholanova, to retrieve the timetable (_emploi du temps_) and convert it in [iCalendar](https://fr.wikipedia.org/wiki/ICalendar) format for importing it in her agenda.

This script makes a first request for retrieving the AJAX token (because the payload send a string explaining the error with the AJAX token 🤷). After that, it make a new request with the AJAX token, parse the XML payload (yep it's a XML payload inside a JSON payload...), create a calendar by inserting all created events (or all events up to the specified limit) and create a _ics file_. If a _messaging service_ (example: Discord) and a _webhook URL_ was sent in parameters, it send a message with the _ics file_ in attachment.

## Features
 * Retrieves the timetable and store it in a _ics file_.
 * Can limit the number of days retrieved by the script
 * Can notify on a messaging service and sending the _ics file_ in attachment.

The script is compatible with theses messaging services:
 * Discord

## Prerequisites
 * _Python_ >= 3.5
 * _Poetry_ (highly recommended) or _pip_ (as fallback)
 * _Cron_ or similar
 * _Timetable_ url (for security reasons, it's not hardcoded for not exposing the url because anyone can access to it without authentication)

_Note:_ This script can be runned on _Function as a Service (FaaS)_ platforms. It compatible with _AWS Lambda_, _Azure Function_ and _GCloud Function_.

## Deployment
### Deployment on Linux
First of all, clone this repo and use the latest tag created:
```bash
git clone https://github.com/themimitoof/sn-edt2ics.git
cd sn-edt2ics
git checkout v0.1.0
```

Create a virtualenv by using:
```bash
python -m venv venv
source venv/bin/activate
```

Now, you need to install dependencies. If you have _poetry_ installed, you can use ```poetry install```. If isn't, you can use _pip_ by using the command ```pip install -r requirements.txt```.

....
```bash
python edt2ics.py \
    --url <url> \
    --class_id <integer> \
    --notifier discord \
    --notifier_url https://discordapp.com/api/webhooks/<id>/<token>
```

Finally, you can configure _cron_ task to run the script periodically. For this, run the command ```crontab -e``` and add your configuration. For example, for running the script each fridays at 0h00:
```cron
0 0 * * 5 python /opt/sn-edt2ics/ python edt2ics.py --url <url> --class_id <integer> --notifier discord --notifier_url https://discordapp.com/api/webhooks/<id>/<token> >> /tmp/log/sn-edt2ics.log
```

### Deploy on AWS Lambda
...

### Deploy on Azure Functions
...

### Deploy on GCloud Functions
...


## Contributions
You can create a _Pull request_ for sending your contributions or create an issue for reporting a bug or adding a _messaging provider_.

**Note:** This project use [black](https://github.com/ambv/black) and is conform as max as possible to the _PEP8_.

## License
This script is shipped with MIT license.