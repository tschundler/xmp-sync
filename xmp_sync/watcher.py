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
        print(b'sf ' + src_file)

        try:
        #from ipdb import launch_ipdb_on_exception
        #with launch_ipdb_on_exception():

            if src_file in ignore_list:
                if ignore_list[src_file] + 5.0 > time.time():
                    print(b'Already Updated: ' + src_file)  
                    return

            print(glob.glob(src_file.replace(b'.xmp', b'*')))
            for f in glob.iglob(src_file.replace(b'.xmp', b'*')):
                if not f.endswith(b'xmp') and not f.endswith(b'XMP'):
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
                print(b'Updated in AfterShot: ' + raw_file)
            elif src_file == lr:
                # triggered by Lighroom
                ignore_list[bib] = time.time()
                lr2bib_files(lr, bib, raw_file)
                ignore_list[bib] = time.time()
                print(b'Updated in LR: ' + raw_file)
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

