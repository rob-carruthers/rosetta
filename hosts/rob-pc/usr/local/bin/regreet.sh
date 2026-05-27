#!/bin/sh
(
  sleep 0.5
  wlr-randr | grep -o '^\S*' | while read output; do
    wlr-randr --output "$output" --mode 1920x1080@143.998993
  done
) &
exec regreet
