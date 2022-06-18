import datetime
import pandas as pd
import time
import tqdm
import helper

FINAL_DATE = datetime.datetime(2015, 8, 25)


class RepoData:
    def __init__(self, repo_url, github_con):
        self.repo_url = repo_url
        repo_url_s = repo_url.split("/")
        self.repo_name = f'{repo_url_s[0]}_{repo_url_s[1]}'
        self.github_con = github_con
        self.df = None
        self.normalized_df = None

    def get_normalized_df(self, verbose=False):
        if self.normalized_df is None:
            self.produce_normalized_df(verbose)
        return self.normalized_df

    def get_df(self, verbose=False):
        if self.df is None:
            self.produce_df(verbose)
        return self.df

    def produce_normalized_df(self, verbose=False):
        if self.df is None:
            self.produce_df(verbose)
        df = self.df
        df1 = df.loc[:, (df.columns != 'developer') & (df.columns != 'repo')]

        normalized_df = (df1 - df1.mean()) / df1.std()
        df.loc[:, (df.columns != 'developer') & (df.columns != 'repo')] = normalized_df
        self.normalized_df = df


    def produce_df(self, verbose=False):
        github_connection = self.github_con

        repo = github_connection.get_repo(self.repo_url)
        repo_name = self.repo_name

        ''' can be replace with *** : START'''

        dev_list, commit_list = helper.get_developer_commits(repo_name)
        pullList = repo.get_pulls(state='all')
        pullClosedList = repo.get_pulls(state='closed')

        n = len(dev_list)

        if verbose:
            print(f">> {self.repo_url}...")
            print(f">> Number of developers: {n}")

        df = pd.DataFrame()
        df['repo'] = [self.repo_url] * n
        df['developer'] = dev_list

        # Commits
        df['commit'] = commit_list
        add_del = helper.get_addition_deletion(repo_name)
        df['addition'] = add_del[0]
        df['deletion'] = add_del[1]
        df['days_since_last_commit'] = helper.get_days_since_last_commit(repo_name)
        df['days_first_to_last_commit'] = helper.get_days_first_to_last_commit(repo_name)



        ''' can be replace with *** : END'''

        # Open Pull Requests
        start_time = time.time()
        df['pull_open'] = [0] * n
        for i in tqdm.tqdm(range(pullList.totalCount), desc="Open Pull"):
            pull = pullList[i]
            if pull.created_at < FINAL_DATE:
                if pull.user is not None:
                    name = pull.user.login
                    df.loc[df['developer'] == name, 'pull_open'] += 1
        end_time = time.time()
        if verbose:
            print(">> Open pull requests in %s seconds" % (end_time - start_time))
        # df.to_csv('files/o2_open.csv')

        # Closed Pull Requests
        start_time = time.time()
        df['pull_merged'] = [0] * n

        for i in tqdm.tqdm(range(pullClosedList.totalCount), desc="Merged Pull"):
            pull = pullClosedList[i]
            if pull.created_at < FINAL_DATE:
                if pull.merged_by is not None:
                    name = pull.merged_by.login
                    df.loc[df['developer'] == name, 'pull_merged'] += 1
        end_time = time.time()
        if verbose:
            print(">> Merged pull requests in %s seconds" % (end_time - start_time))
        # df.to_csv('files/o3_merged.csv')

        # Users Commented on the pull requests
        # start_time = time.time()
        # df['pull_comment'] = [0] * n
        # for i in tqdm.tqdm(range(pullList.totalCount), desc="Pull Comment"):
        #     pull = pullList[i]
        #     if pull.created_at < FINAL_DATE:
        #         commentList = pull.get_comments()
        #         for comment in commentList:
        #             if comment.user is not None:
        #                 name = comment.user.login
        #                 df.loc[df['developer'] == name, 'pull_comment'] += 1
        # end_time = time.time()
        # if verbose:
        #     print("Commented pull requested in %d seconds" % (end_time - start_time))
        # df.to_csv('files/o4_comment.csv')

        self.df = df


def main():
    repo_url = input("Enter the repo url: ")
    access_token = input("Enter the access token: ")
    df = RepoData(repo_url, access_token)


if __name__ == "__main__":
    main()


'''
devList = repo.get_contributors()
commitList = repo.get_commits(until=FINAL_DATE)
pullList = repo.get_pulls(state='all')
pullClosedList = repo.get_pulls(state='closed')

# creating developer commit dictionary
dev_list = [dev.login for dev in devList]
n = len(dev_list)

if verbose:
    print(f">> {self.repo_url}...")
    print(f">> Number of developers: {n}")

df = pd.DataFrame()
df['repo'] = [self.repo_url] * n
df['developer'] = dev_list

# Commits
df['commit'] = [0] * n
df['addition'] = [0] * n
df['deletion'] = [0] * n
df['days_since_last_commit'] = [0] * n
df['days_first_to_last_commit'] = [0] * n
df['last_day'] = [0] * n

start_time = time.time()
commit_list_size = commitList.totalCount
i = 0
for i in tqdm.tqdm(range(commit_list_size), desc="Commit"):
    commit = commitList[i]
    if commit.author is not None:
        name = commit.author.login
        df.loc[df['developer'] == name, 'commit'] += 1
        df.loc[df['developer'] == name, 'addition'] += commit.stats.additions
        df.loc[df['developer'] == name, 'deletion'] += commit.stats.deletions
        if (commit.get_statuses().totalCount > 0):
            if (df.loc[df['developer'] == name, 'last_day'].any() == 0):
                df.loc[df['developer'] == name, 'last_day'] = commit.get_statuses()[0].created_at
                df.loc[df['developer'] == name, 'days_since_last_commit'] = (FINAL_DATE\
                                                                            - commit.get_statuses()[0].created_at).days

            elements = str(df.loc[df['developer'] == name, 'last_day']).split()
            last_date = datetime.datetime.strptime(elements[1].strip(), '%Y-%m-%d')
            df.loc[df['developer'] == name, 'days_first_to_last_commit'] = (last_date\
                                                                           - commit.get_statuses()[0].created_at).days
df = df.drop(columns='last_day')
end_time = time.time()

if verbose:
    print(">> Commits done in %s seconds" % (end_time - start_time))
# df.to_csv('files/o1_commit.csv')
'''

