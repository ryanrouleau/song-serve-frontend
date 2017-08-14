#!/usr/bin/env python3

import sys, os
import threading, subprocess

class NodeServerThread(threading.Thread):
    def __init(self):
        self.stdout = None
        self.stderr = None
        threading.Thread.__init__(self)
        self.clientId = ''
        self.clientSecret = ''
        print(self.clientId)
        self.getSpotifyCredentials()

    def run(self):
        # change wd to song-serve directory
        self.getSpotifyCredentials()
        os.chdir('../../song-serve')
        self.p = subprocess.Popen(['node', 'app.js', self.clientId, self.clientSecret, '--verbose'], shell=False)
        self.stdout, self.stderr = self.p.communicate()

    def exitServer(self):
        self.p.kill()
        self.exit()

    def getSpotifyCredentials(self):
        # read spotify api client id and client secret from file and store
        try:
            with open('spotify-credentials.txt', 'r') as f:
                self.clientId = f.readline().rstrip('\n')
                self.clientSecret = f.readline().rstrip('\n')
        except:
            print('Spotify API credentials file does not exist.')
            print('Create spotify-credentials.txt w/ first line being client id and second line being client secret.')
            sys.exit(1)
