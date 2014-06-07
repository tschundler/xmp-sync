import sys
import logging
import glob
import time
from .common import *
from .bib2lr import bib2lr_files
from .lr2bib import lr2bib_files
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import PatternMatchingEventHandler

ignore_list = {}

class UpdateWatcher(PatternMatchingEventHandler):

    """A simple trick that does only logs events."""

    def on_any_event(self, event):
        src_file = event.src_path
        try:
            src_file = src_file.decode()
        except AttributeError:
            pass
        print('sf ', src_file)

        try:
        #from ipdb import launch_ipdb_on_exception
        #with launch_ipdb_on_exception():

            if src_file in ignore_list:
                if ignore_list[src_file] + 5.0 > time.time():
                    print('Already Updated: ', src_file)  
                    return

            print(glob.glob(src_file.replace('.xmp', '*')))
            for f in glob.iglob(src_file.replace('.xmp', '*')):
                if not f.endswith('xmp') and not f.endswith('XMP'):
                    raw_file = f
                    break
            else:
                return

            bib, lr = xmp_filenames(raw_file)

            if src_file == bib:
                # triggered by AfterShot
                ignore_list[lr] = time.time()
                bib2lr_files(bib, lr, raw_file)
                ignore_list[lr] = time.time()
                print('Updated in AfterShot: ' + raw_file)
            elif src_file == lr:
                # triggered by Lighroom
                ignore_list[bib] = time.time()
                lr2bib_files(lr, bib, raw_file)
                ignore_list[bib] = time.time()
                print('Updated in LR: ' + raw_file)
        except FileNotFoundError:
            pass
        except:
            import traceback
            traceback.print_exc()

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    print("Watching directory for changes: " + path)

    event_handler = UpdateWatcher(patterns=['*.xmp'], ignore_patterns=['.*'])
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        observer.join()
    except KeyboardInterrupt:
        observer.stop()
        observer.join()

if __name__  == '__main__':
    main()

