import requests
import json
import datetime
import time
from bs4 import BeautifulSoup
import re
import os.path
from os import path
import csv
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

mpl.use('agg')

token = "495312aafae6f078a049c8931b63cd6cb70a0bb6"
baseurl = "https://api.github.com/repos/"
user = ""
project = ""

# master lists
users = []
projects = []
pull_requests = []

# the repo object with various attributes, and essential functions
class Project:
    def __init__(self, name="",description="",login="", home_page="", lic="",
        proj_forks="",proj_watchers="",capture_date="", proj_stars=""):
        self.name = name
        self.description = description
        self.login = login
        self.home_page = home_page
        self.lic = lic
        self.proj_watchers = proj_watchers
        self.proj_forks = proj_forks
        self.capture_date = capture_date
        self.proj_stars = proj_stars

    def __str__(self):
        return(str(self.login) + "/" + str(self.name) + ": " + str(self.description) + " ("+str(self.proj_stars)+ ")")

    # print project details, used for writing csv records
    def get_deets(self):
        return self.name + "," + self.login + "," + str(self.description) + "," + str(self.home_page) + "," + str(self.lic) + "," + str(self.proj_watchers) + "," + str(self.proj_forks) + "," + self.capture_date + "," + str(self.proj_stars)

    # for csv header
    def get_header(self):
        return "name,login,description,home,lic,proj_watchers,proj_forks,capture_date,proj_stars"

# the PR object with various attributes, and essential functions
class Pull_Request:
    def __init__(self,title="",number="",body="", state="", created_at="",
    closed_at="",user="",number_commits="", additions="", deletions="",changed_files="",repo_name=""):
        self.title = title
        self.number = number
        self.body = body
        self.state = state
        self.created_at = created_at
        self.closed_at = closed_at
        self.user = user
        self.number_commits = number_commits
        self.additions = additions
        self.deletions = deletions
        self.repo_name = repo_name
        self.changed_files = changed_files

    def __str__(self):
        return(self.number + "," + self.title + ","  + self.body + "," + self.state + ","
        + self.created_at + "," + self.closed_at + "," + self.user + "," + self.number_commits + ","
        + self.additions + "," + self.deletions + "," + self.changed_files)

    # print pull details, used for writing csv records
    def get_deets(self):
        return str(self.number) + "," + "\"" + str(self.title) + "\"" + ","  + "\"" + str(self.body) + "\"" + "," + str(self.state) + "," + str(self.created_at) + "," + str(self.closed_at) + "," + str(self.user) + "," + str(self.number_commits) + "," + str(self.additions) + "," + str(self.deletions) + "," + str(self.changed_files) + "," + str(self.repo_name)

    # for csv header
    def get_header(self):
        return "number,title,body,state,created_at,closed_at,user,commits,additions,deletions,changed_files,repo"

# the User object with various attributes, and essential functions
class User:
    def __init__(self,pulls="",login="",has_a_twitter="",num_repos="",num_followers="",
        num_following="",num_contributions="",involved_repo=""):
        self.login = login
        self.num_pulls = pulls
        self.has_twitter = has_a_twitter
        self.num_repos = num_repos
        self.num_followers = num_followers
        self.num_following = num_following
        self.num_contributions = num_contributions
        self.involved_repo = involved_repo

    def __str__(self):
        return '%s,%s,%s,%s,%s,%s,%s,%s' % (self.login, str(self.num_pulls), str(self.has_twitter),
        str(self.num_repos), str(self.num_followers), str(self.num_following),
        str(self.num_contributions), str(self.involved_repo))

    # print user details, used for writing csv records
    def get_deets(self):
        return str(self.login) + "," + str(self.num_pulls) + "," + str(self.has_twitter) + "," + str(self.num_repos) + "," + str(self.num_followers) + "," + str(self.num_following) + "," + str(self.num_contributions) + "," + str(self.involved_repo)

    # for csv header
    def get_header(self):
        return "user,num_pulls,has_twitter,num_repos,followers,following,contributions,involved_repo"

