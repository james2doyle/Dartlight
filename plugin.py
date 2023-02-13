from os import system

import sublime
import sublime_plugin
import subprocess
import platform


def run_reload():
    if platform.system() == "Darwin" or platform.system() == "Linux":
        # send SIGUSR1 to trigger a hot reload and SIGUSR2 to trigger a hot restart
        subprocess.check_call(
            "kill -s USR1 \"$(pgrep -f flutter_tools.snapshot\\ run)\" &> /dev/null", shell=True)
    else:
        # TODO support Windows
        sublime.error_message(
            "Dartlight: hot reload is not supported on your platform")


class DartReloadOnSave(sublime_plugin.EventListener):
    """ A class to listen for events triggered by ST. """

    def on_post_save_async(self, view):
        """
        This is called after a view has been saved. It runs in a separate thread
        and does not block the application.
        """

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
                return sublime.error_message("Failed to trigger hot reload on save. " + getattr(e, 'message', str(e)))
