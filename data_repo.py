from github import Github
import datetime
import pandas as pd
import time
import os

if __name__ == '__main__':
    print(os.getcwd())
    totalCommits = 0
    pullsCreated = 0
    pullsMerged = 0
    pullsCommented = 0

    # TODO change the location to a key file and add it to the .gitignore
    g = Github("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")

    # TODO change it with a general solution
    repo = g.get_repo("wp-cli/wp-cli")
    devList = repo.get_contributors()
    commitList = repo.get_commits(until=datetime.datetime(2015, 8, 25))
    pullOpenList = repo.get_pulls(state='open')
    pullClosedList = repo.get_pulls(state='closed')

    # creating developer commit dictionary
    dev_list = [dev.login for dev in devList]
    n = len(dev_list)

    '''
    dev_commit_dict = dict(zip(dev_list, [0]*len(dev_list)))
    start_time = time.time()
    for commit in commitList:
            if (commit.author!=None):
                dev_commit_dict[commit.author.login] += 1
    end_time = time.time()
    print("Execution time is %s seconds" % (end_time-start_time))
    '''

    '''
    start_time = time.time()
    for dev in devList:
        for commit in commitList:
            if (commit.author!=None and dev != None):
                if (commit.author.login == dev.login):
                    totalCommits+=1
        #print(dev.login + "          number of commits = " + str(totalCommits))
        totalCommits = 0
    end_time = time.time()
    print("Execution time is %s seconds" % (end_time-start_time))
    '''

    df = pd.DataFrame()
    df['dev'] = dev_list

    # Commits
    df['commit'] = [0] * n
    df['addition'] = [0] * n
    df['deletion'] = [0] * n

    start_time = time.time()
    for commit in commitList:
        if commit.author is not None:
            name = commit.author.login
            # df[df['dev'] == name]['commit'] += 1 # gives warning
            df.loc[df['dev'] == name, 'commit'] += 1
            df.loc[df['dev'] == name, 'addition'] += commit.stats.additions
            df.loc[df['dev'] == name, 'deletion'] += commit.stats.deletions
    end_time = time.time()

    print("Commits, Addition, and Deletion done in %s seconds" % (end_time - start_time))
    df.to_csv('output/o1_commit.csv')

    # Open Pull Requests
    start_time = time.time()
    df['pull_open'] = [0] * n
    for pull in pullOpenList:
        if pull.created_at < datetime.datetime(2015, 8, 25):
            if pull.user is not None:
                name = pull.user.login
                df.loc[df['dev'] == name, 'pull_open'] += 1
    end_time = time.time()
    print("Open pull requests in %s seconds" % (end_time - start_time))
    df.to_csv('output/o2_open.csv')

    # Closed Pull Requests
    start_time = time.time()
    df['pull_merged'] = [0] * n
    for pull in pullClosedList:
        if pull.created_at < datetime.datetime(2015, 8, 25):
            if pull.merged_by is not None:
                name = pull.merged_by.login
                df.loc[df['dev'] == name, 'pull_merged'] += 1
    end_time = time.time()
    print("Merged pull requests in %s seconds" % (end_time - start_time))
    df.to_csv('output/o3_merged.csv')

    # Users Commented on the pull requests
    start_time = time.time()
    df['pull_comment'] = [0] * n
    pullList = repo.get_pulls(state='all')
    for pull in pullList:
        commentList = pull.get_comments()
        for comment in commentList:
            if comment.user is not None:
                name = comment.user.login
                df.loc[df['dev'] == name, 'pull_comment'] += 1
    end_time = time.time()
    print("Commented pull requested in %d seconds" % (end_time - start_time))
    df.to_csv('output/o4_comment.csv')
