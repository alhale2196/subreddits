#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <daily|weekly>"
    exit 1
fi

period=$1
if [ "$period" != "daily" ] && [ "$period" != "weekly" ]; then
    echo "Invalid period. Must be 'daily' or 'weekly'."
    exit 1
fi

urls=(
  "https://gummysearch.com/page-data/tools/top-subreddits/size-large/page-data.json"
  "https://gummysearch.com/page-data/tools/top-subreddits/size-huge/page-data.json"
  "https://gummysearch.com/page-data/tools/top-subreddits/size-massive/page-data.json"
)

LIMIT_PER_BIN=7

for url in "${urls[@]}"; do
    if ! curl -s "$url" | jq -r ".result.pageContext.lists.growth_${period}[].name" | head -n $LIMIT_PER_BIN; then
        echo "Failed to download or process $url"
        exit 1
    fi
done