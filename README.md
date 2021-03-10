# gnu pass -> bitwarden exporter

I didn't like any of the suggestions I could find online for moving from gnu pass to bitwarden, so I threw this together.  Keep in mind this was a one-time need for me so it's quick and dirty.

This tool assumes you're going to copy everything out of gnu pass into
bitwarden.  It only creates bitwarden 'login' items.  If you have a
ton of credit cards or secure notes or whatever, yuo'll want to
change it so it generates bitwarden's JSON correctly.  See [here](https://bitwarden.com/help/article/condition-bitwarden-import/#condition-a-json) for some more details.

## exported structure

My gnu pass vault had some folder structure to it, which I initially tried to just port over to bitwarden, but bitwarden sorts all the top level items that aren't in a folder into a folder called "No Folder".  Additionally, in the "All Items" view, it doesn't include the folder name in the display of each item.  So, since I had several folders with passwords on a given service for me and each of my kids

```
someservice/
someservice/me
someservice/kid1
someservice/kid2
someservice/kid3
otherservice/me
otherservice/kid2
otherservice/kid3
```

in my initial export, these were showing up under "All Items" as half a dozen items all with the name `me` or all with the name `kid1`, and it was hard to tell which item was for which service.

This exporter keeps the "unfiled items go under the `No Folder` folder" aspect, but gives each of the items a name that includes its relative path in my gnu pass vault.  In the above example, `someservice/kid2` would show up as an item with name `servicename/kid2` under the folder `someservice`.  This way, the "All Items" view is at least somewhat useful to me.

## quickstart

First, prepare by dumping all your passwords from gnu pass to a temporary directory on disk with something like

```
% mkdir -p root && cd root
% ( cd $PASSWORD_STORE_DIR && find . \! -path \*.git\* -a -type d ) | sed -e 's#^./##' | while read d; do mkdir -p $d; done
% ( cd $PASSWORD_STORE_DIR && find . -type f -name \*.gpg ) | sed -e 's#^./##' -e 's#\.gpg$##' | sort | while read fname; do echo $fname; pass ${fname} > ${fname}; done
```

Then run this file on the dumped output

```
% python gather.py > ~/Downloads/bitwarden_import.json
```

and go to Bitwarden's web vault, tools -> import, choose "Bitwarden
json" and pick the file.  It takes a little while if you have a lot of
entries.

Don't forget to securely delete the temporary directory when you're done.
