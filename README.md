rsync-usb
=========

An implementation of the Rsync protocol that can be used with offline storage when two hosts are not connected by a network.

Summary
-------

This project aims to create a [rsync](http://rsync.samba.org/) like utility which can be used to perform file transfers where no network connection exists.  The rsync protocol is design to be completed in three phases:

1. On the target system, calculate hashes for for chunks of files already existing at the target path.  These hashes are then sent to the source system.
2. On the source system, search the files being copied for chunks of data that already exist on the target system using the supplied hashes.  A plan is then built to instruct the target system on how to make it's files identical to those on the source system.
3. On the target system, follow the plan to make the files identical.

This tool modifies the protocol to save the hashes calculated by the target system, and the plan calculated by the source system, onto storage medium rather than transmitting over the network.  The goal is to allow the rsync process to be used between two disconnected computers even if all you have a USB disk.  Even if the transfer cannot be completed in a single pass, say if the amount of file data to transfer is greater than the size of the intermediate storage medium, the process can still be completed as efficiently as possible by running the script in multiple passes.

Sample Use Cases
----------------

1. One sample use case (indeed the first use case that motivated this project) is to accomplish the off-site backup of a system not connected to high-speed Internet.  If I visit my parents once a week, and want to also assist with protecting their pictures, I can bring my USB disk with me to get a copy of all new photos (and changes to photos) to sync into my big disk array at my house.

