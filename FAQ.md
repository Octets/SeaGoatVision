FAQ
---

INSTALLATION
============

1. Error on compiling filter in c++ with opencv. Example, with the filter ScipyExample.py.
Do you install opencv-dev? Is this repertory exist: /usr/local/include/opencv
If not, maybe you need this: sudo ln -s /usr/include/opencv /usr/local/include/opencv

2. Error when recording video.
Maybe you need to compile opencv with ffmpeg. Be sure you install ffmpeg dependance.
About fedora package, follow this: https://bugzilla.redhat.com/show_bug.cgi?id=812628

DEVELOP FILTERS
===============

1. How adding filters. Template of code is in the directory: filters/template/
Add your code in filters/private or filters/public
Read filters/README for more information.

2. How running filters. You need to open a client and create filterchain.
The configuration is in this directory: configurations/private or configurations/public
Read configurations/README for more information.
