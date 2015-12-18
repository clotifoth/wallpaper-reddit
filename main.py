import os
import sys

import config
import connection
import download
import reddit
import wallpaper


def run():
    try:
        config.create_config()
        # blacklist the current wallpaper if requested
        if config.blacklistcurrent:
            reddit.blacklist_current()
        # check if the program is run in a special case (save or startup)
        if config.save:
            wallpaper.save_wallpaper()
            sys.exit(0)
        if config.startup:
            connection.wait_for_connection(config.startupattempts, config.startupinterval)
        # make sure you're actually connected to reddit
        if not connection.connected("http://www.reddit.com"):
            print("ERROR: You do not appear to be connected to Reddit. Exiting")
            sys.exit(1)
        # download the image
        links = reddit.get_links()
        titles = links[1]
        valid = reddit.choose_valid(links[0])
        valid_url = valid[0]
        title_index = valid[1]
        title = titles[title_index]
        download.download_image(valid_url)
        download.save_info(valid_url, title)
        wallpaper.set_wallpaper()
        external_script()
    except KeyboardInterrupt:
        sys.exit(1)


# in - string - messages to print
# takes a string and will print it as output if verbose
def log(info):
    if config.verbose:
        print(info)


# creates and runs the ~/.wallpaper/external.sh script
def external_script():
    if config.opsys == 'Linux':
        if not os.path.isfile(config.walldir + '/external.sh'):
            with open(config.walldir + '/external.sh', 'w') as external:
                external.write(
                    '# ! /bin/bash\n\n# You can enter custom commands here that will execute after the main program is finished')
            os.system('chmod +x ' + config.walldir + '/external.sh')
        os.system('bash ' + config.walldir + '/external.sh')
