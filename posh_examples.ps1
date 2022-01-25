$user_root = '' #scripts for HelpDesk, copy acces rights between users
$list_target_users = ('')
foreach ($user_target in $list_target_users) {
    $group_list = Get-ADUser -Identity $user_root -Properties *| select memberof
    foreach ($group in $group_list.memberof) {
        $group_name =  $group.Substring(3, $group.indexof(',') - 3)
        Add-ADGroupMember -Identity $(get-adgroup -Filter {Name -eq $group_name}) -Members $user_target
        write-host "User " -NoNewline
        write-host $($user_target) -ForegroundColor Green -NoNewline
        write-host " added in group " -NoNewline
        write-host "$($group_name)" -ForegroundColor Green 
    
}
    Write-Host 'Copying groups completed' -ForegroundColor Cyan 
}


#change vm storage policy for list_vm
$vm_list = (
)
foreach ($vm_name in $vm_list) {
    (get-vm -name $vm_name), (Get-HardDisk -VM $vm_name) | Get-SpbmEntityConfiguration |Set-SpbmEntityConfiguration  -StoragePolicy '' 
}