# read a csv object from filesystem
def read_CSV(name,owner,repo):

    if name is not "pulls":
        filename = "/Users/cbc_personal/Documents/school/inf502/pa2/" + name + ".csv"
    else:
        filename = "/Users/cbc_personal/Documents/school/inf502/pa2/projects/" + owner + "-" + repo + ".csv"

    if path.exists(filename):
        with open(filename, newline='') as file:
            readCSV = csv.reader(file, delimiter=',')

            if name is "users":

                for row in readCSV:
                    login = row[0]
                    num_pulls = row[1]
                    has_twitter = row[2]
                    num_repos = row[3]
                    num_followers = row[4]
                    num_following = row[5]
                    num_contributions = row[6]
                    involved_repo = row[7]

                    new_user = User(num_pulls,login,has_twitter,num_repos,num_followers,num_following,num_contributions,involved_repo)
                    users.append(new_user)

            elif name is "projects":

                for row in readCSV:
                    if row[0] != "name":
                        #print("loading proj ")
                        name = row[0]
                        login = row[1]
                        description = row[2]
                        home_page = row[3]
                        lic = row[4]
                        proj_watchers = row[5]
                        proj_forks = row[6]
                        capture_date = row[7]
                        proj_stars = row[8]

                        new_proj = Project(name,description,login,home_page,lic,proj_forks,proj_watchers,capture_date, proj_stars)
                        projects.append(new_proj)

            elif name is "pulls":

                for row in readCSV:
                    number = row[0]
                    title = row[1]
                    body = row[2]
                    state = row[3]
                    created_at = row[4]
                    closed_at = row[5]
                    user = row[6]
                    number_commits = row[7]
                    additions = row[8]
                    deletions = row[9]
                    changed_files = row[10]
                    repo_name = row[11]

                    new_pull = Pull_Request(title,number,body,state,created_at,closed_at,
                    user,number_commits,additions,deletions,changed_files,repo_name)
                    pull_requests.append(new_pull)

# write object records to a csv filename
def to_CSV(obj,name):

    filename = "/Users/cbc_personal/Documents/school/inf502/pa2/" + name + ".csv"

    if path.exists(filename):
        with open(filename, 'a', newline='') as file:
            file.write(obj.get_deets() + "\n")
    else:
        with open(filename, 'a', newline='') as file:
            file.write(obj.get_header() + "\n")
            file.write(obj.get_deets() + "\n")

# used for scraping the attributes not provided in api
def scrape_user(user):
    user_stats = []
    result = requests.get("https://github.com/" + user + "/")
    content = result.content
    soup=BeautifulSoup(content, "html.parser")

    twitter_result = requests.get("https://twitter.com/" + user)
    if twitter_result.status_code is 200:
         has_twitter = True
    else:
         has_twitter = False
    count = 0


    # get contributions
    try:
        cont_div = soup.find_all('div', class_='js-yearly-contributions')
        cont_h2 = soup.find_all('h2', class_='f4 text-normal mb-2')[0]
        num_contributions = cont_h2.text.strip().split()[0]
    except:
        num_contributions = 0

    # get repos number
    try:
        repos_chunk = soup.find_all('a')[53]
        num_repos = repos_chunk.span.text.strip()
    except:
        num_repos = 0

    try:
        followers_chunk = soup.find_all('a')[56]
        num_followers = followers_chunk.span.text.strip()
    except:
        num_followers = 0

    try:
        following_chunk = soup.find_all('a')[57]
        num_following = following_chunk.span.text.strip()
    except:
        num_following = 0


    # load stats into list
    user_stats.append(has_twitter)
    user_stats.append(num_repos)
    user_stats.append(num_followers)
    user_stats.append(num_following)
    user_stats.append(num_contributions)

    # return our scraped stats to get_project
    return user_stats

# print out project objects
def print_projects():

    for i in projects:
        if i.name == "name":
             pass
        else:
            print(i)

# provide a summary of the repo
def repo_summary(owner,repo):
    num_users = 0
    open_pulls = 0
    closed_pulls = 0
    num_valid_twitter = 0

    print("\nSummary for the " + repo + " repo ...\n")
    print("Owner: " + owner)
    print("Repo: " + repo)

    for i in pull_requests:
        if i.state == "open":
            open_pulls = open_pulls + 1
        else:
            closed_pulls = closed_pulls + 1

    print("Open pulls: " + str(open_pulls))
    print("Closed pulls: " + str(closed_pulls))

    # num users
    for i in users:
        if i.involved_repo == repo:
            num_users = num_users + 1

    print("Num users: " + str(num_users))

    # get oldest pull
    epoch_times = []
    min_epoch = 0
    for i in pull_requests:

        if i.created_at != "created_at":
            curdate = i.created_at
            utc_time = datetime.datetime.strptime(curdate, "%Y-%m-%dT%H:%M:%SZ")
            epoch_time = (utc_time - datetime.datetime(1970, 1, 1)).total_seconds()
            epoch_times.append(epoch_time)

    min_epoch = min(epoch_times)
    print("Date of oldest pull: " + time.strftime('%m/%d/%Y %H:%M:%S',  time.gmtime(min_epoch)))

    # valid twitters
    for i in users:
        if i.involved_repo == repo:
            if i.has_twitter == "True":
                num_valid_twitter = num_valid_twitter + 1

    print("Users with valid twitter accounts: " + str(num_valid_twitter))

