if [[ $1 == '' ]]; then
	echo '\033[0;31mPlease enter a word\033[0m'
	exit 1
fi

while read line; do
	if [[ ! $line == *' '* ]]; then
		echo $line
	fi

done < agent-profiles.txt