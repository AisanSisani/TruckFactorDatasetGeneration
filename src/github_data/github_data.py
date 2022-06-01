import json
import pandas as pd

import repo_data


class GithubData:
    def __init__(self, data, access_token):
        self.df = None
        self.data = data
        self.access_token = access_token

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
            repo_d = repo_data.RepoData(repo_url, self.access_token)
            repo_df = repo_d.get_normalized_df(verbose = True)
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

            # TODO: deprecated  -replace with pandas concat
            df.append(repo_df)

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

    gd = GithubData(data, access_token)
    df = gd.get_df(verbose=True)
    print("\nData has been gathered.")

    # TODO change the path to a convention
    df.to_csv(f'../../output/github.csv')
    print("The csv file has been created successfully as ../../output/github.csv")


if __name__ == '__main__':
    main()
