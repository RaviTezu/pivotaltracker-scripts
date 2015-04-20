#!/usr/bin/python
from ConfigParser import SafeConfigParser
from collections import defaultdict
from datetime import date
import requests

CONFIG_FILE = 'Config.ini'
PIVOTAL_URL = 'https://www.pivotaltracker.com/services/v5/projects/{0}/stories?updated_after={1}'

def readConfigFile(conf_file, user='default'):
    """ Read the config file for token and project IDs and returns them as a tuple """
    parser = SafeConfigParser()
    parser.read(conf_file)
    token  = parser.get(user, 'TOKEN')
    project_ids = parser.get(user, 'PROJECT_IDS')
    return (token, project_ids)

def hackPivotal(creds_tuple):
    """ Take token and projet ids and returns the updated stories in"""
    #today_time = date.today().isoformat()+'T12:00:00Z'
    today_time = '2015-04-01'+'T12:00:00Z'
    result = requests.get(PIVOTAL_URL.format(creds_tuple[1],today_time), headers={"X-TrackerToken":creds_tuple[0]})
    return result.json()

def displayStories(stories_received):
    """ Takes a list of dictionaries and displays them """
    res  = defaultdict(list)
    for story in stories_received:
        points = story.get('estimate',0)
        if points:
            res[story['story_type']].append(story['name']+" "+"["+story['current_state'].upper() +"]" +" ["+str(points)+"]")
        else:
            res[story['story_type']].append(story['name']+" "+"["+story['current_state'].upper() +"]")
    for k,v in res.iteritems():
        print k.title()+": "+str(len(v))
        for t in v:
            print t
        print ""
    
def main():
    """ main function, executed when you run this file """
    creds   = readConfigFile(CONFIG_FILE)   
    stories = hackPivotal(creds)
    displayStories(stories)

if __name__ == '__main__':
    main()