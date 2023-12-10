#!/bin/bash

echo "Welcome to Git Command Script"
while true
do
	echo "Enter the number for the action you want to perform:"
	if [ -d '.git' ]
	then
		echo "1. Git Status"
		echo "2. Git Add"
		echo "3. Git Commit"
		echo "4. Git Push"
		echo "5. List Branches"
		echo "6. Create Branch"
		echo "7. Switch Branch"
		echo "8. Create and Switch Branch"
		echo "9. Delete Local Repo!!"
		echo "10. Exit"

		read choice

		case $choice in
    		1)
        		git status
        		;;
    		2)
        		echo "Enter file(s) to add (separated by space):"
        		read files
        		git add $files
        		;;
    		3)
        		echo "Enter commit message:"
        		read message
        		git commit -m "$message"
        		;;
    		4)
       	 		echo "Existing Braches:"
				git branch
				echo "Enter remote branch name (e.g., main):"
        		read remote_branch
        		git push origin $remote_branch
        		;;
			5)
				echo "Existing Braches:"
				git branch
				;;
    		6)
				echo "Existing Braches:"
				git branch
				echo "Enter Branch name(except above):"
				read name
				if [ "$(git branch | grep -c -w $name)" -gt "0" ]
				then
					echo "branch exist!!"
				else
					echo "Creating Branch..."
        			git branch $name
					echo " $name Created."
				fi
        		;;
    	
			7)
				echo "Existing Braches:"
				git branch
				echo "Enter Branch name(present in above):"
				read name
				if [ "$(git branch | grep -c -w $name)" -gt "0" ]
				then	
					echo "Switching Branch..."
					git checkout $name
					echo "Switched to  $name."
				else
					echo "Branch doesn't exists!"
				fi
				;;
			8)
				echo "Existing Braches:"
				git branch
				echo "Enter Branch name(except above):"
				read name
				if [ "$(git branch | grep -c -w $name)" -gt "0" ]
				then
					echo "branch exist!!"
				else
					echo "Creating Branch..."
						git branch $name
					echo " $name Created."
				fi
				echo "Switching Branch..."
					git checkout $name
				echo "Switched to  $name."
					;;
			9)
				echo "Do You Really Want to Delete?(y/n)"
				read choice1
				case $choice1 in
					y)
						echo "Deleting!!"
						rm -r -f .git
						echo "Deleted."
						;;
					n)
						echo "Deletion Stopped!"
						;;

					*)
						echo "Invaild Option...not able to delete"
						;;
				esac
				;;
			10)
				echo "Exiting script..."
				exit 0
				;;
		
			*)
				echo "Invalid option. Please choose a number between 1 to 5."
				;;
		esac

	else
		echo "1. Git init"
		echo "2. Exit"
		
		read choice

		case $choice in
			1)
				git init
				git branch -m master main
				echo "Add remote branch link"
				read remotelink
				git remote add origin $remotelink
				;;

			2)
				echo "Exiting script..."
				exit 0
				;;
			*)
				echo "Invalid option. Please choose a number between 1 to 5."
				;;
		esac
	fi
done