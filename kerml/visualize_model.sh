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
OUTPUT=../_dot_files
GEN_GRAMMAR=0
GEN_LANGUAGE=0

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
    LANGUAGE_FILE=$(find . -name "$1")
    GEN_LANGUAGE=1
    IFS='.'
    read -r -a inFile <<<"$1"
    MODEL=${inFile[0]}
    IFS=\n
    ;;
  *.tx)
    GRAMMAR_FILE=$(find . -name "$1")
    IFS='.'
    read -r -a inFile <<<"$1"
    GRAMMAR=${inFile[0]}
    IFS=\n
    GEN_GRAMMAR=1
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
  echo "Language: ${LANGUAGE_FILE}"
  echo "Target: ${TARGET}"
  echo "Flags: ${DEBUG_FLAG}"
  echo "================================================================================"
fi

case ${COMMAND} in
check)
  if [[ ${VERBOSE} -eq 1 ]]; then
    echo "Checking Language: ${LANGUAGE_FILE}"
    echo "textx ${DEBUG_FLAG} check ${LANGUAGE_FILE} --grammar ${GRAMMAR_FILE}"
    echo "--------------------------------------------------------------------------------"
  fi
  textx ${DEBUG_FLAG} check "${LANGUAGE_FILE}" --grammar "${GRAMMAR_FILE}"
  ;;
generate)
  if [[ ${GEN_GRAMMAR} -eq 1 ]]; then
    if [[ ${VERBOSE} -eq 1 ]]; then
      echo "Generating Grammar: ${GRAMMAR} dot file"
      echo "textx ${DEBUG_FLAG} generate ${GRAMMAR_FILE} --target ${TARGET} --overwrite -o ${OUTPUT}"
      echo "dot -Tpng -O $(find . -name "${GRAMMAR}".dot)"
      echo "--------------------------------------------------------------------------------"
    fi
    textx ${DEBUG_FLAG} generate "${GRAMMAR_FILE}" --target ${TARGET} --overwrite
    GRAMMAR_DOT=$(find . -name "${GRAMMAR}".dot)
    dot -Tpng -O "${GRAMMAR_DOT}"
  fi
  if [[ ${GEN_LANGUAGE} -eq 1 ]]; then
    if [[ ${VERBOSE} -eq 1 ]]; then
      echo "Generating Language: ${LANGUAGE_FILE} dot file"
      echo "textx ${DEBUG_FLAG} generate --grammar ${GRAMMAR_FILE} --target ${TARGET} --overwrite -o ${OUTPUT}" "${LANGUAGE_FILE}"
      echo "dot -Tpng -O $(find . -name "${MODEL}".dot)"
      echo "--------------------------------------------------------------------------------"
    fi
      textx ${DEBUG_FLAG} generate --grammar "${GRAMMAR_FILE}" --target ${TARGET} --overwrite -o ${OUTPUT} "${LANGUAGE_FILE}"
    LANGUAGE_DOT=$(find ${OUTPUT} -name "${MODEL}".dot)
    dot -Tpng -O "${OUTPUT}/${LANGUAGE_DOT}"
  fi
  ;;
esac

if [[ ${OPEN} -eq 1 ]]; then
  echo "--------------------------------------------------------------------------------"
  echo "Opening Generated: ${GRAMMAR}.dot.png"
  echo "--------------------------------------------------------------------------------"
  find . -name "${GRAMMAR}.dot.png" -exec open {} \;

  echo "--------------------------------------------------------------------------------"
  echo "Opening Generated: ${MODEL}.dot.png"
  echo "--------------------------------------------------------------------------------"
  find ${OUTPUT} -name "${MODEL}.dot.png" -exec open {} \;
fi
