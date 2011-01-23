"""
tsol.py - Phenny M1 timetable module
Copyright 2011, Andrew Watson
Licensed under whatever

http://inamidst.com/phenny/
"""
from BeautifulSoup import BeautifulSoup
from urllib import urlencode
import urllib, re

def tsol(phenny, input):
    """.tsol destination - Shows next timetables to destination from epfl.
    .tsol from source to destination takes any two stops"""
    destinations = {'L':'Lausanne Flon', 'R':'Renens VD'}
    directions = {'L':'A', 'R':'R'}
    q = input.group(2)
    dest = ''
    if not q:
        dest = 'both'
        q = ''
    else:
        q = q[:]


    flon= re.compile('lausanne|flon')
    renens = re.compile('renens')
    if flon.search(q):
        dest = 'L'
    elif renens.search(q):
        dest = 'R'
    else:
        dest = 'none'

    if re.compile('more').search(q):
        more = True
    else:
        more = False

    if dest == 'none' or dest == 'both':
        phenny.say(
                "Please specify your direction (.tsol flon or .tsol renens)")
        return


    base_url = 'http://www.t-l.ch/htr.php?'
    payload = dict(ligne='70',
                    sens=directions[dest],
                    arret='EPFL'+'_'+dest)
    socket = urllib.urlopen( base_url + urlencode(payload))
    content = socket.read()
    socket.close()
    
    soup = BeautifulSoup(content)

    next_minutes = soup.findAll('span', id='e_minutes')
    next_hours = soup.findAll('span', id='e_heures')
    stop_name = soup.findAll('span', id='e_nom_arret')
    destination = destinations[dest]

    mins = "Next departure from " + stop_name[0].getText() + \
    " to " + destination + " in "
    for i in range(len(next_minutes)):
        mins = mins + next_minutes[i].getText()
        if(i < len(next_minutes)-1):
            mins = mins + " then "
        else:
            mins = mins + " "
    mins = mins + "minutes."

    phenny.say(mins)

    if(more == True):
        hours = "Following departures at "
        for i in range(len(next_hours)):
            hours = hours + next_hours[i].getText()
            if(i < len(next_hours)-2):
                hours = hours + ", "
            elif(i == len(next_hours)-2):
                hours = hours + " and "
            else:
                hours = hours + " "
        hours = hours + "hours."

        phenny.say(hours)

tsol.commands = ['tsol']
tsol.priority = 'medium'
tsol.example = '.tsol renens or .tsol from epfl to flon'

def test(phenny, input):
    q = input.group(2)
    q = q[:]
    flon= re.compile('lausanne|flon')
    renens = re.compile('renens')
    if flon.search(q):
        phenny.say("We're going to Flon!!")
    elif renens.search(q):
        phenny.say("Going to Renens VD")
test.commands=['tt']

def advertise(phenny, input):
    phenny.say("Hey " + input.nick +
    ", I know the timetables to the m1! ask me with .tsol")
advertise.rule = r'.*m1.*'
advertise.priority = 'high'
advertise.thread = False

