#Create a script that checks all the contributors of a given GitHub project and downloads their avatars into a corresponding folder.
#
#For example:
#
#$> python3 download_contributors_avatars.py -u kennethreitz -p requests
#…
#$> tree
#.
#├── kennethreitz
#│   └── requests
#│       ├── acdha.jpg
#│       ├── bbamsch.jpg
#│       ├── BraulioVM.jpg
#│       ├── ContinuousFunction.png
#│       ├── daftshady.jpg
#│       ├── davidfischer.jpg
#│       ├── DemetriosBairaktaris.png
#│       ├── dpursehouse.jpg
#│       ├── gazpachoking.jpg
#│       ├── idan.jpg
#│       ├── jasongrout.jpg
#│       ├── jdufresne.jpg
#│       ├── jerem.jpg
#│       ├── jgorset.jpg
#│       ├── joequery.jpg
#│       ├── kenneth-reitz.jpg
#│       ├── kevinburke.jpg
#│       ├── klimenko.jpg
#│       ├── kmadac.png
#│       ├── Lukasa.jpg
#│       ├── mgiuca.jpg
#│       ├── mjpieters.jpg
#│       ├── monkeython.jpg
#│       ├── mrtazz.jpg
#│       ├── nateprewitt.jpg
#│       ├── riyadparvez.jpg
#│       ├── schlamar.jpg
#│       ├── sigmavirus24.png
#│       ├── slingamn.jpg
#│       └── t-8ch.png
#└── download_contributors_avatars.py
#
#The script has to create {username}/{project} folders and download the avatar picture files with names that match contributor’s login.
#
#Please check function os.makedirs(…) its parameter exist_ok.
#https://docs.python.org/3/library/os.html#os.makedirs
#
#For file downloads with Python requests, check the following:
#http://docs.python-requests.org/en/master/user/quickstart/#raw-response-content
#
#You need to check the response headers to figure out the picture format (JPEG or PNG).
#
#You may also take a look at the pathlib module to help with file and directory path creation.
#https://realpython.com/python-pathlib/
#
#You will still need to use argparse for the script parameters (similar to the previous task).
#
#Once implemented, please check that your script works correctly on some popular GitHub repositories.

#constants and default params
BASE_URL = 'https://api.github.com/repos/{}/{}/contributors'

####################################################################
#check out download_contributors_avatars.py for solution
