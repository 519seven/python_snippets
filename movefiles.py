#!/bin/bash
exec 1> >(logger -s -t $(basename $0)) 2>&1
# https://urbanautomaton.com/blog/2014/09/09/redirecting-bash-script-output-to-syslog/

# The pattern were looking for is <hoa> <docsubject> <yyyy> <mm> <dd>.{pdf,doc}

TARGET=/var/www/html/wp-content/uploads
SOURCE=~ithelper/Site_Files

checkYear () {
	if [[ "$1" =~ .*"2020".* ]]; then
		YEAR=2020
	elif [[ "$1" =~ .*"2019".* ]]; then
		YEAR=2019
	else
		>&2 echo "File $1 did not match; is the year included in the filename and is it 4 digits?"
	fi
}
checkTopic () {
	if [[ "$1" =~ .*"minute".* ]] || [[ "$1" =~ .*"annual".* ]] || [[ "$1" =~ .*"meeting".* ]]; then
		TOPIC=minutes
	elif [[ "$1" =~ .*"newsletter".* ]]; then
		TOPIC=newsletters
	elif [[ "$1" =~ .*"document".* ]]; then
		TOPIC=documents
	else
		>&2 echo "File $1 did not match; is the topic included in the name?"
	fi
	
}
checkAssoc () {
	if [[ $1 =~ .*berkshire.* ]] || [[ $1 =~ .*berkshire[[:space:]]landing.* ]]; then
		ASSOC="berkshirelanding"
	elif [[ $1 =~ .*bpoa.* ]] || [[ $1 =~ .*branchlands.* ]] || [[ $1 =~ .*branch[[:space:]]lands.* ]]; then
		ASSOC=branchlands
	elif [[ $1 =~ .*chathamridge.* ]] || [[ $1 =~ .*chatham[[:space:]]ridge.* ]]; then
		ASSOC=chathamridge
	elif [[ $1 =~ .*creekside.* ]] || [[ $1 =~ .*vhmcoa.* ]]; then
		ASSOC=creekside
	elif [[ $1 =~ .*druidhill.* ]] || [[ $1 =~ .*druid[[:space:]]hill.* ]]; then
		ASSOC=druidhill
	elif [[ $1 =~ .*huntingtonvillage.* ]] || [[ $1 =~ .*huntington[[:space:]]village.* ]]; then
		ASSOC=huntingtonvillage
	elif [[ $1 =~ .*laurelpark.* ]] || [[ $1 =~ .*laurel[[:space:]]park.* ]]; then
		ASSOC=laurelpark
	elif [[ $1 =~ .*riverrun.* ]] || [[ $1 =~ .*river[[:space:]]run.* ]]; then
		ASSOC=riverrun
	elif [[ $1 =~ .*solomoncourt.* ]] || [[ $1 =~ .*solomon[[:space:]]court.* ]]; then
		ASSOC=solomoncourt
	elif [[ $1 =~ .*somerchase.* ]] || [[ $1 =~ .*somer[[:space:]]chase.* ]]; then
		ASSOC=somerchase
	elif [[ $1 =~ .*villagehomesiii.* ]] || [[ $1 =~ .*village[[:space:]]homes[[:space:]]iii.* ]]; then
		ASSOC=villagehomesiii
	elif [[ $1 =~ .*villagehomeiv.* ]] || [[ $1 =~ .*village[[:space:]]homes[[:space:]]iv.* ]]; then 	
		ASSOC=villagehomesiv
	elif [[ $1 =~ .*villas.* ]] || [[ $1 =~ .*villas[[:space:]]at[[:space:]]southern[[:space:]]ridge.* ]]; then
		ASSOC=villasatsouthernridge
	else
		>&2 echo "File $1 did not match; is this a new association or is the filename pattern wrong?"
	fi
}

OIFS="$IFS"
IFS=$'\n'
for i in $(find $SOURCE -type f); do
	ASSOC=
	YEAR=
	TOPIC=
	# convert to lowercase
	li=$(echo "$i" | tr '[:upper:]' '[:lower:]')
	checkAssoc "$li"
	checkYear "$li"
	checkTopic "$li"
	if [[ -z $ASSOC ]] || [[ -z $YEAR ]] || [[ -z $TOPIC ]]; then
		>&2 echo "Variable is unset: |$ASSOC|$YEAR|$TOPIC|"
		>&2 echo "File $i did not allow us to match something known."	# http://www.tldp.org/LDP/abs/html/io-redirection.html
	else
		DEST=${TARGET}/${ASSOC}/${TOPIC}/${YEAR}/ 
		mv "$i" $DEST
		>&2 echo "File $i moved to $DEST" 
	fi
done
IFS="$OIFS"
exit 0
