import datetime

import requests
import rumps

SITE_NAME = '基隆'   # default value


class App(rumps.App):
    url = 'http://opendata2.epa.gov.tw/AQI.json'
    site_name = SITE_NAME

    def __init__(self):
        super(App, self).__init__("🏖️")
        self.menu.add(rumps.MenuItem(title='Refresh Time'))
        self.menu.add(rumps.MenuItem(title='Air!'))
        self.menu.add(rumps.MenuItem(title='Change Area'))
        self.menu.add(rumps.separator)
        self.menu.add(rumps.MenuItem(title='Show all area'))
        # rumps.debug_mode(True)

    def get_air(self, session):
        """Query and parse AQI data."""
        result = "Not found: " + self.site_name
        aqi = -1

        repo = session.get(self.url)
        if repo.status_code == 200:
            for data in repo.json():
                if data.get('SiteName', '') == self.site_name:
                    aqi = data['AQI']
                    result = (
                        f"{data['SiteName']}:"
                        f"{data['Status']}, AQI(<100): {aqi}"
                    )
                    break

        return result, aqi

    def refresh_status(self):
        """Refresh AQI information on menu."""
        with requests.Session() as s:
            self.menu['Air!'].title, aqi = self.get_air(s)

            self.menu['Refresh Time'].title = (
                f"Updated:"
                f"{datetime.datetime.now().strftime('%m-%d %H:%M:%S')}"
            )

            # menu title (icon)
            self.title = ''.join([f"{int(i, 16)}" for i in aqi])

    def get_monitor_area(self, session):
        """Get all air monitor area."""
        area_list = []

        repo = session.get(self.url)
        if repo.status_code == 200:
            for data in repo.json():
                area_list.append(data.get('SiteName'))

        # string display format
        output = ""
        for idx, v in enumerate(area_list):
            output += v + " , "

            if idx + 1 == len(area_list):
                output = output.rstrip(", ")

            if (idx + 1) % 5 == 0:
                output += "\n"

        return output
        # return '\n'.join(area_list)

    @rumps.clicked("Change Area")
    def area_setting(self, sender):
        """ clicked "Change Area button." """
        setting_window = rumps.Window(
            message='Set where you want to monitor air area',
            title='Preferences',
            default_text=self.site_name,
            ok="Submit",
            cancel='Cancel',
            dimensions=(100, 20)
        )

        resp = setting_window.run()
        if resp.clicked:
            self.site_name = resp.text
            self.refresh_status()

    @rumps.timer(60 * 60)
    def get_air_quality(self, sender):
        """ Timer """
        # sender = self.menu['Air!']  # if action no bind on clicked action

        def counter(t):
            self.refresh_status()

        # if bind on clicked action
        # set_timer = rumps.Timer(callback=counter, interval=60 * 60)
        # set_timer.start()

        counter(None)

    @rumps.clicked("Show all area")
    def show_area(self, sender):
        """ clicked "Show all area button." """
        with requests.Session() as s:
            area_list = self.get_monitor_area(s)

            show_window = rumps.Window(
                message='All area name',
                title='Area List',
                default_text=area_list,
                ok=None,
                dimensions=(300, 300)
            )

            show_window.run()

        # self.site_name = response.text
        # self.refresh_status()


if __name__ == "__main__":
    myapp = App()
    myapp.run()
