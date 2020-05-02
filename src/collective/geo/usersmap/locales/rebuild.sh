#!/bin/bash

PRODUCT=collective.geo.usersmap

EXCLUDEPOTFILE=`find ../browser/usersmap_kml.pt -name "*.*pt"`

i18ndude rebuild-pot --pot ../locales/${PRODUCT}.pot --exclude=$EXCLUDEPOTFILE --create $PRODUCT ../ 
i18ndude sync --pot ../locales/${PRODUCT}.pot ../locales/*/LC_MESSAGES/${PRODUCT}.po

#i18ndude rebuild-pot --pot ../locales/plone.pot --merge ../locales/manual.pot --create plone ../profiles/
i18ndude rebuild-pot --pot ../locales/plone.pot --create plone ../profiles/
i18ndude sync --pot ../locales/plone.pot ../locales/*/LC_MESSAGES/plone.po

#for lang in $(find ../locales -mindepth 1 -maxdepth 1 -type d); do
#    if test -d $lang/LC_MESSAGES; then
#        msgfmt -o $lang/LC_MESSAGES/${PRODUCT}.mo $lang/LC_MESSAGES/${PRODUCT}.po
#    fi
#done

WARNINGS=`find . -name "*pt" | xargs i18ndude find-untranslated | grep -e '^-WARN' | wc -l`
ERRORS=`find . -name "*pt" | xargs i18ndude find-untranslated | grep -e '^-ERROR' | wc -l`
FATAL=`find . -name "*pt"  | xargs i18ndude find-untranslated | grep -e '^-FATAL' | wc -l`

echo
echo "There are $WARNINGS warnings \(possibly missing i18n markup\)"
echo "There are $ERRORS errors \(almost definitely missing i18n markup\)"
echo "There are $FATAL fatal errors \(template could not be parsed, eg. if it\'s not html\)"
echo "For more details, run \'find . -name \"\*pt\" \| xargs i18ndude find-untranslated\' or"
echo "Look the rebuild i18n log generate for this script called \'rebuild_i18n.log\' on locales dir"

rm ./rebuild_i18n.log
touch ./rebuild_i18n.log

find ../ -name "*pt" | xargs i18ndude find-untranslated > ./rebuild_i18n.log
# Ok, now poedit is your friend!