# primary function to fetch a repo
def fetch_project(user,repo):
    user_names = []
    date = datetime.datetime.now()
    capture_date = date.strftime("%y%m%d")
    user = owner
    project = repo
    proj_name = "null"
    proj_home = "null"
    proj_desc = "null"
    proj_url = baseurl + user + "/" + project + "?access_token=" + token

    title = ""
    number = ""
    body = ""
    state = ""
    created_at = ""
    closed_at = ""
    new_user = ""
    pull_user = ""
    pull_commits = ""
    pull_additions = ""
    pull_deletions = ""
    pull_changes = ""

    print("Checking if repo: " + repo + " is cached ...")

    # check if we already have the project cached
    for i in projects:
        if i.name == repo:
            print("\nGood news, we already have that project cached ...")
            print(i)
            return

    print("The repo is not cached ... getting it now ...")

    proj_response = requests.get(proj_url)

    # if the url was invalid, or something else like a connection issue say
    if proj_response.status_code != 200:
        print("Doesn't seem to be a valid owner/repo combination!")
        return

    proj_data = json.loads(proj_response.text)

    try:
        proj_desc = proj_data.get("description", "none")
    except:
        proj_desc = "null"

    proj_name = proj_data.get("name", "none")


    proj_home = proj_data.get("homepage", "none")
    proj_forks = proj_data.get("forks", "none")
    proj_stars = proj_data.get("stargazers_count", "none")
    proj_watchers = proj_data.get("watchers", "none")
    try:
        proj_lic = proj_data['license'].get("name", "none")
    except:
        proj_lic = "null"

    proj_login = proj_data['owner'].get("login", "none")

    pulls_url = "https://api.github.com/search/issues?q=is:pr+repo:" + owner + "/" + repo
    pulls_response = requests.get(pulls_url)
    pulls_data = json.loads(pulls_response.text)
    pulls_items = pulls_data['items']

    for pull in pulls_items:
        # status update
        print(".")

        title = pull['title']
        number = pull['number']
        body = pull['body']

        body1 = body.replace('\n', '')
        body2 = body1.replace('\r', '')
        body3 = body2.replace(',', '')
        fixed_body = body3.replace('\t', '')

        state = pull['state']
        created_at = pull['created_at']
        closed_at = pull['closed_at']
        pull_user = pull['user'].get('login',"none")
        pull_user_url = pull['pull_request'].get('url',"none")

        # sigh have to get next data from a different url
        user_pull_response = requests.get(pull_user_url)
        user_pull_response_data = json.loads(user_pull_response.text)

        pull_commits = user_pull_response_data.get('commits',"none")
        pull_additions = user_pull_response_data.get('additions',"none")
        pull_deletions = user_pull_response_data.get('deletions',"none")
        pull_changes = user_pull_response_data.get('changed_files',"none")

        user_stats = scrape_user(pull_user)
        user_contributions = user_stats.pop()
        user_following = user_stats.pop()
        user_followers = user_stats.pop()
        user_repos = user_stats.pop()

        if not isinstance(user_repos, int):
            user_repos = 1
        user_twitter = user_stats.pop()

        if pull_user not in user_names:
            new_user = User(1,pull_user,user_twitter,user_repos,user_followers,user_following,user_contributions,project)
            users.append(new_user)
            user_names.append(pull_user)
        else:
            for i in users:
                if i.login == pull_user:
                    i.num_pulls = i.num_pulls + 1

        # create the pull request object
        new_pull = Pull_Request(title,number,"\"" + fixed_body + "\"",state,created_at,closed_at,
        pull_user,pull_commits,pull_additions,pull_deletions,pull_changes,project)

        # write the object to file
        to_CSV(new_pull,"projects/" + user + "-" + project)

        # add pull request to master List
        pull_requests.append(new_pull)

    # create the project object
    proj = Project(proj_name, proj_desc, proj_login,proj_home, proj_lic,proj_forks,proj_watchers,capture_date, proj_stars)

    # write the object to file
    to_CSV(proj,"projects")

    # add this project to master list of projects
    projects.append(proj)

    # write out users to csv
    for i in users:
        to_CSV(i,"users")

# grab all pulls
def print_pulls():
    print("")
    for i in pull_requests:
        print (i)

# boxplot comparing closed and open pull requests in terms of number of commits
def cg_bpcommits():
    plt.clf()

    open_commits = []
    closed_commits = []
    data = []

    for i in pull_requests:
        if i.state != "state":
            if i.state == "closed":
                if i.number_commits != "none":
                    closed_commits.append(int(i.number_commits))
            elif i.state == "open":
                if i.number_commits != "none":
                    open_commits.append(int(i.number_commits))

    data = [closed_commits, open_commits]
    fig = plt.figure(1, figsize=(9,6))

    # Create an axes instance
    ax = fig.add_subplot(111)

    # Create the boxplot
    bp = ax.boxplot(data)

    ax.set_title('Commits')
    ax.set_xticklabels(['closed', 'open '])

    # Save the figure
    fig.savefig('bp_commits.png', bbox_inches='tight')

