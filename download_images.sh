while IFS=' ' read -r name url || [ -n "$name" ]; do curl -o "images/${name}" "${url}"; done < images.txt