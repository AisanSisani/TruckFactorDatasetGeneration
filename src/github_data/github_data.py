import json
import pandas as pd

import repo_data
from github import Github

from colorama import Fore, Style

import traceback


class GithubData:
    def __init__(self, data, github_con):
        self.df = None
        self.data = data
        self.github_con = github_con

    def produce_df(self, type_norm, verbose=False):
        try:
            # df = pd.read_csv(f'../../files/github.csv', index_col=False)
            df = pd.DataFrame()
        except:
            df = pd.DataFrame()
            print("> No dataframe was found at ../../files/github.csv")
        else:
            print("> Dataframe loaded from ../../files/github.csv")

        repos_size = len(self.data['repositories'])
        for i in range(repos_size):
            repo = self.data['repositories'][i]
            try:
                repo_url = repo['repo_url']
                if verbose:
                    print(f"> {i + 1}/{repos_size}: {repo_url}")

                # TODO
                '''
                if repo['status'] == 1:
                    print(f"> {repo_url} has been gathered before.")
                    continue
                '''

                if repo['status'] == -1:
                    print(f"> {repo_url} is requested to be skipped.")
                    continue

                if verbose:
                    print(f"> The features for {repo_url} is being gathered...")
                repo_d = repo_data.RepoData(repo_url, self.github_con)
                repo_df = repo_d.get_df(verbose=True)
                repo_df_norm = repo_d.get_normalized_df(type_norm, verbose=True)
                if verbose:
                    print(f"> The features for {repo_url} have been gathered.")

                repo_authors = repo['authors']
                repo_df_norm['author'] = [0] * repo_df_norm.shape[0]
                for author in repo_authors:
                    name = author['username']
                    repo_df_norm.loc[repo_df_norm['developer'] == name, 'author'] = 1

                repo_df['author'] = [0] * repo_df.shape[0]
                for author in repo_authors:
                    name = author['username']
                    repo_df.loc[repo_df['developer'] == name, 'author'] = 1

                # deprecated  -replace with pandas concat
                # df = df.append(repo_df_norm)
                df = pd.concat([df, repo_df_norm], ignore_index=True)


                repo_df_norm.to_csv(f'../../files/repos_complete/{repo_d.repo_name}_{type_norm}.csv', index=False)
                repo_df.to_csv(f'../../files/repos_notnorm/{repo_d.repo_name}.csv', index=False)
                if verbose:
                    print(f"> The dataframe for repository {repo_url} is saved at ../../files/repos/")

            except Exception:
                print(Fore.RED + f"> Error happened while gathering features for repo {repo_url}")
                print(Style.RESET_ALL, end='')
                traceback.print_exc()
            else:
                df.to_csv(f'../../files/github.csv', index=False)
                if verbose:
                    print(f"> The csv file has been updated successfully: ../../files/github.csv")
                self.data['repositories'][i]['status'] = 1
                with open('data/repo_detail.json', "w") as outfile:
                    json.dump(self.data, outfile, indent=4)
                    print("Repo detail file updated with new status")

        self.df = df

    def get_df(self, type_norm,verbose=False):
        if self.df is None:
            if verbose:
                print("> Creating github dataframe.")
            self.produce_df(type_norm, verbose)
        return self.df


def main():
    print(f"The files csv file will be saved as ../../files/github.csv")

    with open('data/repo_detail.json', "r") as repo_detail_file:
        data = json.load(repo_detail_file)
        print("Repo details file loaded.")
    print("Repo Details:")
    print(data)

    # TODO print the error that the keys.json should be generated first
    keys_file = open('data/keys.json')
    access_token = json.load(keys_file)['access_token']
    print("Access token loaded.")

    github_con = Github(access_token)
    print("Github connection created.")

    gd = GithubData(data, github_con)
    type_norm = 'ratio'
    df = gd.get_df(type_norm, verbose=True)

    # TODO change the path to a convention
    df.to_csv(f'../../files/github.csv', index=False)
    print("../../files/github.csv created.")

    with open('data/repo_detail.json', "w") as outfile:
        json.dump(gd.data, outfile, indent=4)
        print("Repo detail file updated with status")


if __name__ == '__main__':
    main()
