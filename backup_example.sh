!#/bin/bash
#we need to copy some files from the previous day 
search_path='serach_path'
storage_path='target_path'
current_date=$(date +"%Y-%m-%d" -d "yesterday") 
current_year=$(date +"%Y" -d "yesterday") #get previous year
current_month=$(date +"%m" -d "yesterday") #get previous month
current_day=$(date +"%Y-%m-%d" -d "yesterday") #get previous day
if [[ ! -e $storage_path/$current_year/$current_month/$current_day ]]; then
    mkdir -p $storage_path/$current_year/$current_month/$current_day # create target directory
    if [[ $? -ne 0 ]]; then echo $(date +'%Y-%m-%d %T') Can\'t create directory. Exit code 1 >> /var/log/copy_pcr_result.log; fi
    find $search_path/$current_date -regextype posix-extended -regex '.+_p_.+\.pdf$' -exec cp {} $storage_path/$current_year/$current_month/$current_day \; #find and copy files by mask
    if [[ $? -eq 0 ]]; then #logging
        echo $(date +'%Y-%m-%d %T') Job successful. Exit code 0 >> /var/log/copy_pcr_result.log 
        else 
        echo $(date +'%Y-%m-%d %T') Job failed. Exit code 1 >> /var/log/copy_pcr_result.log 
    fi
else
    echo $(date +'%Y-%m-%d %T') Current directory exist, job canceling. Exit code 0 >> /var/log/copy_pcr_result.log
fi
