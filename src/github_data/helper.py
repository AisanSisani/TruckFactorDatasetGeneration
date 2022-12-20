import numpy as np
INPUT_FOLDER_PATH = '../../files/repos_incomplete/'

def get_developer_commits(repo_name):
    dev_list = []
    commit_list = []
    with open(INPUT_FOLDER_PATH + repo_name + '/commits.txt', encoding='latin-1') as file:
        for line in file:
            stripped = line.strip()
            splited = stripped.split()
            commit = int(splited[0])
            commit_list.append(commit)
            dev = ''.join([i for i in stripped if not i.isdigit()]).strip()
            dev_list.append(dev)
    return dev_list, commit_list


def get_addition_deletion(repo_name):
    add_list = []
    del_list = []
    with open(INPUT_FOLDER_PATH + repo_name + '/aads.txt', encoding='latin-1') as file:
        for line in file:
            if line.isspace():
                add_list.append(0)
                del_list.append(0)
                continue
            s = line.strip().split()
            addition = int(s[0])
            deletion = int(s[1])
            add_list.append(addition)
            del_list.append(deletion)
    return add_list, del_list


def get_days_since_last_commit(repo_name):
    days_list = []
    with open(INPUT_FOLDER_PATH + repo_name + '/daysSinceLast.txt', encoding='latin-1') as file:
        for line in file:
            if line.isspace():
                days_list.append(-1)
                continue
            days_list.append(int(line))
    #print(days_list)
    #return days_list
    avg_list = [x for x in days_list if x != -1]
    avg = round(np.mean(avg_list))
    print(avg)
    result = [x if x!=-1 else avg for x in days_list]
    print(result)
    return result


def get_days_first_to_last_commit(repo_name):
    days_list = []
    with open(INPUT_FOLDER_PATH + repo_name + '/daysBetweenFirstLast.txt', encoding='latin-1') as file:
        for line in file:
            if line.isspace():
                days_list.append(0)
                continue
            days_list.append(int(line))
    return days_list

