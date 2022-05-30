import json
import repo_data
import pandas as pd


class GithubData:
    def __int__(self, data, access_token):
        self.df = None
        self.data = data
        self.access_token = access_token

    def produce_df(self):
        df = pd.DataFrame()

        for repo in self.data['repositories']:
            repo_url = repo['repo_url']
            repo_authors = repo['authors']
            repo_df = repo_data.RepoData(repo_url, self.access_token)
            repo_df['Author'] = [0] * repo_df.shape[0]
            for author in repo_authors:
                name = author['username']
                repo_df.loc[repo_df['dev'] == name, 'Author'] = 1

            df.append(repo_df)

        return

    def get_df(self):
        if self.df is None:
            self.produce_df()
        return self.df

def main():
    # get the list of list of repos
    # get the list of authors for each repo

    repo_detail_file = open('repo_detail.json')
    data = json.load(repo_detail_file)

    # TODO print the error that the keys.json should be generated first
    keys_file = open('keys.json')
    access_token = json.load(keys_file)['access_token']

    gd = GithubData(data, access_token)
    df = gd.get_df()

    # TODO change the path to a convention
    df.to_csv(f'../output/github.csv')
    print("The csv file has been created successfully in the output/")


if __name__ == '__main__':
    main()
