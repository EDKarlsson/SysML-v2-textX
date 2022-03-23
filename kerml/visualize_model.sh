#!/bin/bash

USAGE="Usage: $0 command grammar language [debug,verbose]
clean:
  clean generate *.dot files.

open:
  open dot file after generating it

(check | generate):
  grammar   [*.tx]              textX grammar file that describes the language
  language  [*.kerml]           language file for kerml
  flags     [debug,verbose]     flags to pass to textX app
"

if [ "$#" == "0" ]; then
  echo "$USAGE"
  exit 1
fi

OPEN=0
VERBOSE=0
TARGET='dot'
DEBUG_FLAG=

while (("$#")); do
  case $1 in
  clean)
    echo "Cleaning files."
    find . -name '*.dot' -print -exec rm {} \;
    find . -name '*.png' -print -exec rm {} \;
    exit
    ;;
  check | generate)
    COMMAND=$1
    ;;
  *.kerml)
    LANGUAGE=$(find . -name "$1")
    ;;
  *.tx)
    GRAMMAR_FILE=$(find . -name "$1")
    IFS='.'
    read -r -a inFile <<< "$1"
    GRAMMAR=${inFile[0]}
    IFS=\n
    ;;
  dot)
    TARGET='dot'
    ;;
  PlantUML)
    TARGET='PlantUML'
    ;;
  debug)
    DEBUG_FLAG='--debug'
    ;;
  verbose)
    VERBOSE=1
    ;;
  open)
    OPEN=1
    ;;
  esac
  shift
done

if [[ ${VERBOSE} -eq 1 ]]; then
  echo "================================================================================"
  echo "Variables:"
  echo "--------------------------------------------------------------------------------"
  echo "Path to Grammar File: ${GRAMMAR_FILE}"
  echo "Grammar: ${GRAMMAR}"
  echo "Language: ${LANGUAGE}"
  echo "Target: ${TARGET}"
  echo "Flags: ${DEBUG_FLAG}"
  echo "================================================================================"
fi

case ${COMMAND} in
check)
  if [[ ${VERBOSE} -eq 1 ]]; then
    echo "Checking Language: ${LANGUAGE}"
    echo "textx ${DEBUG_FLAG} check ${LANGUAGE} --grammar ${GRAMMAR_FILE}"
    echo "--------------------------------------------------------------------------------"
    fi
  textx ${DEBUG_FLAG} check "${LANGUAGE}" --grammar "${GRAMMAR_FILE}"
  ;;
generate)
  if [[ ${VERBOSE} -eq 1 ]]; then
    echo "Generating Grammar: ${GRAMMAR} dot file"
    echo "textx ${DEBUG_FLAG} generate ${GRAMMAR_FILE} --target ${TARGET} --overwrite"
    echo "dot -Tpng -O $(find . -name "${GRAMMAR}".dot)"
    echo "--------------------------------------------------------------------------------"
  fi
  textx ${DEBUG_FLAG} generate "${GRAMMAR_FILE}" --target ${TARGET} --overwrite
  dot -Tpng -O "$(find . -name "${GRAMMAR}".dot)"
  ;;
esac

if [[ ${OPEN} -eq 1 ]]; then
    echo "--------------------------------------------------------------------------------"
    echo "Opening Generated: ${GRAMMAR}.dot.png"
    echo "--------------------------------------------------------------------------------"
    find . -name '*.dot.png' -exec open {} \;
fi
