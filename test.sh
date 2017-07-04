#!/bin/bash
folder=`date +"%Y%m%d"`
if [ ! -d $folder ]; then
    /bin/mkdir $folder
fi
cd $folder


function check_and_run_script {
    local script=$1
    local flag=$2

    if [ ! -f $flag ]; then
        python3 ../read/$script
        if [ $? == 0 ]; then
            touch $flag
        else
            exit 0
        fi
    fi
}


# Call 01_prepare_db.py
script01="01_prepare_db.py"
step01=".01_done"
check_and_run_script $script01 $step01

# Call 02_article_list.py
script02="02_article_hot_list.py"
step02=".02_done"
check_and_run_script $script02 $step02

# Call 03_article.py
script03="15_article_directory_list.py"
step03=".03_done"
check_and_run_script $script03 $step03

# Call 04_image_link.py
script04="16_article_content.py"
step04=".04_done"
check_and_run_script $script04 $step04