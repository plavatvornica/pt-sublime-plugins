import sublime, sublime_plugin
import subprocess

locations = {
    'dev': 'root@wiki.dev.',
    'live': 'root@plavatvornica.com.'
}

class DownloadWordpressCommand(sublime_plugin.WindowCommand):

    def run(self):
        sublime.active_window().show_quick_panel(list(locations.keys()), self.location_chosen, sublime.MONOSPACE_FONT)

    def location_chosen(self, i):
        keys = list(locations.keys())
        location = locations[keys[i]]

        sublime.active_window().show_input_panel('Upisi korisnika (vlasnika) projekta', 'user', self.user_chosen, None, None)

        self.location = location

    def user_chosen(self, user):
        sublime.active_window().show_input_panel('Upisi path do projekta', '/home/%s/public_html/' % user, self.path_chosen, None, None)

        self.user = user

    def path_chosen(self, path):
        self.path = path

        self.run_script()

    def run_script(self):
        cmd = "ssh %s './scripts/download_wordpress %s --path %s'" % (self.location, self.user, self.path)
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = process.communicate()

        output = list(map(lambda x: x.decode(encoding='UTF-8'), output))

        view = sublime.active_window().new_file()
        view.set_name('downloading wordpress...')
        view.run_command('insert', {'characters': output[0]})

