import numpy as np
INPUT_FOLDER_PATH = '../../files/repos_incomplete/'

def get_developer_commits(repo_name):
    dev_list = []
    commit_list = []
    with open(INPUT_FOLDER_PATH + repo_name + '/commits.txt', encoding='utf-8') as file:
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
    with open(INPUT_FOLDER_PATH + repo_name + '/aads.txt', encoding='utf-8') as file:
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
    with open(INPUT_FOLDER_PATH + repo_name + '/daysSinceLast.txt', encoding='utf-8') as file:
        for line in file:
            if line.isspace():
                days_list.append(-1)
                continue
            days_list.append(int(line))
    #print(days_list)
    #return days_list
    #avg_list = [x for x in days_list if x != -1]
    #avg = round(np.mean(avg_list))
    #print(avg)
    #result = [x if x!=-1 else avg for x in days_list]
    #print(result)
    return days_list


def get_days_first_to_last_commit(repo_name):
    days_list = []
    with open(INPUT_FOLDER_PATH + repo_name + '/daysBetweenFirstLast.txt', encoding='utf-8') as file:
        for line in file:
            if line.isspace():
                days_list.append(0)
                continue
            days_list.append(int(line))
    return days_list

def get_files(repo_name):
    files_list = []
    with open(INPUT_FOLDER_PATH + repo_name + '/files.txt', encoding='utf-8') as file:
        for line in file:
            if line.isspace():
                files_list.append(0)
                continue
            files_list.append(int(line))
    return files_list

def get_commit_messages(repo_name):
    commit_messages_list = []
    with open(INPUT_FOLDER_PATH + repo_name + '/commitMsgs.txt', encoding='utf-8') as file:
        for line in file:
            if line.isspace():
                commit_messages_list.append(0)
                continue
            commit_messages_list.append(int(line))
    return commit_messages_list

def get_days_worked(repo_name):
    days_worked_list = []
    with open(INPUT_FOLDER_PATH + repo_name + '/daysWorked.txt', encoding='utf-8') as file:
        for line in file:
            if line.isspace():
                days_worked_list.append(-1)
                continue
            days_worked_list.append(int(line))
    avg_list = [x for x in days_worked_list if x != -1]
    avg = round(np.mean(avg_list))
    result = [x if x!=-1 else avg for x in days_worked_list]
    return result

def get_files_blamed(repo_name):
    files_blamed_list = []
    with open(INPUT_FOLDER_PATH + repo_name + '/filesBlame.txt', encoding='utf-8') as file:
        for line in file:
            if line.isspace():
                files_blamed_list.append(0)
                continue
            files_blamed_list.append(int(line))
    return files_blamed_list

def get_issues(repo_name):
    issues_list = []
    with open(INPUT_FOLDER_PATH + repo_name + '/issues.txt', encoding='utf-8') as file:
        for line in file:
            if line.isspace():
                issues_list.append(0)
                continue
            issues_list.append(int(line))
    return issues_list


def get_pulls(repo_name):
    pulls_list = []
    with open(INPUT_FOLDER_PATH + repo_name + '/pullsCreated.txt', encoding='utf-8') as file:
        for line in file:
            if line.isspace():
                pulls_list.append(0)
                continue
            pulls_list.append(int(line))
    return pulls_list



def get_merges(repo_name):
    merges_list = []
    with open(INPUT_FOLDER_PATH + repo_name + '/merges.txt', encoding='utf-8') as file:
        for line in file:
            if line.isspace():
                merges_list.append(0)
                continue
            merges_list.append(int(line))
    return merges_list






