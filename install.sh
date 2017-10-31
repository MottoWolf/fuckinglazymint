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
    options=("Chrome ${opts[1]}" "Cinnamon ${opts[2]}" "Git ${opts[3]}" "Hangups ${opts[4]}" "KeepassX ${opts[5]}" "Spotify ${opts[6]}" "Steam ${opts[7]}" "Terminator ${opts[8]}" "Vim ${opts[9]}" "Virtualbox ${opts[10]}"  "INSTALL")
    select opt in "${options[@]}"
    do
        case $opt in
            "Chrome ${opts[1]}")
                choice 1
                break
                ;;
            "Cinnamon ${opts[2]}")
                choice 2
                break
                ;;
            "Git ${opts[3]}")
                choice 3
                break
                ;;
            "Hangups ${opts[4]}")
                choice 4
                break
                ;;
            "KeepassX ${opts[5]}")
                choice 5
                break
                ;;
            "Spotify ${opts[6]}")
                choice 6
                break
                ;;
            "Steam ${opts[7]}")
                choice 7
                break
                ;;
            "Terminator ${opts[8]}")
                choice 8
                break
                ;;
            "Vim ${opts[9]}")
                choice 9
                break
                ;;
            "Virtualbox ${opts[10]}")
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
         #echo ansible-playbook playbook.yml --tags "$selected" | rev | cut -c 4- | rev
	  echo ansible-playbook playbook.yml --tags $selected | rev | cut -c 4- | rev
    fi
done
#ansible-playbook playbook.yml --tags 
