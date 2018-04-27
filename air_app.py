import datetime

import requests
import rumps

SITE_NAME = '基隆'


class App(rumps.App):
    url = 'http://opendata2.epa.gov.tw/AQI.json'
    site_name = SITE_NAME

    def __init__(self):
        super(App, self).__init__("🏖️")
        self.menu.add(rumps.MenuItem(title='Refresh Time'))
        self.menu.add(rumps.MenuItem(title='Air!'))
        self.menu.add(rumps.separator)
        self.menu.add(rumps.MenuItem(title='Help'))
        # rumps.debug_mode(True)

    def get_air(self, session):
        result = ""
        aqi = 0

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

    def get_monitor_area(self, session):
        result = []

        repo = session.get(self.url)
        if repo.status_code == 200:
            for data in repo.json():
                result.append(data.get('SiteName'))

        return result

    """ Can't work because RUMPS has a bug about type string in textbox. """
    # @rumps.clicked("Setting")
    # def area_setting(self, sender):
    #     setting_window = rumps.Window(
    #         message='Set where you want to monitor air area',
    #         title='Preferences',
    #         default_text=self.site_name,
    #         ok="Submit",
    #         cancel='Cancel',
    #         dimensions=(100, 20)
    #     )

    #     resp = setting_window.run()
    #     if resp.clicked:
    #         print(resp.text)
    #         self.site_name = resp.text

    # @rumps.clicked("Air!")
    @rumps.timer(60 * 60)
    def get_air_quality(self, sender):
        sender = self.menu['Air!']  # if action no bind on clicked action

        def counter(t):
            with requests.Session() as s:
                sender.title, aqi = self.get_air(s)

                self.menu['Refresh Time'].title = (
                    f"Updated:"
                    f"{datetime.datetime.now().strftime('%m-%d %H:%M:%S')}"
                )

                # menu title (icon)
                self.title = ''.join([f"{int(i, 16)}" for i in aqi])

        # if bind on clicked action
        # set_timer = rumps.Timer(callback=counter, interval=60 * 60)
        # set_timer.start()

        counter(None)

    @rumps.clicked("Help")
    def area_setting(self, sender):
        with requests.Session() as s:
            area_list = self.get_monitor_area(s)

            show_window = rumps.Window(
                message='All area name',
                title='Area List',
                default_text=area_list,
                ok=None,
                dimensions=(300, 200)
            )

            show_window.run()


if __name__ == "__main__":
    myapp = App()
    myapp.run()
