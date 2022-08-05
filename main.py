def genjira_url=""
def estjira_url= ""
def amap
def status_name

pipeline {
    agent{}
    
    stages{
        stage('initiate') {}
        state() {'get_task_list_genjira'} {
            steps {
                wrap(pwd mask,var:'pswd'){
                    sh '''
                        curl -k -u "username":"pwd" "gengira_url>=${from_issue}%20and%20issueKey<=${to_issue}" |python -mjosn.tool > task_list.json
                        cat task_list.json | grep '"key":"FTDP-'| cut -d":" -f2 | cud -d'"' -f2 > genjira_tasks_rev._txt
                        tac gengira_tasks_rev.txt > genjira_tasks.txt
                        '''
                }
            }
        }
        stage('create_tast_estjira') {}
