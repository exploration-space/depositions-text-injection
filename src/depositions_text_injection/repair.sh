#!/usr/bin/env bash

for i in `ls *.xml`;    # for each xml file in current dir:
do                      # run this monster regexp in perl:
echo -en "\r"$i"   "    # show filename of currently processed file
perl -pe '
s|(;[^&]*);|\1|gs;                  # remove semicolons which are not endings of a entities

s|<(/?)not([ >])|<\1note\2|gs;      # repair common tag names typos; not -> note </to> -> </del> (???)

s|</?dead([\s>]?)|</del><add\1|gs;  # fix </dead to </del><add

s|</dell>|</del></del>|gs;          # and <dell> to </del><del
s|</?dell([\s>]?)|</del><del\1|gs;

s|<(/?)named? |<\1name>|gs;         # <named> to <name>

s|<(/?)a([ >])|<\1del\2|gs;         # rename <a> tags to <del> as should be

s|</([A-Za-z_][^<>]*?) ([^<>]*?)>|<\1 \2>|g;    # all "closing" tags with attributes are repaired to be opening tags

s|(>[^<]*?)rend="|\1<del rend="|g;              # adding proper opening to random rand="stiketrough etc. in text
s|(>[^<]*?)place="|\1<add place="|g;            # ...and to random place="


# enclosing tags which were "closed" with single angle bracket, like this: <del rand="striketrough">something, bla, bla> (or) <
s|(<([A-Za-z_][^<>\s]*?)>)([\w\s&;.,#'"'"']*?)>|\1\3</\2>|gs;
s|(<([A-Za-z_][^<>\s]*?)>)([\s]*[\w&;.,#'"'"']+[\w\s&;.,#'"'"']*?)<([^>]*?)<|\1\3</\2>\4<|gs;
s|(<([A-Za-z_][^<>\s]*?)\s+[^<>]*?>)([\w\s&;.,#'"'"']*?)>|\1\3</\2>|gs;
s|(<([A-Za-z_][^<>\s]*?)\s+[^<>]*?>)([\s]*[\w&;.,#'"'"']+[\w&;.,\s#'"'"']*?)<([^>]*?)<|\1\3</\2>\4<|gs;


s|(</?[A-Za-z_][^<>]*?)<|\1><|g;        # enclosing tags that are not closed before the start of next tag

s|(</[A-Za-z_][^<>\s]*?) |\1>|g;        # all closing tags that are not immadietly closed are being closed

s|(?<!<del )rend="|<del rend="|g;       # setting tags with rend param to del


s|</to[ >]|</del>|gs;                   # change </de/something/> tags to </del>
s|</?de[^l][\w[:punct:]]*?>|</del>|sg;
s|</de>|</del>|sg;

                                        # merging double occurrences of del tags
s|(?:<del rend="strikethrough">[\s]*){2}|<del rend="strikethrough">|gs;
s|(?:<del rend="(?:double)?strikethrough">[\s]*){2}|<del rend="doublestrikethrough">|gs;
s|</del></del>|</del>|gs;


s|(<[A-Za-z_][^<>]*>)([^/]*?)\1|\1\2|sg;    # deduplicate opening tags that werent closed in between


s|&am[^p]|&amp; |gs;        # repair broken entities of ampersands
s|&amp[^;]|&amp; |gs;
s|&(?!amp)|\1|gs;
s|am;|&amp;|gs;

s|<([^>]*<)|\1|gs;          # remove hanging angle brackets

s|(</?damage)d|\1|gs;                   # repair often broken damage tags
s| damage>| <damage>|gs;
s|<supplied([^>]+?)>|<supplied>\1|gs;   # ...and supplied tags

' $i > "repaired/"$i; # and dump result to corresponding file in "repaired" subdirectory
done
echo # just to finish
