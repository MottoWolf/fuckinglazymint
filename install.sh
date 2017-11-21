#!/bin/bash
# El demigrante

choice () {
    local choice=$1
    if [[ ${opts[choice]} ]] # toggle
    then
        opts[choice]=
    else
        opts[choice]="[*]"
    fi
}

PS3='Please enter your choice: '
while :
do
    clear
    options=("chrome ${opts[1]}" "cinnamon ${opts[2]}" "git ${opts[3]}" "hangups ${opts[4]}" "keepassX ${opts[5]}" "spotify ${opts[6]}" "steam ${opts[7]}" "terminator ${opts[8]}" "vim ${opts[9]}" "virtualbox ${opts[10]}"  "INSTALL")
    select opt in "${options[@]}"
    do
        case $opt in
            "chrome ${opts[1]}")
                choice 1
                break
                ;;
            "cinnamon ${opts[2]}")
                choice 2
                break
                ;;
            "git ${opts[3]}")
                choice 3
                break
                ;;
            "hangups ${opts[4]}")
                choice 4
                break
                ;;
            "keepassX ${opts[5]}")
                choice 5
                break
                ;;
            "spotify ${opts[6]}")
                choice 6
                break
                ;;
            "steam ${opts[7]}")
                choice 7
                break
                ;;
            "terminator ${opts[8]}")
                choice 8
                break
                ;;
            "vim ${opts[9]}")
                choice 9
                break
                ;;
            "virtualbox ${opts[10]}")
                choice 10
                break
                ;;
            "INSTALL")
                break 2
                ;;
            *) printf '%s\n' 'invalid option';;
        esac
    done
done

printf '%s\n' 'Installing...'
for opt in "${!opts[@]}"
do
    if [[ ${opts[opt]} ]]
    then
	 selected=$(printf '%s\n' "${options[opt - 1]}") 
	  echo ansible-playbook ansible/playbook.yml --tags $selected | rev | cut -c 4- | rev
          ansible-playbook ansible/playbook.yml --tags "$selected" | rev | cut -c 4- | rev

    fi
done
#ansible-playbook playbook.yml --tags 
