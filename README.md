# NetFileXfer TLS Programming

This program was a part of my college course assignment to implement a TLS/SSL programming to encrypt file transfer in a tunnel. This program is accompanied by Wireshark to do further investigation when the packets being sent are encrypted. This program also uses open source OpenSSL that came with using Ubuntu. 

## How to use NetFileXfer

There are two programs to this project: `NetFileXferServer.py` and `NetFileXferClient.py`.

Before running these files, it is important to refer to the **Installation** instructions on installing Wireshark on Linux to analyze the packets in this project.

In order for the `NetFileXferServer.py` to work, it needs to have your own cert.pem and key.pem.<br>
Refer to the installation instructions on how to use OpenSSL to generate these certifications.

After these prior set-ups, the programs can be run in terminal.

## NetFilexfer Server and Client
Before running the program, have Wireshark capture these packets using the `any` option.

Open one terminal window. To run the `NetFileXferServer.py` program in terminal, traverse through the directories from the `usr` using the command:
> `cd NetFileXfer_TLSProgramming` > `cd server`

Next, invoke the server program to start the server with this command:
> `python3 NetFileXferServer.py [port_number]`<br>
> ex: `python3 NetFileXferServer.py 7800`

* NOTE: Interpreter may vary (e.g. 'py', 'python', 'python2', 'python3', etc.) so type the first part according to your machine.

Second, run the `NetFileXferClient.py` on a separate terminal to let the client connect to the server and send files securely.<br>
Be sure that the client's port number matches with the server.
>`python3 NetfileXferClient.py [IP] [port number] [file]`<br>
> ex: `python3 NetFileXferClient.py localhost 7800 test.txt`

Inside this file, there is a `test.txt` and a `mountain-lake.jpg`. You are allowed to run these example files or add more files to your liking. Doing so will serve a good purpose to let Wireshark capture these encrypted packets.

# Installation

## OpenSSL Set up (for TLS)
For this first part of needing a key.pem or cert.pem, OpenSSL must be set up first in order to generate these two.

To verify OpenSSL exists in your Linux, in the terminal, type `openssl version`.

If it does exist, in the terminal, type: 

>`openssl req -newkey rsa:2048 -new -nodes -x509 -days 3650 -keyout key.pem -out cert.pem`

This procedure will prompt you to enter some required information for a Distinguished Name. Leaving these fields blank will cause this prompt to fail!

After generating the key.pem and the cert.pem, move them to the `NetFileXfer` folder inside the same directory called `server` where the `NetFileXferServer.py` is located.

Doing so will make the two programs run properly. The `NetFileXferServer.py` needs these .pem to implement TLS/SSL encryption security.

## Installing Wireshark

Install the Wireshark with this command in terminal:
>`sudo apt-get install wireshark`

After the line above, type:
> `sudo dpkg-reconfigure wireshark-common`

Select "yes" when prompted to the question.
Next, type this command below to add yourself to the "wireshark" group:

> `sudo usermod -a -G wireshark {username}`<br>
> <br>alternatively: `sudo adduser $USER wireshark`
> <br>ex: `sudo usermod -a -G wireshark vboxjem`

Before running wireshark, log out or restart your linux machine!

Finally, run the program in the terminal to start capturing the NetFileXfer programs:
> `wireshark`

For this program, you can select "any" when you run Wireshark to capture the packets when running the NetFileXfer programs in the terminal.

## Programming References
[SSL implementation in client and server side (asecuritysite)](https://asecuritysite.com/subjects/chapter107)
