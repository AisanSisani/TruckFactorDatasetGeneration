
from github import Github
import datetime

if __name__ == '__main__':
    totalCommits = 0
    pullsCreated = 0
    pullsMerged  = 0
    pullsCommented = 0

    g = Github("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")
    repo = g.get_repo("wp-cli/wp-cli")
    devList = repo.get_contributors()
    commitList = repo.get_commits(until=datetime.datetime(2015, 8, 25))
    pullList = repo.get_pulls()


    # total commits per author
    for dev in devList:
        for commit in commitList:
            if (commit.author!=None and dev != None):
                if (commit.author.login == dev.login):
                    totalCommits+=1
        print(dev.login + "          number of commits = " + str(totalCommits))
        totalCommits = 0

    # pull requests created and merged per author
    for dev in devList:
        for pull in pullList:
        #    print(pull.created_at)
            if (pull.created_at < datetime.datetime(2015, 8, 25)):
                print("a")
                if (pull.user != None and pull.user.login == dev.login):
                    pullsCreated+=1
                if (pull.merged_by != None and pull.user.login == dev.login):
                    pullsMerged += 1
                commentlist = pull.get_comments()
                for comment in commentlist:
                    if (comment.user != None and comment.user.login == dev.login):
                        pullsCommented+=1
                        break

        print(dev.login + "          pulls created - pulls merged = " + str(pullsCreated) + " - " + str(pullsMerged))
        pullsCreated = 0
        pullsMerged = 0
        pullsCommented = 0

    # comments







