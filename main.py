
def from socket import AI_V4MAPPED


genjira_url=""
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
        stage('create_tast_estjira') {
            steps{
                script{
                    def file = readFile "genjira_tasks.txt"
                    def lines = file.readLines()
                    
                    file.split('\n').each {String line ->
                        wrap([$class:'MaskPasswordsBuildWrapper', varPasswordPairs: [[password: "${password}", var: 'PSWD']]]) {
                            def resp = sh(script: ''' curl -k -u ${username}: $(password) url ''' + line+ ''' | python -mjoson tool > jira_details.json ''', returnStdout:true)
                            echo resp
                        }
                        
                        def props = readJSON file: 'jira_details.json'
                        summary_value = "${props.fields.summary}"
                        issuetype_name="${props.fields.issuetype.name}"
                        reporter_name="${props.fields.reporter.name}"
                        description="${props.fields.description}"
                        fxver_arch="${props.fields.fixVersions.archived}"
                        echo "Fix Version:${fxver_arch}"
                        fxver_name="${props.fields.fixVersions.name}"
                        fxver_reldate="${props.fields.fixVersions.releasedDate}"
                        fxver_rel="${props.fields.fixVersions.released}"
                        priority_name="${props.fields.priority.name}"
                        labels="${props.fields.labels}"
                        components="${}"
                        try {
                            assignee_name = "${props.fields.assignee.name}"
                        }
                        catch(Exception ex) {
                            assignee_name = "Default"
                        }
                        epic_link = "${props.fields.customfield_12202}"
                        try{
                            resolution_name ="${props.fields.resolution.name}"
                        }
                        catch(Exception ex) {
                            resolution_name=null
                        }
                        attachment_name = "${props.fields.attachment.filename}"
                        attachment_content ="${props.fields.attachment.cotent}"
                        comments="${props.fields.comment.comments.content}"
                        status_name="${props.fields.status.name}"
                        fxver_arch= sh(returnStdout: true,script: "echo${fxver_arch}| cut -d'[' -f2}| cut -d']' -f1").trim()
                        fxver_name=sh(returnStdout: true,script: "echo${fxver_name}| sed ).trim()
                        fxver_reldate=sh(returnStdout: true,script: "echo${fxver_reldate}| cut ).trim()
                        fxver_rel=sh(returnStdout: true,script: "echo${fxver_rel}| cut ).trim()
                        labels=sh(returnStdout: true,script: "echo${labels}| cut ).trim()
                        epic_link=sh(returnStdout: true,script: "echo${epic_link}| sed ).trim()
                        attachment_name=sh(returnStdout: true,script: "echo${attachment_name}| cut ).trim()
                        attachment_content=sh(returnStdout: true,script: "echo${attachment_content}| cut ).trim()
                        comments=sh(returnStdout: true,script: "echo${comments}| cut ).trim()
                        status_name=sh(returnStdout: true,script: "echo${status_name}| cut ).trim()
                        
                        
                        if (description=="null"){
                            env="NA"
                        }
                        if (env=="null"){
                            env = "NA"
                        }
                        
                        if (fxver_arch==""){
                            amap = [
                                fields:
                                [
                                    project:
                                    [
                                        key:"FTCPLAT"
                                    ],
                                    summary:"${summary_value}",
                                    issuetype:
                                    [
                                        name:"$issuetype_name}"
                                    ],
                                    reporter:
                                    [
                                        name:"${reported_name}"
                                    ],
                                    description:"${description}"
                                ],
                                priority:
                                [
                                    name:"${priority_name}"
                                ],
                                assignee:
                                [
                                    name:"${assignee_name}"
                                ]
                            ]
                        } else{
                            amap = [
                                fields:
                                [
                                    project:
                                    [
                                        key:"FTCPLAT"
                                    ],
                                    summary:"${summary_value}",
                                    issuetype:
                                    [
                                        name:"$issuetype_name}"
                                    ],
                                    reporter:
                                    [
                                        name:"${}"
                                    ],
                                    description:"${}"
                                ],
                                fixVersions:[
                                [
                                    archived:"${fxver_arch}",
                                    name:"${fxver_name}",
                                    releaseDate: "${fxver_reldate}",
                                    released: "${fxver_rel}"
                                ]],
                                priority:
                                [
                                    name:"${priority_name}"
                                ],
                                assignee:
                                [
                                    name:"${assignee_name}"
                                ],
                                components:
                                [
                                    name: "${component_name}"
                                ]
                            ]
                            ]
                        }
                        
                        
                        writeJSON file: 'estjira_inout.json', json:amap
                        wrap([$class: 'MaskPasswordsBuildWrapper',varPasswordPairs:[[password: "${password}",var: 'PSWD'']]])){
                            sh '''
                            estjira::: curl::: post
                            jira_issue=grep FTCPLAT jiraop|cut -d',' -f2|cut -d':' -f2| tr -d '"''
                            
                            if [-z $jira_issue]; then
                                excho "Eoor in migrating" '''+line+''' "
                                exit 1
                            fi
                            
                            echo $jira_issue created from '''+Line+'''" >> estjira.output
                            
                            
                            case "'''+status_name+'''" in Backlog")
                                            tansition_id=11
                                            ;;
                                    "Selected for development")
                                            transition_id=21
                                            ;;
                                    "In Progree")
                                            transition_id=31
                                            ;;
                                    "Done")
                                            transition_id: 41
                                            ;;
                            
                            esac
                            
                            
                            curl -v -k - u "":"" -X POST  --data '{"transition":{"id":"'$transition_id'"}} -H "Content-Type": application/json  https://estjira/*/*/issue/$jira_issue/transitions?expand=transitions.fields
                            
                            if [! -z "'''+attachment_name+'''"];then
                                IFS=',' read -r -a name_array <<< "'''+attachment_name+'''"
                                IFS=',' read -r -a content_array  <<< "'''+attachment_content+'''"

                                for (( i=o; i<${#name_array[@]}; i++))
                                do
                                    filename='echo "$#name_array[i]" | sed -e 's/^[[:space]]*//''
                                    curl -k -u "username":"pwd" "$(content_array[i])  > $filename
                                    curl -v -k -u "username":${"pwd"} - POST H"X-Atlassian-Token:nocheck" -F file=@$filename" estjira///attachments
                                done
                           fi
                            
                            
                            if [! -z "'''+comments+'''"];then
                                IFS=',' read -r -a comments_array <<< "'''+comments+'''"
                                
                                for (( c=o; c<${#comments_array[@]}; c++))
                                do 
                                    curl -k -u "":"" ${comments_array[c]} | python -m json.tool > comment$c.json
                                    echo "{" > comment_input.json
                                    cat comment$c.json | grep body | sed 's/,*\r*$//' >> comment_input.json
                                    echo "}" >> comment_input.json
                                    curl -v -k -u "":""  -X POST -H "Content-Type: application/json" -d @comment_input.json estjira_url
                                done
                            fi
                            
                            
                            if [! -z "'''+labels+'''"];then
                                IFS=',' read -r -a labels_array <<< "'''+labels+'''"
                            fi
                            
                            for (( l=o; l<${#labels_array[@]}; l++))
                            do
                            
                                curl -v -k -u "":"" -X PUT --data '{"update":{"labels":[{"add":"'${labels_array[1]}'"}]}}' -H "Content-Type:application/json" estjira_url//issue/$jira_issue
                            done
                         
                            '''
                        }
                        
                        }
                }
            }
        }
                
        stage('Send_email') {
            steps{
                script{
                    emailext attachmentsPattern: '*.outbody,body:'attachedo/p file has issue ids migrated to estjira', subject: 'o/p of Genjira to ESTjira' to: 'tinkunaga.konduru@bacrlays.com'
                }
            }
        }    
}    
}   
