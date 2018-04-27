# air-quality-app
**This is a example.**

It work on OS X **v10.13.3**

OS X App for monitor Taiwan air quality by python rumps.

## Requirement
  * Python == 3.6
  * [rumps](https://github.com/jaredks/rumps) == 0.2.2
  * [requests](https://github.com/requests/requests) == 2.18.4

## Run app
```bash
$ python air_app.py
```

Recommended use [PM2](https://github.com/Unitech/PM2) for work on background.

```bash
$ pm2 start air_app.py --name my_example_app
```

## License
MIT license.
