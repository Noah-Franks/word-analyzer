if [[ $1 == '' ]]; then
	echo '\033[0;31mPlease enter a word\033[0m'
	exit 1
fi

invert=$2
if [[ $invert == '' ]]; then
	invert='false'
else 
	invert='true'
fi

search_word=$1

speaker=''
all_speakers=''

selected=''
while read line; do
	if [[ ! $line == *' '* ]]; then
		speaker=$line
		all_speakers="$all_speakers|$line"
	else
		if [[ $line == *"$search_word"* ]]; then
			echo "$speaker $line"
			selected="$selected|$speaker"
		fi
	fi
done < agent-profiles.txt

all_speakers="${//\|/ }"

echo "\t$selected"
echo "\t$all_speakers"