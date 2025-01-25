# golden-hour

A python script to generate a timelapse video. Designed specifically to record at sunset, and post to Bluesky with a weather report.

## Setup

This project assumes that you will run this on [a Raspberry Pi][pi] with a CSI-port [camera], although pull requests to broaden that support are certainly accepted. Original code from [goldenhourSEA]. This version has run on [a Raspberry Pi Zero W][zero-w]. 

[pi]: https://www.raspberrypi.org
[camera]: https://www.raspberrypi.org/products/camera-module-v2/
[goldenhourSEA]: https://twitter.com/goldenhourSEA
[zero-w]: https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/

### Installation

#### Installing [`FFmpeg`][ffmpeg]

FFmpeg is used to convert the sequence of photos captured by the camera into a video suitable for uploading to Bluesky. FFmpeg must be compiled with x264 support. On a Raspberry Pi running Raspbian, simply `sudo apt install ffmpeg`. If you are running this on a Mac, `brew install ffpmeg` should be sufficient.

[ffmpeg]: http://ffmpeg.org

#### Installing `golden-hour`

1. Check out this repo to a convenient location on your Pi.
2. Run `pip install .`
3. Run `golden-hour --help` to check that it's hooked up right!

#### Configuration

Configuration data - Bluesky and Openweather credentials, and location information, will all live in a `.yaml` file.
You should put this in `~/.config/golden-hour.yaml` as there are several hardcoded dependencies for this path (sorry, I'm lazy and the only user).
Check out `example_config.yaml` for the expected format of the file.

##### Location

So that `golden-hour` knows when sunset or sunrise will happen, tell it where the camera is located via the configuration file. For many major cities, you can just specify the city name. The yaml also accepts longitude, latitude, and elevation for greater accuracy.
See `example_config.yaml` for the format.

##### Bluesky

1. Create a Bluesky account.
    - It is recommended to use a name like "goldenhourXYZ", where XYZ is airport code or abbrevation for your city.
2. No seperate developer console or app configuration is needed at this time. Bluesky is built on the [atproto libraries][atproto]. There is a python library available of [PyPi][pypi]

[atproto]: https://docs.bsky.app/docs/get-started
[pypi]: https://pypi.org/project/atproto/

##### Open Weather *(optional)*
[Open Weather][openweather] is used to get weather information and post the weather and forecast at the location of the timelapse. Their free account should more than sufficient to run Golden Hour code. 

[openweather]: https://openweathermap.org/api


#### Running as a one-off

Once it's installed, run `golden-hour --help` for usage instructions.
If you get the error "`-bash: golden-hour: command not found`", you may need to restart your shell or check that `golden-hour` is installed somewhere on your `PATH`. See "Gotchas" below.

#### Running automatically

Once you have everything set up, set up a cron job to run `golden-hour` at the same time every day. Make sure it runs at least one hour before the earliest sunset of the year. You can find this by looking at the "Sun Graph" for your city at timeanddate.com (for example, [here is Seattle](https://www.timeanddate.com/sun/usa/seattle)).

Example crontab entry (Insert this into your user's crontab with `crontab -e`):
```cron
0 15 * * *  golden-hour --start-before-sunset 60  --post-to-bluesky
```
You can also leverage virtualenvs using a `.sh` file that is executed in the cron command.

Here is an example of what the `.sh` could look like:
```#!/bin/bash

cd install-directory
source bin/activate

golden-hour --start-before-sunset 60 --post-to-bluesky
```

##### Where are the logs?

When it is run by `cron`, by default `golden-hour` will send logs to syslog. You can monitor them with `tail -F /var/log/syslog`. Default logging is `INFO`.

##### Gotchas:

- depending on how you installed `golden-hour`, you will need to make sure that it's on your `PATH`. This may mean adding something like `PATH=~/.local/bin:/usr/local/bin:$PATH` to your crontab and your `~/.bash_profile`, or activating a virtualenv.
- `cron` runs in a different environment from your normal shell. In my case, it did not have access to `ffmpeg`, because I had installed it to `/usr/local/bin`, but the `$PATH` only had `/bin` and `/usr/bin`.
- Your Pi may not be configured to your local timezone. Run `date` to see what time it is for your Pi, and set the cron job to run at an appropriate translated time. I set mine to run at 2300, which is 3pm local time.
- If using virtual environments the file output might end up in your /venv/ folder directory, making it hard to track. This was solved by hardcoding the output directory to the user home directory (sorry, still lazy), but can be modified to use relative path if forking the code.
