# golden-hour

A python script to generate a timelapse video. Designed specifically to record at sunset, and post to twitter with a weather report.

## Setup

This project assumes that you will run this on [a Raspberry Pi][pi] with a CSI-port camera, although pull requests to broaden that support are certainly accepted. [@goldenhourSEA][goldenhourSEA] runs on a [Pi 3 Model B][model-3] with the [Camera Module V2][camera].

[pi]: https://www.raspberrypi.org
[camera]: https://www.raspberrypi.org/products/camera-module-v2/
[goldenhourSEA]: https://twitter.com/goldenhourSEA
[model-3]: https://www.raspberrypi.org/products/raspberry-pi-3-model-b/

### Installation

#### Installing [`FFmpeg`][ffmpeg]

FFmpeg is used to convert the sequence of photos captured by the camera into a video suitable for uploading to Twitter. FFmpeg must be compiled with x264 support. On a Raspberry Pi running Raspbian, simply `sudo apt install ffmpeg`. If you are running this on a Mac, `brew install ffpmeg` should be sufficient.

[ffmpeg]: http://ffmpeg.org

#### Installing `golden-hour`

1. Check out this repo to a convenient location on your Pi.
2. Run `pip install .`
3. Run `golden-hour --help` to check that it's hooked up right!

#### Configuration

Configuration data - Twitter and Dark Sky credentials, and location information, will all live in a `.yaml` file.
You can put this wherever you want but we recommend `~/.config/golden-hour.yaml`. 
Check out `example_config.yaml` for the expected format of the file.

##### Location

So that `golden-hour` knows when sunset will happen, tell it where the camera is located via the configuration file. For many major cities, you can just specify the city name.
See `example_config.yaml` for the format.

##### Twitter

1. Create a Twitter account.
    - I recommend a name like "goldenhourXYZ", where XYZ is airport code or abbrevation for your city.
    - You may want to associate the account with a phone number, to avoid Twitter's anti-spam measures.
2. Create a [Twitter "app"][twitter-app] for that account.
    - Make sure to set the access permissions to "Read and write", otherwise you won't be able to post tweets.
    - In the root of the repo, create a `twitter_secrets.yaml` file, and put the consumer key, consumer secret, access token, and access token secret in there:

[twitter-app]: https://apps.twitter.com

##### Open Weather *(optional)*

#### Running as a one-off

Once it's installed, run `golden-hour --help` for usage instructions.
If you get the error "`-bash: golden-hour: command not found`", you may need to restart your shell or check that `golden-hour` is installed somewhere on your `PATH`. See "Gotchas" below.

#### Running automatically

Once you have everything set up, set up a cron job to run `golden-hour` at the same time every day. Make sure it runs at least one hour before the earliest sunset of the year. You can find this by looking at the "Sun Graph" for your city at timeanddate.com (for example, [here is Seattle](https://www.timeanddate.com/sun/usa/seattle)).

Example crontab entry (Insert this into your user's crontab with `crontab -e`):
```cron
0 15 * * *  golden-hour --start-before-sunset 60  --post-to-twitter
```
For another example, which uses a specially crafted `.sh` file and a virtualenv, check out [alanhussey's setup](`https://gist.github.com/alanhussey/0f5ccbd1f28e1c7d2c851bff5c496889`) . Note that this may be out of date from the latest version of code in this repo.

##### Where are the logs?

When it is run by `cron`, by default `golden-hour` will send logs to syslog. You can monitor them with `tail -F /var/log/syslog`. Default logging is `INFO`.

##### Gotchas:

- depending on how you installed `golden-hour`, you will need to make sure that it's on your `PATH`. This may mean adding something like `PATH=~/.local/bin:/usr/local/bin:$PATH` to your crontab and your `~/.bash_profile`, or activating a virtualenv.
- `cron` runs in a different environment from your normal shell. In my case, it did not have access to `ffmpeg`, because I had installed it to `/usr/local/bin`, but the `$PATH` only had `/bin` and `/usr/bin`.
- Your Pi may not be configured to your local timezone. Run `date` to see what time it is for your Pi, and set the cron job to run at an appropriate translated time. I set mine to run at 2300, which is 3pm local time.
