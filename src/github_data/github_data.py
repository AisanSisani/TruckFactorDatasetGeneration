import json
import pandas as pd

import repo_data
from github import Github


class GithubData:
    def __init__(self, data, github_con):
        self.df = None
        self.data = data
        self.github_con = github_con

    def produce_df(self, verbose=False):
        df = pd.DataFrame()

        repos_size = len(self.data['repositories'])
        i = 1
        for repo in self.data['repositories']:
            repo_url = repo['repo_url']
            if verbose:
                print(f"Accessing {i}/{repos_size}: {repo_url}")
                i = i + 1

            if verbose:
                print(f"The features for {repo_url} is being gathered...")
            repo_d = repo_data.RepoData(repo_url, self.github_con)
            repo_df = repo_d.get_normalized_df(verbose=True)
            if verbose:
                print(f"The features for {repo_url} has been gathered.")
                print("The data frame:")
                print(repo_df.head())

            repo_authors = repo['authors']
            if verbose:
                print(f"Number of Authors: {len(repo_authors)} for {repo_url}")

            repo_df['Author'] = [0] * repo_df.shape[0]
            for author in repo_authors:
                name = author['username']
                if verbose:
                    print(name)
                repo_df.loc[repo_df['dev'] == name, 'Author'] = 1

            print("Repo df:")
            print(repo_df.head())
            # TODO: deprecated  -replace with pandas concat
            df = df.append(repo_df)
            df.to_csv(f'../../output/github_{repo_url.split("/")[1]} .csv')
            print(f"\nThe csv file has been created successfully as ../../output/github{repo_url}.csv")

        self.df = df

    def get_df(self, verbose=False):
        if self.df is None:
            self.produce_df(verbose)
        return self.df


def main():
    # get the list of repos
    # get the list of authors for each repo
    df = pd.DataFrame()
    df.to_csv(f'../../output/github.csv')
    print(f"The output csv file will be saved as ../../output/github.csv")

    repo_detail_file = open('data/repo_detail.json')
    data = json.load(repo_detail_file)
    print("\nRepo Details:")
    print(data)

    # TODO print the error that the keys.json should be generated first
    keys_file = open('data/keys.json')
    access_token = json.load(keys_file)['access_token']
    print("\nAccess Token Gained.")

    github_con = Github(access_token)
    print("\nGithub connection created.")

    gd = GithubData(data, github_con)
    df = gd.get_df(verbose=True)
    print("\nData has been gathered.")

    # TODO change the path to a convention
    df.to_csv(f'../../output/github.csv')
    print("\nThe csv file has been created successfully as ../../output/github.csv")


if __name__ == '__main__':
    main()
