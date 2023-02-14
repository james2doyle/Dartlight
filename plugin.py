from os import system

import sublime
import sublime_plugin
import subprocess
import platform


# copied logic from https://github.com/reisub0/hot-reload.vim/blob/master/autoload/hotReload.vim#L5
def run_reload():
    if platform.system() == "Darwin" or platform.system() == "Linux":
        try:
            # send SIGUSR1 to trigger a hot reload
            subprocess.call(
                "kill -s USR1 \"$(pgrep -f flutter_tools.snapshot\\ run)\" &> /dev/null", shell=True)
        except Exception as e:
            sublime.error_message(
                "FlutterDartCode: " + getattr(e, 'message', str(e)))
    else:
        # TODO support Windows
        sublime.error_message(
            "FlutterDartCode: hot reload is not supported on your platform")


def run_restart():
    if platform.system() == "Darwin" or platform.system() == "Linux":
        try:
            # send SIGUSR2 to trigger a hot restart
            subprocess.call(
                "kill -s USR2 \"$(pgrep -f flutter_tools.snapshot\\ run)\" &> /dev/null", shell=True)
        except Exception as e:
            sublime.error_message(
                "FlutterDartCode: " + getattr(e, 'message', str(e)))
    else:
        # TODO support Windows
        sublime.error_message(
            "FlutterDartCode: hot reload is not supported on your platform")


class FlutterDartCode(sublime_plugin.EventListener):
    def on_post_save_async(self, view):
        file_path = view.file_name()
        if not file_path:
            return
        NOT_FOUND = -1
        pos_dot = file_path.rfind(".")
        if pos_dot == NOT_FOUND:
            return
        file_extension = file_path[pos_dot:]
        if file_extension.lower() in [".dart"]:
            try:
                view.set_status("flutter_reloading", "Reloading...")
                sublime.set_timeout_async(run_reload)
                sublime.set_timeout(lambda: view.erase_status(
                    "flutter_reloading"), 1000)
            except Exception as e:
                return sublime.error_message(
                    "Failed to trigger hot reload on save. " + getattr(e, 'message', str(e)))


class FlutterDartCodeHotReloadCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.set_status("flutter_reloading", "Reloading...")
        sublime.set_timeout_async(run_reload)
        sublime.set_timeout(lambda: self.view.erase_status(
            "flutter_reloading"), 1000)


class FlutterDartCodeHotRestartCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.set_status("flutter_restarting", "Restarting...")
        sublime.set_timeout_async(run_restart)
        sublime.set_timeout(lambda: self.view.erase_status(
            "flutter_restarting"), 1000)
