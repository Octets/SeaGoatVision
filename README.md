SeaGoatVision
=============

Description
--------------
SeaGoatVision is a computer vision system running into a server.

Actually, this platform is used to doing robotic.

Principal feature :
 - Manage multiple client and media
 - Run filterchain
 - Control filter by parameters
 - Give environnement for debug and create filter
 - Run in local or in remote
 - Can send message to other platform
 - Execute Python and C++ filters

Installation
-------------
Be sure to read the INSTALL.md file.

Operating instructions
---------------------------
Read HOWTO.md file.

License
---------
Read LICENSE file.

Contact information
------------------------
Go on website https://github.com/Octets/SeaGoatVision and create an issue.

Known bugs
---------------
The bugs is showing in issues of the project : https://github.com/Octets/SeaGoatVision/issues?labels=bug&page=1&state=open

Troubleshooting
-------------------
The project is only supported in python 2.7, because opencv is not supported in python 3 at this moment.

Credits
---------
Thanks club Capra and club Sonia to support us.

 - http://capra.etsmtl.ca
 - http://sonia.etsmtl.ca

Changelog
----------------
 - 0.2 : version with Qt graphic interface, GTK is removed. Integrate Firewire camera, client/server with Protobuf, add parameters between client and filter/media. The analyser of filter and the camera Ethernet is removed temporary.
 - 0.1 : version with GTK graphic interface. Ready for the Capra competition. Can create and run filterchain, reload filters, save parameters, observer filters output, run python and c++ filters, and record video.
