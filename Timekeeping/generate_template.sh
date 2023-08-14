#!/bin/bash

# /////////////////////////////////////////////////////////////////////////////
#
# Summary: Read in template, output to named file for the next 4 weeks
#
# Prerequisites: A template named weekly_template.tmpl
#
# Description: This script generates <X weeks for PI sprint?> of 
#    files based on a template. The contents of the template are
#    copied into a new text file named YYYY-MM-DD.txt where "DD"
#    is the date of that week's Monday.  Within the template can
#    be the following placeholders:
#      1) The string "# Week of" is replaced with 
#         "# Week of YYYY-MM-DD" where "DD" is the date of that 
#         week's Monday
#         
#         Example: 
#           Comment "# Week of" replaced with "# Week of 2023-07-03"
#      2) The strings MM TT WW TT FF SS SS are each replaced with 
#         the date of the day of the week in question. Because global
#         replacements are not used, it's assumed that the first TT
#         is Tuesday and the first SS is Saturday
#
#         Example:
#           Heading "MM Monday" replace with "07 Monday"
#
# /////////////////////////////////////////////////////////////////////////////

# Set DEBUG to false unless otherwise assigned
DEBUG="${DEBUG:-false}"

##
## Get template contents
##

# Check for template to exist
if [ -f ./weekly_template.tmpl ]
then
  TEMPLATE_FILE=./weekly_template.tmpl
  echo "Using $TEMPLATE_FILE as the template"
else
  TEMPLATE_FILE="${TEMPLATE_FILE:-unset}"
  if [ $TEMPLATE_FILE == unset ]
  then
    echo "TEMPLATE_FILE is unset. Specify your TEMPLATE_FILE using export TEMPLATE_FILE=./weekly_template.tmpl"
    exit 1
  fi
fi

# Read in the template
template_file_contents=$(<$TEMPLATE_FILE)

if [ $DEBUG == true ]
then
  echo "template file contents: $template_file_contents"
fi

##
## Generate Files
##

echo "Generating weekly files"

# Do date calculations

# Do we start for this week (starting on Monday) or next?
# +%F is shorthand for +%Y-%m-%d
this_monday=$(date -v-monday +%F)

# If this week's file exists, next Monday is our starting point
if [ -f "${this_monday}.txt" ]
then
  this_monday=$(date -v+7d +%F)
fi

# Placeholder Variable Initiation
# Placeholder #1 - Two-letter placeholder for date of DOW
# Make array of DOW
dow=(Monday Tuesday Wednesday Thursday Friday Saturday Sunday)

# Create weekly files for the next 4 weeks starting Monday
for (( i=1; i<=4; i++ ))
do
  echo "Creating file for week starting on $this_monday (Monday)"
  # for each week get the date for the Monday
  start_date=$this_monday
  new_file="./${start_date}.txt"
  # replace "Week of" with value
  #if [ $DEBUG = true ]; then echo "Replacing 'Week of' heading with $start_date"; fi
  #sed -i '' -e "s~#\ Week\ of.*$~# Week of $start_date~" $new_file
  # loop through the days of the week, replace placeholders in variable string before it's written
  counter=0
  for (( j=0; j<7; j++ ))
  do
    # get the date of start of current week
    curr_date=$(date -v+${j}d -jf "%Y-%m-%d" "$this_monday" +'%B %d')
    if [ $DEBUG = true ]; then echo "Current date of week day: $curr_date"; fi
    # replace placeholder with "Month Date"
    if [ $DEBUG = true ]; then echo "Replacing ${dow[j]} with $curr_date"; fi
    # replace __DAY__ and __DATE__
    #sed -i '' -e "1s/${dow[j]}/$curr_date/;t" -e "1,/${dow[j]}/s//$curr_date/" $new_file 
    this_day="${template_file_contents/__DAY__/${dow[counter]}}"
    echo "${this_day/__DATE__/$curr_date}" >> $new_file
    ((counter++))
  done
  # advance it 1 week
  if [ $DEBUG = true ]; then echo "Advancing $start_date by 1 more week"; fi
  this_monday=$(date -v+1w -jf "%Y-%m-%d" "$start_date" +%F)
done
