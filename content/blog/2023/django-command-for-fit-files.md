title: Django Command for FIT files
slug: django-command-for-fit-files
date: 2023-05-21
tags: python, django, running

FIT - [Flexible and Interoperable Transfer](https://developer.garmin.com/fit/protocol/) - is a protocol designed for storing and sharing data from fitness and health devices.

Since getting a [Coros](https://coros.com/) running watch in July 2022, I've been exporting the FIT file data to Dropbox after every run.

Having all of this data laying around seemed like a good excuse for a toy project.<sup>1</sup> I haven't done much web programming in the last five years, so I opted to build a little web app with Django.

## FIT data

The data I'm most interested in are the Session, Lap, and Record types from each file.

`Sessions` capture aggregated data about your run - things like total distance, average heart rate, average speed, etc.

`Laps` capture aggregated data about a particular lap of your run. By default, my watch creates one lap every mile. The fields here are similar to sessions - average heart rate, average speed, etc.

`Records` are the raw data about the run. My watch creates a new "record" every second of the run. It captures my latitude and longitude, as well as things like my heart rate, speed, cadence, estimated power output (watts), step length, etc.

To relate this data back to its source file, I've created one additional type called `Activity`. This contains the source filename and date, and also acts as a foreign key on the `Session`, `Lap`, and `Record` tables.

Mapping each of these to a Django model looks like this (I've omitted many fields for the sake of conciseness):

```python
from django.db import models


class Activity(models.Model):
    source_filename = models.FilePathField(unique=True)
    began_at = models.DateTimeField(null=True)

class Session(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    total_elapsed_time = models.FloatField()
    avg_heart_rate = models.PositiveSmallIntegerField()
    # ... many more fields

class Lap(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    total_elapsed_time = models.FloatField()
    avg_heart_rate = models.PositiveSmallIntegerField()
    # ... more fields omitted

class Record(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    position_lat = models.CharField(max_length=255, null=True)
    position_long = models.CharField(max_length=255, null=True)
    heart_rate = models.PositiveSmallIntegerField(null=True)
    # ... more fields omitted
```

## Ingest command

Django allows you to register [custom commands](https://django.readthedocs.io/en/stable/howto/custom-management-commands.html#module-django.core.management) with your application that can be run via `manage.py`. This is useful for standalone scripts or ones that you'll want to regularly run.


First, some helper functions to use within the command:

```python
def convert_frame_to_dict(frame) -> Dict[str, Any]:
    return {field.name: field.value
            for field in frame.fields}
```
Data rows from the FIT file are message objects with a property containing the fields, and each field containing a name and value. `convert_frame_to_dict` converts these to dictionaries so they're easier to work with.


```python
def extract_datetime_from_filename(filename: str) -> str:
    regex = r"([0-9]+).fit"
    match = re.search(regex, filename)
    if not match:
        return

    try:
        dt = datetime.strptime(match.group(1), "%Y%m%d%H%M%S")
    except ValueError:
        return
    return dt
```
File names from Coros contain a timestamp marking when the run began (e.g. `Run20230520091606.fit`). `extract_datetime_from_filename` parses out that timestamp so it can be stored in the database.

```python
def determine_files_for_ingest(filepaths: List[Path]) -> List[Path]:
    """
    Given a list of filepaths, compare with DB to determine which ones should be ingested.
    Returns a list of filepaths in need of ingest.
    """
    # get a list of all the files in the DB
    ingested_files = Activity.objects.values_list("source_filename", flat=True)

    needs_ingest = []
    for fp in filepaths:
        if fp.name not in ingested_files:
            needs_ingest.append(fp)
    return needs_ingest
```
Since I will call this command after every run, `determine_files_for_ingest` compares the FIT file directory with what's already been loaded into the database.

With [fitdecode](https://github.com/polyvertex/fitdecode) doing the heavy lifting, my custom command looks like below:

```python
class Command(BaseCommand):
    help = "Loads FIT file(s) into the database"

    def add_arguments(self, parser):
        parser.add_argument("fitfile_dir", type=str)

    def handle(self, *args, **options):
        fitfile_dir = Path(options["fitfile_dir"])
        filepaths = fitfile_dir.glob("*Run*.fit")

        # filter out any files that are already in the DB
        needs_ingest = determine_files_for_ingest(filepaths)
        self.stdout.write(f"Found {len(needs_ingest)} files to ingest")

        if not needs_ingest:
            return

        # extract date from filename so we can process in chronological order
        filepaths = {extract_datetime_from_filename(fp.name): fp
                     for fp in needs_ingest}

        for _, fp in sorted(filepaths.items()):
            self.stdout.write(f"Loading {fp.name} to database")

            try:
                self.process_fitfile(fp)
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"Failed to load {fp.name} to database", e)
                )

            self.stdout.write(
                self.style.SUCCESS(f"Successfully loaded {fp.name} to database")
            )

    def process_fitfile(self, filepath: Path):
        with fitdecode.FitReader(filepath) as fit:
            activity = Activity.objects.create(
                source_filename=filepath.name,
                began_at=extract_datetime_from_filename(filepath.name)
            )

            for frame in fit:
                if frame.frame_type != fitdecode.FIT_FRAME_DATA:
                    continue

                data = convert_frame_to_dict(frame)

                if frame.name == 'session':
                    self.create_session(data, activity)
                if frame.name == 'lap':
                    self.create_lap(data, activity)
                if frame.name == 'record':
                    self.create_record(data, activity)
```
I've ommitted the code for `create_session`, `create_lap`, and `create_record`. Each just instantiates the appropriate model and calls its `save` method.

Running the command with `manage.py`:
```bash
$ python manage.py ../Apps/coros
```

The payoff? Now I can easily write SQL queries against my running data!

```bash
$ sqlite3 db.sqlite3 < sql/weekly_totals.sql -table
+---------+---------------+-------+--------------+----------+
|  week   | hours_running | miles | feet_climbed | calories |
+---------+---------------+-------+--------------+----------+
| 2023-14 | 3.5           | 21.8  | 883.0        | 2408.0   |
| 2023-15 | 3.6           | 22.2  | 1316.0       | 2375.0   |
| 2023-16 | 4.3           | 28.3  | 1486.0       | 3102.0   |
| 2023-17 | 4.8           | 30.6  | 2139.0       | 3328.0   |
| 2023-18 | 2.2           | 14.5  | 912.0        | 1703.0   |
| 2023-19 | 4.8           | 31.0  | 1686.0       | 3626.0   |
| 2023-20 | 5.2           | 33.6  | 1765.0       | 3871.0   |
+---------+---------------+-------+--------------+----------+
```

Sure, Strava already does a lot of this, but where's the fun in that?

<hr>

1. My history with side projects is one of abandonment.