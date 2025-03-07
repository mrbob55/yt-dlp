#!/usr/bin/env sh
# exec "${PYTHON:-python3}" -Werror -Xdev "$(dirname "$(realpath "$0")")/yt_dlp/__main__.py" "$@"
exec "${PYTHON:-python3}" "$(dirname "$(realpath "$0")")/yt_dlp/__main__.py" "$@"