# boxplot comparing closed and open pull requests in terms of additions and deletions
def cg_bp_adds_dels():
    plt.clf()

    closed_adds_dels = []
    open_adds_dels = []
    data = []

    for i in pull_requests:
        if i.additions != "additions":
            if i.state == "closed":
                if i.number_commits != "none":
                    closed_adds_dels.append(int(i.additions))
                    closed_adds_dels.append(int(i.deletions))
            elif i.state == "open":
                if i.number_commits != "none":
                    open_adds_dels.append(int(i.additions))
                    open_adds_dels.append(int(i.deletions))

    data = [closed_adds_dels, open_adds_dels]
    fig = plt.figure(1, figsize=(9,6))

    # Create an axes instance
    ax = fig.add_subplot(111)

    # Create the boxplot
    bp = ax.boxplot(data)

    ax.set_title('Adds and Deletions')
    ax.set_xticklabels(['closed', 'open '])

    # Save the figure
    fig.savefig('bp_adds_dels.png', bbox_inches='tight')

# boxplot comparing the number of changed files grouped by the author association
def cg_changed_files():
    # TODO

    data = []
    user = []
    users = []

# scatterplot: additions x deletions
def cg_sp_adds_dells():
    data = []
    adds = []
    dels = []

    plt.clf()

    for i in pull_requests:
        if i.additions != "additions":
            if i.additions != "none":
                adds.append(int(i.additions))
            if i.deletions != "none":
                dels.append(int(i.deletions))

    plt.scatter(adds, dels, alpha=0.5)
    plt.title('Adds x Dels')
    plt.xlabel('Adds')
    plt.ylabel('Dels')

    plt.savefig('sp_adds_dels.png', bbox_inches='tight')

# line graph showing the total number of pull requests per day
#def cg_ap_lg_pr():
    # TODO


if __name__ == '__main__':
    # create directory projects if doesn't exist
    if not os.path.exists("projects"):
        os.makedirs("projects")

    while True:

        print("")
        print("Here you can investigate some github repos!")
        print("-- Enter the number corresponding to the option --")
        print("1 - Request a repo to be collected ")
        print("2 - List all repos in our database")
        print("3 - List all pull requests from a repo")
        print("4 - Provide summary of a repo")
        print("5 - Create various graphics illustrating repo statistics")
        print("6 - Create various graphics considering all pull requests from all repos")
        print("7 - Exit")

        cmd = int(input("Enter option: "))

        if cmd is 1:
            owner = input("Provide the owner: ")
            repo = input("Provide the repo: ")
            print("Stand by, it can take a bit of time ...")
            read_CSV("projects","null","null")
            fetch_project(owner,repo)
            print("All set ...")

        elif cmd is 2:
            projects = []
            read_CSV("projects","null","null")
            print("Repos in my db ...\n")
            print_projects()

        elif cmd is 3:
            print("Repos in my db ...")
            projects = []
            read_CSV("projects","null","null")
            print_projects()
            repo = input("Provide the repo: ")

            check = 0
            for i in projects:
                if i.name == repo:
                    check = 1
                    owner = i.login
                    repo = i.name

            if check is 1:
                pull_requests = []
                read_CSV("pulls",owner,repo)
                print_pulls()
            else:
                print("Invalid repo specified!")


        elif cmd is 4:
            print("Repos in my db ...")
            projects = []
            pull_requests = []
            users = []
            read_CSV("projects","null","null")
            print_projects()
            repo = input("Provide the repo please: ")

            check = 0
            for i in projects:
                if i.name == repo:
                    check = 1
                    owner = i.login
                    repo = i.name
            if check is 1:
                read_CSV("pulls",owner,repo)
                read_CSV("users",owner,repo)
                repo_summary(owner,repo)
            else:
                print("Invalid repo specified!")

        elif cmd is 5:
            print("Repos in my db ...")
            projects = []
            read_CSV("projects","null","null")
            print_projects()
            repo = input("Provide the repo: ")

            check = 0
            for i in projects:
                if i.name == repo:
                    check = 1
                    owner = i.login
                    repo = i.name

            if check is 1:
                pull_requests = []
                read_CSV("pulls",owner,repo)
                projects = []
                read_CSV("projects","null","null")
                cg_bpcommits()
                cg_bp_adds_dels()
                ##cg_changed_files()
                cg_sp_adds_dells()
                ##cg_hist_commits
                #cg_ap_lg_pr()
            else:
                print("Invalid repo specified!")
                
            print("All set, you will find the graphics stored as png files next to pa2.py")

        elif cmd is 6:
            print("Sorry amigo, this is not yet functional!")

        elif cmd is 7:
            print("Ok, suit your self!")
            exit()
