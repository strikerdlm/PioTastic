**Meshtastic Python CLI Guide**
The python pip package installs a \"meshtastic\" command line executable\, which displays packets sent over the network as JSON and lets you see serial debugging information from the meshtastic devices\. This command is not run inside of python\, you run it from your operating system shell prompt directly\. If when you type \"meshtastic\" it doesn\'t find the command and you are using Windows\: Check that the python \"scripts\" directory is in your path\.
## \*\*Connection Arguments[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#connection-arguments)
### \*\*\-\-port PORT[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--port-port)
The port the Meshtastic device is connected to\, i\.e\. **`/dev/ttyUSB0`**\, **`/dev/cu.wchusbserial`**\, **`COM4`** etc\. if unspecified\, meshtastic will try to find it\. Important to use when multiple devices are connected to ensure you call the command for the correct device\.
This argument can also be specified as **`--serial`** or **`-s`**\.
Usage
```warp-runnable-command
meshtastic --port /dev/ttyUSB0 --infomeshtastic --port COM4 --infomeshtastic -s --info

```
### \*\*\-\-host HOST[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--host-host)
The hostname\/ipaddr of the device to connect to \(over TCP\)\. If a host is not provided\, the CLI will try to connect to **`localhost`**\.
This argument can also be specified as **`--tcp`** or **`-t`**\.
Usage
```warp-runnable-command
meshtastic --host meshtastic.local --infomeshtastic --host --info

```
### \*\*\-\-ble BLE[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--ble-ble)
Connect to a Meshtastic device using its BLE address or name\. This option allows for wireless communication with the device\, similar to how the **`--host`** option is used for TCP connections\. If an address is not provided\, meshtastic will try to find a compatible device that\'s paired\.
This argument can also be specified as **`-b`**\.
Usage
```warp-runnable-command
meshtastic --ble "device_name_or_address" --infomeshtastic -b --info

```
## \*\*Help \& Support Arguments[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#help--support-arguments)
### \*\*\-h or \-\-help[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#-h-or---help)
Shows a help message that describes the arguments\.
Usage
```warp-runnable-command
meshtastic -h

```
### \*\*\-\-version[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--version)
Show program\'s version number and exit\.
Usage
```warp-runnable-command
meshtastic --version

```
### \*\*\-\-support[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--support)
Print out info that would be helpful supporting any issues\.
Usage
```warp-runnable-command
meshtastic --support

```
## \*\*Optional Arguments[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#optional-arguments)
### \*\*\-\-export\-config[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--export-config)
Export the configuration of the device\. \(to be consumed by the \'\-\-configure\' command\)\.
To create to a file with the connected device\'s configuration\, this command\'s output must be piped to a yaml file\.
Usage
```warp-runnable-command
meshtastic --export-config > example_config.yaml

```
### \*\*\-\-configure[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--configure)
Configure radio using a yaml file\.
Usage
```warp-runnable-command
meshtastic --configure example_config.yaml

```
### \*\*\-\-seriallog SERIALLOG[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--seriallog-seriallog)
Logs device serial output to either \'stdout\'\, \'none\' or a filename to append to\. Defaults to \'stdout\' if no filename is specified\.
Usage
```warp-runnable-command
meshtastic --port /dev/ttyUSB0 --seriallogmeshtastic -t meshtastic.local --seriallog log.txt

```
### \*\*\-\-info[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--info)
Read and display the radio config information\.
Usage
```warp-runnable-command
meshtastic --port /dev/ttyUSB0 --info

```
### \*\*\-\-set\-canned\-message[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--set-canned-message)
Set the canned message plugin messages separated by pipes **`|`** \(up to 200 characters\)\.
Usage
```warp-runnable-command
meshtastic --set-canned-message "I need an alpinist!|Call Me|Roger Roger|Keep Calm|On my way"


```
### \*\*\-\-get\-canned\-message[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--get-canned-message)
Show the canned message plugin message\.
Usage
```warp-runnable-command
meshtastic --get-canned-message

```
### \*\*\-\-set\-ringtone RINGTONE[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--set-ringtone-ringtone)
Set the Notification Ringtone \(up to 230 characters\)\.
Usage
```warp-runnable-command
meshtastic --set-ringtone "LeisureSuit:d=16,o=6,b=56:f.5,f#.5,g.5,g#5,32a#5,f5,g#.5,a#.5,32f5,g#5,32a#5,g#5,8c#.,a#5,32c#,a5,a#.5,c#.,32a5,a#5,32c#,d#,8e,c#.,f.,f.,f.,f.,f,32e,d#,8d,a#.5,e,32f,e,32f,c#,d#.,c#"


```
### \*\*\-\-get\-ringtone[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--get-ringtone)
Show the stored ringtone\.
Usage
```warp-runnable-command
meshtastic --get-ringtone

```
### \*\*\-\-nodes[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--nodes)
Prints a node list in a pretty\, formatted table\.
Usage
```warp-runnable-command
meshtastic --nodes

```
### \*\*\-\-qr[\<u\>1](https://meshtastic.org/docs/software/python/cli/#user-content-fn-1)[​\<\/u\>\*\*](https://meshtastic.org/docs/software/python/cli/#--qr)
Displays the URL and QR code that corresponds to the current primary channel\.
Usage
```warp-runnable-command
meshtastic --qr

```
### \*\*\-\-qr\-all[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--qr-all)
Displays the URL and QR code that corresponds to all configured channels on the node\.
Usage
```warp-runnable-command
meshtastic --qr-all

```
### \*\*\-\-get \[config\_section\][<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--get-config_section)
Gets a preferences field\.
Configuration values are described in\: [**<u>Configuration</u>**](https://meshtastic.org/docs/configuration)\.
Usage
```warp-runnable-command
meshtastic --get lorameshtastic --get lora.region

```
To see all valid values\, pass an invalid value\, such as **`0`**\:
Usage
```warp-runnable-command
meshtastic --get 0

```
### \*\*\-\-set \[config\_section\]\.\[option\]  \[value\][<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--set-config_sectionoption-value)
Sets a preferences field\.
Configuration values are described in\: [**<u>Configuration</u>**](https://meshtastic.org/docs/configuration)\.
Usage
```warp-runnable-command
meshtastic --set lora.region Unset

```
### \*\*\-\-seturl SETURL[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--seturl-seturl)
Set the channel URL\, which contains LoRa configuration plus the configuration of channels\. Replaces your current configuration and channels completely\.
Usage
```warp-runnable-command
meshtastic --seturl https://www.meshtastic.org/c/GAMiIE67C6zsNmlWQ-KE1tKt0fRKFciHka-DShI6G7ElvGOiKgZzaGFyZWQ=


```
### \*\*\-\-pos\-fields POS\_FIELDS[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--pos-fields-pos_fields)
Configure position fields to send with positions\; can pass multiple values\. With 0 values\, list current settings\.
Usage
```warp-runnable-command
meshtastic --pos-fieldsmeshtastic --pos-fields ALTITUDE HEADING SPEED

```
### \*\*\-\-ch\-index CH\_INDEX[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--ch-index-ch_index)
Act on the specified channel index\. Applies to options that configure channels \(such as **`--ch-set`** and **`--ch-del`**\) as well as options that send messages to the mesh \(such as **`--sendtext`** and **`--traceroute`**\)\.
Usage
```warp-runnable-command
meshtastic --ch-index 1 --ch-disable

```
### \*\*\-\-ch\-add CH\_ADD[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--ch-add-ch_add)
Add a secondary channel\, you must specify a channel name\.
Incompatible with **`--ch-index`**\. If you pass **`--ch-add`**\, any subsequent **`--ch-set`** and other commands that use a channel will use the index of the newly\-added channel\.
Usage
```warp-runnable-command
meshtastic --ch-add testing-channel

```
### \*\*\-\-ch\-del[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--ch-del)
Delete the channel specified by **`--ch-index`**\.
Usage
```warp-runnable-command
meshtastic --ch-index 1 --ch-del

```
### \*\*\-\-ch\-enable \(deprecated\)[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--ch-enable-deprecated)
This option is deprecated\. Using **`--ch-add`** is preferred in order to ensure there are no gaps in the channel list\.
Enable the channel specified by **`--ch-index`**\.
Usage
```warp-runnable-command
meshtastic --ch-index 1 --ch-enable

```
### \*\*\-\-ch\-disable \(deprecated\)[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--ch-disable-deprecated)
This option is deprecated\. Using **`--ch-del`** is preferred in order to ensure there are no gaps in the channel list\.
Disable the channel specified by **`--ch-index`**\.
Usage
```warp-runnable-command
meshtastic --ch-index 1 --ch-disable

```
### \*\*\-\-ch\-set CH\_SET CH\_SET[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--ch-set-ch_set-ch_set)
Set a channel parameter on the channel specified by **`--ch-index`**\.
Usage
```warp-runnable-command
meshtastic --ch-set id 1234 --ch-index 0

```
### \*\*\-\-ch\-vlongslow[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--ch-vlongslow)
Change modem preset to **`VERY_LONG_SLOW`**\.
Usage
```warp-runnable-command
meshtastic --ch-vlongslow

```
### \*\*\-\-ch\-longslow[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--ch-longslow)
Change modem preset to **`LONG_SLOW`**\.
Usage
```warp-runnable-command
meshtastic --ch-longslow

```
### \*\*\-\-ch\-longfast[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--ch-longfast)
Change modem preset to \(the default\) **`LONG_FAST`**\.
Usage
```warp-runnable-command
meshtastic --ch-longfast

```
### \*\*\-\-ch\-medslow[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--ch-medslow)
Change modem preset to **`MEDIUM_SLOW`**\.
Usage
```warp-runnable-command
meshtastic --ch-medslow

```
### \*\*\-\-ch\-medfast[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--ch-medfast)
Change modem preset to **`MEDIUM_FAST`**\.
Usage
```warp-runnable-command
meshtastic --ch-medfast

```
### \*\*\-\-ch\-shortslow[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--ch-shortslow)
Change modem preset to **`SHORT_SLOW`**\.
Usage
```warp-runnable-command
meshtastic --ch-shortslow

```
### \*\*\-\-ch\-shortfast[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--ch-shortfast)
Change modem preset to **`SHORT_FAST`**\.
Usage
```warp-runnable-command
meshtastic --ch-shortfast

```
### \*\*\-\-set\-owner SET\_OWNER[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--set-owner-set_owner)
Set device owner name\, sometimes called the long name\.
Usage
```warp-runnable-command
meshtastic --set-owner "MeshyJohn"

```
### \*\*\-\-set\-owner\-short SET\_OWNER\_SHORT[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--set-owner-short-set_owner_short)
Set device owner short name \(4 characters max\)\.
Usage
```warp-runnable-command
meshtastic --set-owner-short "MJ"

```
### \*\*\-\-set\-ham SET\_HAM[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--set-ham-set_ham)
Set licensed Ham ID \(by setting the owner name\) and turn off encryption on the primary channel\.
To disable Ham mode\, use **`--set-owner`** and **`--set-owner-short`** to reset the owner names\, and use **`--seturl`** or **`--ch-set`** commands to configure channels with the name and encryption you wish them to have\. Or\, use **`--factory-reset`** to reset to default settings\.
Usage
```warp-runnable-command
meshtastic --set-ham KI1345

```
### \*\*\-\-dest DEST[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--dest-dest)
The destination node id for any sent commands\, if not passed to a command another way\. Used for [**<u>Remote Node Administration</u>**](https://meshtastic.org/docs/configuration/remote-admin/)\.
On many shells\, exclamation points trigger special behavior unless enclosed in single quotes\.
Usage
```warp-runnable-command
meshtastic --dest '!28979058' --set-owner "MeshyJohn"

```
### \*\*\-\-sendtext SENDTEXT[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--sendtext-sendtext)
Send a text message\. Can specify a channel index \(**`--ch-index`**\) and\/or a destination \(**`--dest`**\)\.
Usage
```warp-runnable-command
meshtastic --sendtext 'Hello Mesh!'meshtastic --ch-index 1 --sendtext 'Hello secondary channel!'


```
### \*\*\-\-traceroute TRACEROUTE[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--traceroute-traceroute)
Traceroute from connected node to a destination\. You need pass the destination ID as an argument\, and may pass **`--ch-index`** to specify a channel\. The node you are tracing must have the same channel configured\, and only nodes that share the channel will identify themselves within the response\. With recent enough firmware\, other nodes may be included as **`!ffffffff`** but not with their actual ID\.
Usage
```warp-runnable-command
meshtastic --traceroute '!ba4bf9d0'

```
### \*\*\-\-request\-telemetry[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--request-telemetry)
Request telemetry from a node\. You need to pass the destination ID as an argument with **`--dest`**\. For repeaters\, using the node\'s decimal ID may be more effective\, but a hexadecimal ID should work as well\.
Usage
```warp-runnable-command
meshtastic --request-telemetry --dest '!ba4bf9d0'meshtastic --request-telemetry --dest 1828779180

```
### \*\*\-\-request\-position[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--request-position)
Request position from a node\. You need to pass the destination ID as an argument with **`--dest`**\.
Usage
```warp-runnable-command
meshtastic --request-position --dest '!ba4bf9d0' --ch-index 1


```
### \*\*\-\-ack[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--ack)
Used in combination with **`--sendtext`** and other commands to wait for an acknowledgment\. Not all commands will be able to return an acknowledgment\. Best used for commands that specify a single destination node\.
Usage
```warp-runnable-command
meshtastic --sendtext 'Hello Mesh!' --dest '!28979058' --ack


```
### \*\*\-\-reboot[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--reboot)
Tell the node to reboot\.
Usage
```warp-runnable-command
meshtastic --reboot

```
### \*\*\-\-shutdown[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--shutdown)
Tell the node to shutdown\.
Usage
```warp-runnable-command
meshtastic --shutdown

```
### \*\*\-\-factory\-reset[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--factory-reset)
Tell the node to install the default config\.
Usage
```warp-runnable-command
meshtastic --factory-reset

```
### \*\*\-\-reset\-nodedb[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--reset-nodedb)
Tell the node to clear its list of nodes\.
Usage
```warp-runnable-command
meshtastic --reset-nodedb

```
### \*\*\-\-remove\-node NODE[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--remove-node-node)
Tell the node to remove the specified node from the NodeDB\.
Usage
```warp-runnable-command
meshtastic --remove-node '!48759737'

```
### \*\*\-\-reply[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--reply)
Listen for messages\. When one is received\, send a message to the primary channel repeating the message along with some information\.
Usage
```warp-runnable-command
meshtastic --reply

```
### \*\*\-\-no\-time[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--no-time)
Suppress sending the current time to the mesh on startup\. May improve reliability and startup time\.
Usage
```warp-runnable-command
meshtastic --port /dev/ttyUSB0 --no-time

```
### \*\*\-\-no\-nodes[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--no-nodes)
Instruct the node to not send nodeinfo from the NodeDB on startup\. Requires firmware of sufficient version\. Commands that use node information may behave unpredictably\, since that information will not be populated\, but this can improve efficiency for commands that don\'t\.
Usage
```warp-runnable-command
meshtastic --no-nodes --no-time --sendtext "Firing off a quick message"


```
### \*\*\-\-wait\-to\-disconnect WAIT\_TO\_DISCONNECT[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--wait-to-disconnect-wait_to_disconnect)
After performing whatever actions are specified by other options\, wait before disconnecting from the device\. Some devices will reboot when the serial connection disconnects\, so adding a wait time may improve reliability\. Defaults to 5 seconds if not provided\.
Usage
```warp-runnable-command
meshtastic --set lora.channel_num 20 --wait-to-disconnect 10


```
### \*\*\-\-setalt SETALT[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--setalt-setalt)
Set device altitude \(allows use without GPS\)\, and enables fixed position mode\.
Can only be used on locally\-connected nodes and not along with **`--dest`**\.
Usage
```warp-runnable-command
meshtastic --setalt 120

```
### \*\*\-\-setlat SETLAT[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--setlat-setlat)
Set device latitude \(allows use without GPS\)\, and enables fixed position mode\.
Can only be used on locally\-connected nodes and not along with **`--dest`**\.
Usage
```warp-runnable-command
meshtastic --setlat 25.2

```
### \*\*\-\-setlon SETLON[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--setlon-setlon)
Set device longitude \(allows use without GPS\)\, and enables fixed position mode\.
Can only be used on locally\-connected nodes and not along with **`--dest`**\.
Usage
```warp-runnable-command
meshtastic --setlon -16.8

```
### \*\*\-\-remove\-position[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--remove-position)
Clear the node\'s currently set fixed position and disable fixed position mode\.
Can only be used on locally\-connected nodes and not along with **`--dest`**\.
Usage
```warp-runnable-command
meshtastic --remove-position

```
### \*\*\-\-debug[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--debug)
Show API library debug log messages\.
Usage
```warp-runnable-command
meshtastic --debug --info

```
### \*\*\-\-listen[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--listen)
Stay open and listen to the stream of protocol buffer messages\. This option enables **`--debug`** even if it is not provided alongside this argument\.
Usage
```warp-runnable-command
meshtastic --listen

```
### \*\*\-\-test[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--test)
Run stress test against all connected Meshtastic devices\.
Usage
```warp-runnable-command
meshtastic --test

```
### \*\*\-\-ble\-scan[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--ble-scan)
Scan for available Meshtastic devices using BLE\. This command lists discoverable devices\, providing a convenient method to identify devices for connection via BLE\.
Usage
```warp-runnable-command
meshtastic --ble-scan

```
### \*\*\-\-noproto[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--noproto)
Don\'t start the API\, just function as a dumb serial terminal\. Useful for debugging because it doesn\'t count as a client\. Depends on a physically cabled serial connection\. It will connect but not display information over a network \(\-\-host\) or Bluetooth \(\-\-ble\) connection\.
Usage
```warp-runnable-command
meshtastic --noproto

```
## \*\*Remote Hardware arguments[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#remote-hardware-arguments)
### \*\*\-\-gpio\-wrb GPIO\_WRB GPIO\_WRB[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--gpio-wrb-gpio_wrb-gpio_wrb)
Set a particular GPIO \# to 1 or 0\.
Usage
```warp-runnable-command
meshtastic --port /dev/ttyUSB0 --gpio-wrb 4 1 --dest '!28979058'


```
### \*\*\-\-gpio\-rd GPIO\_RD[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--gpio-rd-gpio_rd)
Read from a GPIO mask\.
Usage
```warp-runnable-command
meshtastic --port /dev/ttyUSB0 --gpio-rd 0x10 --dest '!28979058'


```
### \*\*\-\-gpio\-watch GPIO\_WATCH[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--gpio-watch-gpio_watch)
Start watching a GPIO mask for changes\.
Usage
```warp-runnable-command
meshtastic --port /dev/ttyUSB0 --gpio-watch 0x10 --dest '!28979058'


```
## \*\*Tunnel arguments[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#tunnel-arguments)
### \*\*\-\-tunnel[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--tunnel)
Linux only\, very experimental\. Low bandwidth and low reliability\.
Create a TUN tunnel device for forwarding IP packets over the mesh\.
## \*\*\-\-subnet TUNNEL\_NET[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--subnet-tunnel_net)
Set the subnet for the local end of the tunnel established using **`--tunnel`**\.
\*\*Footnotes[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#footnote-label)The Meshtastic QR code \(or Channel URL\) allows users to quickly share channel and LoRa settings\, making it easy to configure multiple nodes with matching settings for communication\. Scanning a QR code applies all included channel settings and LoRa configuration settings\, so be sure to review what these settings include before proceeding\. Only scan QR codes from trusted sources\.**Meshtastic Python CLI Guide**
The python pip package installs a \"meshtastic\" command line executable\, which displays packets sent over the network as JSON and lets you see serial debugging information from the meshtastic devices\. This command is not run inside of python\, you run it from your operating system shell prompt directly\. If when you type \"meshtastic\" it doesn\'t find the command and you are using Windows\: Check that the python \"scripts\" directory is in your path\.
## \*\*Connection Arguments[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#connection-arguments)
### \*\*\-\-port PORT[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--port-port)
The port the Meshtastic device is connected to\, i\.e\. **`/dev/ttyUSB0`**\, **`/dev/cu.wchusbserial`**\, **`COM4`** etc\. if unspecified\, meshtastic will try to find it\. Important to use when multiple devices are connected to ensure you call the command for the correct device\.
This argument can also be specified as **`--serial`** or **`-s`**\.
Usage
```warp-runnable-command
meshtastic --port /dev/ttyUSB0 --infomeshtastic --port COM4 --infomeshtastic -s --info

```
### \*\*\-\-host HOST[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--host-host)
The hostname\/ipaddr of the device to connect to \(over TCP\)\. If a host is not provided\, the CLI will try to connect to **`localhost`**\.
This argument can also be specified as **`--tcp`** or **`-t`**\.
Usage
```warp-runnable-command
meshtastic --host meshtastic.local --infomeshtastic --host --info

```
### \*\*\-\-ble BLE[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--ble-ble)
Connect to a Meshtastic device using its BLE address or name\. This option allows for wireless communication with the device\, similar to how the **`--host`** option is used for TCP connections\. If an address is not provided\, meshtastic will try to find a compatible device that\'s paired\.
This argument can also be specified as **`-b`**\.
Usage
```warp-runnable-command
meshtastic --ble "device_name_or_address" --infomeshtastic -b --info

```
## \*\*Help \& Support Arguments[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#help--support-arguments)
### \*\*\-h or \-\-help[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#-h-or---help)
Shows a help message that describes the arguments\.
Usage
```warp-runnable-command
meshtastic -h

```
### \*\*\-\-version[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--version)
Show program\'s version number and exit\.
Usage
```warp-runnable-command
meshtastic --version

```
### \*\*\-\-support[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--support)
Print out info that would be helpful supporting any issues\.
Usage
```warp-runnable-command
meshtastic --support

```
## \*\*Optional Arguments[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#optional-arguments)
### \*\*\-\-export\-config[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--export-config)
Export the configuration of the device\. \(to be consumed by the \'\-\-configure\' command\)\.
To create to a file with the connected device\'s configuration\, this command\'s output must be piped to a yaml file\.
Usage
```warp-runnable-command
meshtastic --export-config > example_config.yaml

```
### \*\*\-\-configure[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--configure)
Configure radio using a yaml file\.
Usage
```warp-runnable-command
meshtastic --configure example_config.yaml

```
### \*\*\-\-seriallog SERIALLOG[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--seriallog-seriallog)
Logs device serial output to either \'stdout\'\, \'none\' or a filename to append to\. Defaults to \'stdout\' if no filename is specified\.
Usage
```warp-runnable-command
meshtastic --port /dev/ttyUSB0 --seriallogmeshtastic -t meshtastic.local --seriallog log.txt

```
### \*\*\-\-info[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--info)
Read and display the radio config information\.
Usage
```warp-runnable-command
meshtastic --port /dev/ttyUSB0 --info

```
### \*\*\-\-set\-canned\-message[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--set-canned-message)
Set the canned message plugin messages separated by pipes **`|`** \(up to 200 characters\)\.
Usage
```warp-runnable-command
meshtastic --set-canned-message "I need an alpinist!|Call Me|Roger Roger|Keep Calm|On my way"


```
### \*\*\-\-get\-canned\-message[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--get-canned-message)
Show the canned message plugin message\.
Usage
```warp-runnable-command
meshtastic --get-canned-message

```
### \*\*\-\-set\-ringtone RINGTONE[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--set-ringtone-ringtone)
Set the Notification Ringtone \(up to 230 characters\)\.
Usage
```warp-runnable-command
meshtastic --set-ringtone "LeisureSuit:d=16,o=6,b=56:f.5,f#.5,g.5,g#5,32a#5,f5,g#.5,a#.5,32f5,g#5,32a#5,g#5,8c#.,a#5,32c#,a5,a#.5,c#.,32a5,a#5,32c#,d#,8e,c#.,f.,f.,f.,f.,f,32e,d#,8d,a#.5,e,32f,e,32f,c#,d#.,c#"


```
### \*\*\-\-get\-ringtone[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--get-ringtone)
Show the stored ringtone\.
Usage
```warp-runnable-command
meshtastic --get-ringtone

```
### \*\*\-\-nodes[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--nodes)
Prints a node list in a pretty\, formatted table\.
Usage
```warp-runnable-command
meshtastic --nodes

```
### \*\*\-\-qr[\<u\>1](https://meshtastic.org/docs/software/python/cli/#user-content-fn-1)[​\<\/u\>\*\*](https://meshtastic.org/docs/software/python/cli/#--qr)
Displays the URL and QR code that corresponds to the current primary channel\.
Usage
```warp-runnable-command
meshtastic --qr

```
### \*\*\-\-qr\-all[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--qr-all)
Displays the URL and QR code that corresponds to all configured channels on the node\.
Usage
```warp-runnable-command
meshtastic --qr-all

```
### \*\*\-\-get \[config\_section\][<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--get-config_section)
Gets a preferences field\.
Configuration values are described in\: [**<u>Configuration</u>**](https://meshtastic.org/docs/configuration)\.
Usage
```warp-runnable-command
meshtastic --get lorameshtastic --get lora.region

```
To see all valid values\, pass an invalid value\, such as **`0`**\:
Usage
```warp-runnable-command
meshtastic --get 0

```
### \*\*\-\-set \[config\_section\]\.\[option\]  \[value\][<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--set-config_sectionoption-value)
Sets a preferences field\.
Configuration values are described in\: [**<u>Configuration</u>**](https://meshtastic.org/docs/configuration)\.
Usage
```warp-runnable-command
meshtastic --set lora.region Unset

```
### \*\*\-\-seturl SETURL[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--seturl-seturl)
Set the channel URL\, which contains LoRa configuration plus the configuration of channels\. Replaces your current configuration and channels completely\.
Usage
```warp-runnable-command
meshtastic --seturl https://www.meshtastic.org/c/GAMiIE67C6zsNmlWQ-KE1tKt0fRKFciHka-DShI6G7ElvGOiKgZzaGFyZWQ=


```
### \*\*\-\-pos\-fields POS\_FIELDS[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--pos-fields-pos_fields)
Configure position fields to send with positions\; can pass multiple values\. With 0 values\, list current settings\.
Usage
```warp-runnable-command
meshtastic --pos-fieldsmeshtastic --pos-fields ALTITUDE HEADING SPEED

```
### \*\*\-\-ch\-index CH\_INDEX[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--ch-index-ch_index)
Act on the specified channel index\. Applies to options that configure channels \(such as **`--ch-set`** and **`--ch-del`**\) as well as options that send messages to the mesh \(such as **`--sendtext`** and **`--traceroute`**\)\.
Usage
```warp-runnable-command
meshtastic --ch-index 1 --ch-disable

```
### \*\*\-\-ch\-add CH\_ADD[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--ch-add-ch_add)
Add a secondary channel\, you must specify a channel name\.
Incompatible with **`--ch-index`**\. If you pass **`--ch-add`**\, any subsequent **`--ch-set`** and other commands that use a channel will use the index of the newly\-added channel\.
Usage
```warp-runnable-command
meshtastic --ch-add testing-channel

```
### \*\*\-\-ch\-del[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--ch-del)
Delete the channel specified by **`--ch-index`**\.
Usage
```warp-runnable-command
meshtastic --ch-index 1 --ch-del

```
### \*\*\-\-ch\-enable \(deprecated\)[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--ch-enable-deprecated)
This option is deprecated\. Using **`--ch-add`** is preferred in order to ensure there are no gaps in the channel list\.
Enable the channel specified by **`--ch-index`**\.
Usage
```warp-runnable-command
meshtastic --ch-index 1 --ch-enable

```
### \*\*\-\-ch\-disable \(deprecated\)[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--ch-disable-deprecated)
This option is deprecated\. Using **`--ch-del`** is preferred in order to ensure there are no gaps in the channel list\.
Disable the channel specified by **`--ch-index`**\.
Usage
```warp-runnable-command
meshtastic --ch-index 1 --ch-disable

```
### \*\*\-\-ch\-set CH\_SET CH\_SET[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--ch-set-ch_set-ch_set)
Set a channel parameter on the channel specified by **`--ch-index`**\.
Usage
```warp-runnable-command
meshtastic --ch-set id 1234 --ch-index 0

```
### \*\*\-\-ch\-vlongslow[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--ch-vlongslow)
Change modem preset to **`VERY_LONG_SLOW`**\.
Usage
```warp-runnable-command
meshtastic --ch-vlongslow

```
### \*\*\-\-ch\-longslow[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--ch-longslow)
Change modem preset to **`LONG_SLOW`**\.
Usage
```warp-runnable-command
meshtastic --ch-longslow

```
### \*\*\-\-ch\-longfast[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--ch-longfast)
Change modem preset to \(the default\) **`LONG_FAST`**\.
Usage
```warp-runnable-command
meshtastic --ch-longfast

```
### \*\*\-\-ch\-medslow[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--ch-medslow)
Change modem preset to **`MEDIUM_SLOW`**\.
Usage
```warp-runnable-command
meshtastic --ch-medslow

```
### \*\*\-\-ch\-medfast[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--ch-medfast)
Change modem preset to **`MEDIUM_FAST`**\.
Usage
```warp-runnable-command
meshtastic --ch-medfast

```
### \*\*\-\-ch\-shortslow[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--ch-shortslow)
Change modem preset to **`SHORT_SLOW`**\.
Usage
```warp-runnable-command
meshtastic --ch-shortslow

```
### \*\*\-\-ch\-shortfast[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--ch-shortfast)
Change modem preset to **`SHORT_FAST`**\.
Usage
```warp-runnable-command
meshtastic --ch-shortfast

```
### \*\*\-\-set\-owner SET\_OWNER[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--set-owner-set_owner)
Set device owner name\, sometimes called the long name\.
Usage
```warp-runnable-command
meshtastic --set-owner "MeshyJohn"

```
### \*\*\-\-set\-owner\-short SET\_OWNER\_SHORT[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--set-owner-short-set_owner_short)
Set device owner short name \(4 characters max\)\.
Usage
```warp-runnable-command
meshtastic --set-owner-short "MJ"

```
### \*\*\-\-set\-ham SET\_HAM[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--set-ham-set_ham)
Set licensed Ham ID \(by setting the owner name\) and turn off encryption on the primary channel\.
To disable Ham mode\, use **`--set-owner`** and **`--set-owner-short`** to reset the owner names\, and use **`--seturl`** or **`--ch-set`** commands to configure channels with the name and encryption you wish them to have\. Or\, use **`--factory-reset`** to reset to default settings\.
Usage
```warp-runnable-command
meshtastic --set-ham KI1345

```
### \*\*\-\-dest DEST[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--dest-dest)
The destination node id for any sent commands\, if not passed to a command another way\. Used for [**<u>Remote Node Administration</u>**](https://meshtastic.org/docs/configuration/remote-admin/)\.
On many shells\, exclamation points trigger special behavior unless enclosed in single quotes\.
Usage
```warp-runnable-command
meshtastic --dest '!28979058' --set-owner "MeshyJohn"

```
### \*\*\-\-sendtext SENDTEXT[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--sendtext-sendtext)
Send a text message\. Can specify a channel index \(**`--ch-index`**\) and\/or a destination \(**`--dest`**\)\.
Usage
```warp-runnable-command
meshtastic --sendtext 'Hello Mesh!'meshtastic --ch-index 1 --sendtext 'Hello secondary channel!'


```
### \*\*\-\-traceroute TRACEROUTE[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--traceroute-traceroute)
Traceroute from connected node to a destination\. You need pass the destination ID as an argument\, and may pass **`--ch-index`** to specify a channel\. The node you are tracing must have the same channel configured\, and only nodes that share the channel will identify themselves within the response\. With recent enough firmware\, other nodes may be included as **`!ffffffff`** but not with their actual ID\.
Usage
```warp-runnable-command
meshtastic --traceroute '!ba4bf9d0'

```
### \*\*\-\-request\-telemetry[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--request-telemetry)
Request telemetry from a node\. You need to pass the destination ID as an argument with **`--dest`**\. For repeaters\, using the node\'s decimal ID may be more effective\, but a hexadecimal ID should work as well\.
Usage
```warp-runnable-command
meshtastic --request-telemetry --dest '!ba4bf9d0'meshtastic --request-telemetry --dest 1828779180

```
### \*\*\-\-request\-position[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--request-position)
Request position from a node\. You need to pass the destination ID as an argument with **`--dest`**\.
Usage
```warp-runnable-command
meshtastic --request-position --dest '!ba4bf9d0' --ch-index 1


```
### \*\*\-\-ack[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--ack)
Used in combination with **`--sendtext`** and other commands to wait for an acknowledgment\. Not all commands will be able to return an acknowledgment\. Best used for commands that specify a single destination node\.
Usage
```warp-runnable-command
meshtastic --sendtext 'Hello Mesh!' --dest '!28979058' --ack


```
### \*\*\-\-reboot[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--reboot)
Tell the node to reboot\.
Usage
```warp-runnable-command
meshtastic --reboot

```
### \*\*\-\-shutdown[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--shutdown)
Tell the node to shutdown\.
Usage
```warp-runnable-command
meshtastic --shutdown

```
### \*\*\-\-factory\-reset[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--factory-reset)
Tell the node to install the default config\.
Usage
```warp-runnable-command
meshtastic --factory-reset

```
### \*\*\-\-reset\-nodedb[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--reset-nodedb)
Tell the node to clear its list of nodes\.
Usage
```warp-runnable-command
meshtastic --reset-nodedb

```
### \*\*\-\-remove\-node NODE[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--remove-node-node)
Tell the node to remove the specified node from the NodeDB\.
Usage
```warp-runnable-command
meshtastic --remove-node '!48759737'

```
### \*\*\-\-reply[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--reply)
Listen for messages\. When one is received\, send a message to the primary channel repeating the message along with some information\.
Usage
```warp-runnable-command
meshtastic --reply

```
### \*\*\-\-no\-time[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--no-time)
Suppress sending the current time to the mesh on startup\. May improve reliability and startup time\.
Usage
```warp-runnable-command
meshtastic --port /dev/ttyUSB0 --no-time

```
### \*\*\-\-no\-nodes[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--no-nodes)
Instruct the node to not send nodeinfo from the NodeDB on startup\. Requires firmware of sufficient version\. Commands that use node information may behave unpredictably\, since that information will not be populated\, but this can improve efficiency for commands that don\'t\.
Usage
```warp-runnable-command
meshtastic --no-nodes --no-time --sendtext "Firing off a quick message"


```
### \*\*\-\-wait\-to\-disconnect WAIT\_TO\_DISCONNECT[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--wait-to-disconnect-wait_to_disconnect)
After performing whatever actions are specified by other options\, wait before disconnecting from the device\. Some devices will reboot when the serial connection disconnects\, so adding a wait time may improve reliability\. Defaults to 5 seconds if not provided\.
Usage
```warp-runnable-command
meshtastic --set lora.channel_num 20 --wait-to-disconnect 10


```
### \*\*\-\-setalt SETALT[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--setalt-setalt)
Set device altitude \(allows use without GPS\)\, and enables fixed position mode\.
Can only be used on locally\-connected nodes and not along with **`--dest`**\.
Usage
```warp-runnable-command
meshtastic --setalt 120

```
### \*\*\-\-setlat SETLAT[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--setlat-setlat)
Set device latitude \(allows use without GPS\)\, and enables fixed position mode\.
Can only be used on locally\-connected nodes and not along with **`--dest`**\.
Usage
```warp-runnable-command
meshtastic --setlat 25.2

```
### \*\*\-\-setlon SETLON[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--setlon-setlon)
Set device longitude \(allows use without GPS\)\, and enables fixed position mode\.
Can only be used on locally\-connected nodes and not along with **`--dest`**\.
Usage
```warp-runnable-command
meshtastic --setlon -16.8

```
### \*\*\-\-remove\-position[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--remove-position)
Clear the node\'s currently set fixed position and disable fixed position mode\.
Can only be used on locally\-connected nodes and not along with **`--dest`**\.
Usage
```warp-runnable-command
meshtastic --remove-position

```
### \*\*\-\-debug[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--debug)
Show API library debug log messages\.
Usage
```warp-runnable-command
meshtastic --debug --info

```
### \*\*\-\-listen[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--listen)
Stay open and listen to the stream of protocol buffer messages\. This option enables **`--debug`** even if it is not provided alongside this argument\.
Usage
```warp-runnable-command
meshtastic --listen

```
### \*\*\-\-test[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--test)
Run stress test against all connected Meshtastic devices\.
Usage
```warp-runnable-command
meshtastic --test

```
### \*\*\-\-ble\-scan[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--ble-scan)
Scan for available Meshtastic devices using BLE\. This command lists discoverable devices\, providing a convenient method to identify devices for connection via BLE\.
Usage
```warp-runnable-command
meshtastic --ble-scan

```
### \*\*\-\-noproto[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--noproto)
Don\'t start the API\, just function as a dumb serial terminal\. Useful for debugging because it doesn\'t count as a client\. Depends on a physically cabled serial connection\. It will connect but not display information over a network \(\-\-host\) or Bluetooth \(\-\-ble\) connection\.
Usage
```warp-runnable-command
meshtastic --noproto

```
## \*\*Remote Hardware arguments[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#remote-hardware-arguments)
### \*\*\-\-gpio\-wrb GPIO\_WRB GPIO\_WRB[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--gpio-wrb-gpio_wrb-gpio_wrb)
Set a particular GPIO \# to 1 or 0\.
Usage
```warp-runnable-command
meshtastic --port /dev/ttyUSB0 --gpio-wrb 4 1 --dest '!28979058'


```
### \*\*\-\-gpio\-rd GPIO\_RD[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--gpio-rd-gpio_rd)
Read from a GPIO mask\.
Usage
```warp-runnable-command
meshtastic --port /dev/ttyUSB0 --gpio-rd 0x10 --dest '!28979058'


```
### \*\*\-\-gpio\-watch GPIO\_WATCH[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--gpio-watch-gpio_watch)
Start watching a GPIO mask for changes\.
Usage
```warp-runnable-command
meshtastic --port /dev/ttyUSB0 --gpio-watch 0x10 --dest '!28979058'


```
## \*\*Tunnel arguments[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#tunnel-arguments)
### \*\*\-\-tunnel[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--tunnel)
Linux only\, very experimental\. Low bandwidth and low reliability\.
Create a TUN tunnel device for forwarding IP packets over the mesh\.
## \*\*\-\-subnet TUNNEL\_NET[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#--subnet-tunnel_net)
Set the subnet for the local end of the tunnel established using **`--tunnel`**\.
\*\*Footnotes[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/#footnote-label)The Meshtastic QR code \(or Channel URL\) allows users to quickly share channel and LoRa settings\, making it easy to configure multiple nodes with matching settings for communication\. Scanning a QR code applies all included channel settings and LoRa configuration settings\, so be sure to review what these settings include before proceeding\. Only scan QR codes from trusted sources\.

**Meshtastic Python CLI installation**
## \*\*Meshtastic Python Library[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/installation/#meshtastic-python-library)
This library provides a command\-line interface \(CLI\) for managing the user settings of Meshtastic nodes and provides an easy API for sending and receiving messages over mesh radios\. Events are delivered using a publish\-subscribe model\, and you can subscribe to only the message types you are interested in\.
The [**<u>Meshtastic\-python repo</u>**](https://github.com/meshtastic/Meshtastic-python) is an excellent source of information\. If you wish to view the code or contribute to the development of the Python library or the command\-line interface\, please visit the Meshtastic Python [**<u>GitHub page</u>**](https://github.com/meshtastic/Meshtastic-python)\.
### \*\*Prerequisites[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/installation/#prerequisites)
Before installing\, ensure that your system meets the following requirements\:
* **Serial Drivers**\: Your computer should have the required serial drivers installed for the [**<u>CP210X USB to UART bridge</u>**](https://www.silabs.com/products/development-tools/software/usb-to-uart-bridge-vcp-drivers) or the [**<u>CH9102</u>**](http://www.wch.cn/downloads/CH343SER_ZIP.html) \(for some newer boards\)\.
* **Python**\: Python 3 should be installed on your system\. Check with **`python3 -V`** and install it if necessary\.
* **pip**\: The Python package installer pip should be installed\. Check with **`pip3 -V`** and install it if necessary\.
After ensuring the requirements are met\, follow the installation instructions for your operating system in the tabbed section below\.
### \*\*Installation Instructions[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/installation/#installation-instructions)
To install the Meshtastic CLI\, select the tab for your operating system and follow the step\-by\-step instructions for installing via **`pip`**\. For Ubuntu only\, you can alternatively install the [**<u>Standalone version</u>**](https://meshtastic.org/docs/software/python/cli/installation/#standalone-installation-ubuntu-only) if you prefer\.

* Linux

* macOS

* Windows

* Termux for Android
Windows[**<u>​</u>**](https://meshtastic.org/docs/software/python/cli/installation/#windows)
* Check that your computer has the required serial drivers installed
    * Connect your Meshtastic device to your USB port
    * Open Device Manager
    * Under **`Ports (COM & LPT)`** you should see something like **`Silicon Labs CP210X USB to UART Bridge (COM5)`**
        * If there is no serial device shown that matches the device you are using\, please review our [**<u>Install Serial Drivers</u>**](https://meshtastic.org/docs/getting-started/serial-drivers/) page before proceeding\.
* Check that your computer has Python 3 installed\.
    * Use the command
```warp-runnable-command
py -V

```
    * If this does not return a version\, install [**<u>python</u>**](https://www.python.org/)
info
When installing Python\, make sure to select the option to \"Add Python to PATH\" or check the box that says \"Add Python to environment variables\"\. If you missed this during installation\, you can add Python to your system\'s PATH manually after installation\. Failing to do so may result in errors when trying to use Python or pip commands\.
* Pip is typically installed if you are using python 3 version \>\= 3\.4
    * Check that pip is installed using this command
```warp-runnable-command
pip3 -V

```
    * If this does not return a version\, install [**<u>pip</u>**](https://pip.pypa.io/en/stable/installing)
* Install pytap2
```warp-runnable-command
pip3 install --upgrade pytap2

```
* Install meshtastic\:
```warp-runnable-command
pip3 install --upgrade "meshtastic[cli]"

```
* \(the **`[cli]`** suffix installs a few optional dependencies that match older versions of the CLI\)
**You may need to close and re\-open the CLI\. The path variables may or may not update for the current session when installing\.**
### \*\*Standalone Installation \(Ubuntu only\)[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/installation/#standalone-installation-ubuntu-only)
1. Download the **`meshtastic_ubuntu`** executable from the [**<u>Releases</u>**](https://github.com/meshtastic/Meshtastic-python/releases) page\.
2. Run the following command to make the file executable and rename it **`meshtastic`**\:
```warp-runnable-command
chmod +x meshtastic_ubuntu && mv meshtastic_ubuntu meshtastic


```
3. To run the CLI\:
```warp-runnable-command
./meshtastic

```
tip
Copy \(or move\) this binary somewhere in your path\.

**Using the Meshtastic CLI**
This section covers using the \"meshtastic\" command line executable\, which displays packets sent over the network as JSON and lets you see serial debugging information from the Meshtastic devices\.
note
The **`meshtastic`** command is not run within python but is a script run from your operating system shell prompt\. When you type \"meshtastic\" and the prompt is unable to find the command in Windows\, check that the python \"scripts\" directory [**is in your path**](https://datatofish.com/add-python-to-windows-path)\.
## \*\*Viewing Serial Output[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/usage/#viewing-serial-output)
The **`--noproto`** command in the Meshtastic Python CLI is used to disable the API and function merely as a \"dumb serial terminal\.\" This mode of operation allows both the API and device functionalities to remain accessible for regular use\, while simultaneously providing a window into the raw serial output\. This feature can be particularly useful for debugging\, development\, or understanding the low\-level communication between devices\. Depends on a physically cabled serial connection\. It will connect but not display information over a network \(\-\-host\) or Bluetooth \(\-\-ble\) connection\.
Example Usage
```warp-runnable-command
user@host % meshtastic --noproto# You should see results similar to this:WARNING file:mesh_interface.py _sendToRadio line:681 Not sending packet because protocol use is disabled by noProtoConnected to radioWARNING file:mesh_interface.py _sendPacket line:531 Not sending packet because protocol use is disabled by noProtoINFO  | 18:38:04 711 [DeviceTelemetryModule] (Sending): air_util_tx=0.116361, channel_utilization=1.916667, battery_level=101, voltage=4.171000DEBUG | 18:38:04 711 [DeviceTelemetryModule] updateTelemetry LOCALDEBUG | 18:38:04 711 [DeviceTelemetryModule] Node status update: 2 online, 4 totalINFO  | 18:38:04 711 [DeviceTelemetryModule] Sending packet to phoneINFO  | 18:38:04 711 Telling client we have new packets 28


```
## \*\*Getting a list of User Preferences[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/usage/#getting-a-list-of-user-preferences)
You can get a list of user preferences by running \'\-\-get\' with an invalid attribute such as \'all\'\.
```warp-runnable-command
meshtastic --get all

```
## \*\*Changing settings[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/usage/#changing-settings)
You can also use this tool to set any of the device parameters which are stored in persistent storage\. For instance\, here\'s how to set the device to keep the Bluetooth link alive for eight hours \(any usage of the Bluetooth protocol from your phone will reset this timer\)
Expected Output
```warp-runnable-command
# You should see a result similar to this:mydir$ meshtastic --set power.wait_bluetooth_secs 28800Connected to radio...Setting power.wait_bluetooth_secs to 28800Writing modified preferences to device...

```
Or to set a node at a fixed position and never power up the GPS\.
```warp-runnable-command
meshtastic --setlat 25.2 --setlon -16.8 --setalt 120

```
Or to configure an ESP32 based board to join a Wifi network as a station\:
```warp-runnable-command
meshtastic --set network.wifi_ssid mywifissid --set network.wifi_psk mywifipsw --set network.wifi_enabled 1


```
note
For a full list of preferences which can be set \(and their documentation\) can be found in the [**protobufs**](https://buf.build/meshtastic/protobufs/docs/main:meshtastic#meshtastic.User)\.
### \*\*Changing channel settings[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/usage/#changing-channel-settings)
The channel settings can also be changed\, either by using a standard \(shareable\) meshtastic URL or you can set a particular channel parameter \(for advanced users\)\.
warning
Meshtastic encodes the radio channel and PSK in the channel\'s URL\. All nodes must connect to the channel again by using the URL provided after a change in this section by performing the **`--info`** switch\.
```warp-runnable-command
meshtastic --ch-set name mychan --ch-index 1 --info

```
You can even set the channel preshared key to a particular AES128 or AES256 sequence\.
```warp-runnable-command
meshtastic --ch-index 1 --ch-set psk 0x1a1a1a1a2b2b2b2b1a1a1a1a2b2b2b2b1a1a1a1a2b2b2b2b1a1a1a1a2b2b2b2b --info


```
Use **`--ch-set psk none --ch-index 0`** to turn off encryption\.
Use **`--ch-set psk random --ch-index 0`** to assign a new \(high quality\) random AES256 key to the primary channel \(similar to what the Android app does when making new channels\)\.
Use **`--ch-set psk default --ch-index 0`** to restore the standard \'default\' \(minimally secure\, because it is in the source code for anyone to read\) AES128 key\.
Use **`--ch-set psk base64:{key} --ch-index {index}`** to set the PSK of a channel to a known entity
All **`ch-set`** commands need to have the **`ch-index`** parameter specified\:
```warp-runnable-command
meshtastic --ch-index 1 --ch-set name mychan --info

```
### \*\*Ham radio support[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/usage/#ham-radio-support)
Meshtastic is designed to be used without a radio operator license\. If you do have a license you can set your operator ID and turn off encryption with\:
Expected Output
```warp-runnable-command
# You should see a result similar to this:mydir$ meshtastic --set-ham KI1345Connected to radioSetting Ham ID to KI1345 and turning off encryptionWriting modified channels to device

```
Toggling **`set-ham`** changes your device settings in the following ways\.
**Setting`set-ham` DefaultNormal Default**
**`IsLicensedtrue`**See [\*\*<u>User Config \- IsLicensed</u>](https://meshtastic.org/docs/configuration/radio/user/#is-licensed-ham)`LongName`***Your CallSign*See [\*\*<u>User Config \- LongName</u>](https://meshtastic.org/docs/configuration/radio/user/#long-name)`ShortName`***Abrv CallSign*See [\*\*<u>User Config \- ShortName</u>](https://meshtastic.org/docs/configuration/radio/user/#short-name)`PSK""`\*\*See [**<u>Channel Settings \- PSK</u>**](https://meshtastic.org/docs/software/python/cli/usage/#changing-the-preshared-key)
## \*\*Changing the preshared key[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/usage/#changing-the-preshared-key)
You can set the channel preshared key to a particular AES128 or AES256 sequence\.
```warp-runnable-command
meshtastic --ch-set psk 0x1a1a1a1a2b2b2b2b1a1a1a1a2b2b2b2b1a1a1a1a2b2b2b2b1a1a1a1a2b2b2b2b --info


```
Use \"\-\-ch\-set psk none\" to turn off encryption\.
Use \"\-\-ch\-set psk random\" will assign a new \(high quality\) random AES256 key to the primary channel \(similar to what the Android app does when making new channels\)\.
Use \"\-\-ch\-set psk default\" to restore the standard \'default\' \(minimally secure\, because it is in the source code for anyone to read\) AES128 key\.
All \"ch\-set\" commands will default to the primary channel at index 0\, but can be applied to other channels with the \"ch\-index\" parameter\.
## \*\*Utilizing BLE via the Python CLI[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/usage/#utilizing-ble-via-the-python-cli)
The Python CLI supports communicating with Meshtastic devices via Bluetooth Low Energy \(BLE\)\, in addition to the standard serial and TCP\/IP connections\. To use BLE\, you will need a Bluetooth adapter on your computer\.
### \*\*Scan for BLE Devices[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/usage/#scan-for-ble-devices)
First\, you can scan for available Meshtastic devices using\:
```warp-runnable-command
meshtastic --ble-scan

```
This will list all Meshtastic devices discoverable over BLE along with their addresses and names in the following format\:
```warp-runnable-command
Found: name='Meshtastic_1234' address='AA11BB22-CC33-DD44-EE55-FF6677889900'BLE scan finished


```
### \*\*Available Commands[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/usage/#available-commands)
Once you have the device address or name\, you can utilize it alongside your normal Python CLI commands like **`--info`**\, **`--nodes`**\, **`--export-config`**\, etc\. but with the **`--ble`** option to communicate via BLE rather than serial\.
You can use **either** the name or address to issue your commands\.
```warp-runnable-command
meshtastic --ble <name> --infomeshtastic --ble <address> --nodes

```
The initial time you use the **`--ble`** option for a specific device\, you will be prompted to enter the BLE PIN code \(as is normal with a client\)\. Once paired\, this step won\'t be required unless you forget the device\.
note
On Linux\, you may need to pair the BLE device using **`bluetoothctl`** before connecting\. This allows entering the required PIN for pairing\.
### \*\*Additional BLE Examples[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/usage/#additional-ble-examples)
Scan for devices and get info from the first one\:[**<u>​</u>**](https://meshtastic.org/docs/software/python/cli/usage/#scan-for-devices-and-get-info-from-the-first-one)
```warp-runnable-command
meshtastic --ble-scan# Sample output:# Found: name='Meshtastic_1234' address='AA11BB22-CC33-DD44-EE55-FF6677889900'# Found: name='Meshtastic_5678' address='FF00DD00-AA11-BB22-CC33-DD44EE5566FF'BLE scan finishedmeshtastic --ble AA11BB22-CC33-DD44-EE55-FF6677889900 --info


```
Connect to a named device and read the node list\:[**<u>​</u>**](https://meshtastic.org/docs/software/python/cli/usage/#connect-to-a-named-device-and-read-the-node-list)
```warp-runnable-command
meshtastic --ble Meshtastic_1234 --nodes

```
Export device config with \-\-export\-config[**<u>​</u>**](https://meshtastic.org/docs/software/python/cli/usage/#export-device-config-with---export-config)
```warp-runnable-command
meshtastic --ble Meshtastic_1234 --export-config > config.yaml


```
Send a command to a remote device using the \-\-dest option\:[**<u>​</u>**](https://meshtastic.org/docs/software/python/cli/usage/#send-a-command-to-a-remote-device-using-the---dest-option)
```warp-runnable-command
meshtastic --dest '!fe1932db4' --set device.is_managed false --ble Meshtastic_9abc


```
For debugging\, you can enable verbose BLE logging by adding the **`--debug`** flag\:[**<u>​</u>**](https://meshtastic.org/docs/software/python/cli/usage/#for-debugging-you-can-enable-verbose-ble-logging-by-adding-the---debug-flag)
```warp-runnable-command
meshtastic --ble AA11BB22-CC33-DD44-EE55-FF6677889900 --debug --info


```
## \*\*FAQ\/common problems[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/usage/#faqcommon-problems)
This is a collection of common questions and answers from our friendly forum\.
### \*\*Permission denied\: ‘\/dev\/ttyUSB0’[<u>​</u>\*\*](https://meshtastic.org/docs/software/python/cli/usage/#permission-denied-devttyusb0)
This indicates an OS permission problem for access by your user to the USB serial port\. Typically this is fixed by the following\.
```warp-runnable-command
sudo usermod -a -G dialout <username>

```
If adding your user to the dialout group does not work\, you can use the following command to find out which group to add your user to\. In this example \(from Arch Linux\) the group was \"uucp\"
```warp-runnable-command
❯ ls -al /dev/ttyACM0crw-rw---- 1 root uucp 166, 0 Jul 20 21:52 /dev/ttyACM0
```
**Meshtastic Site Planner**
The Meshtastic Site Planner is a open\-source web utility for predicting node range and coverage\. It can be found on site\.meshtastic\.org\, and the source code is maintained at [**<u>https\:\/\/github\.com\/meshtastic\/meshtastic\-site\-planner</u>**](https://github.com/meshtastic/meshtastic-site-planner)\.
## \*\*Getting Started[<u>​</u>\*\*](https://meshtastic.org/docs/software/site-planner/#getting-started)
1. Go to the [**<u>official version</u>**](https://site.meshtastic.org/) or run a development copy and open the tool in a web browser\.
2. In **`Site Parameters > Site / Transmitter`**\, enter a name for the site\, the geographic coordinates\, and the antenna height above ground\. Refer to the Meshtastic regional parameters \([**<u>https\:\/\/meshtastic\.org\/docs\/configuration\/region\-by\-country\/</u>**](https://meshtastic.org/docs/configuration/region-by-country/)\) and input the transmit power\, frequency\, and antenna gain for your device\.
3. In **`Site Parameters > Receiver`**\, enter the receiver sensitivity \(**`-130 dBm`** for the default **`LongFast`** channel\)\, the receiver height\, and the receiver antenna gain\.
4. In **`Site Parameters > Receiver`**\, enter the maximum range for the simulation in kilometers\. Selecting long ranges \(\> 50 kilometers\) will result in longer computation times\.
5. Press \"Run Simulation\.\" The coverage map will be displayed when the calculation completes\.
Multiple radio sites can be added to the simulation by repeating these steps\. The other adjustable parameters default to sensible choices for meshtastic radios\, but you can change them if your project uses different hardware\.
## \*\*Understanding Results[<u>​</u>\*\*](https://meshtastic.org/docs/software/site-planner/#understanding-results)
The Meshtastic Site Planner creates a color\-coded map of where your radio signal will reach\, given the terrain and simulation parameters\. The expected signal strength \(RSSI\) can be read from the colorbar\. Regions with a strong signal \(predicted RSSI \> \-110 dBm\) have a stronger chance of successfully receiving and sending signals\. In areas with a low RSSI \(\< 125 dBm\)\, obstacles may limit communication reliability\. You can adjust the signal cutoff threshold under **`Receiver > Sensitivity Limit`**\. Minimum signal thresholds depend on the radio chipset and presets\, and are approximately as follows\:
**PresetBandwidth \(kHz\)Spreading Factor \(SF\)Coding RateSensitivity \(dBm\)**
**ShortTurbo**50074\/5\-117**ShortFast**25074\/5\-121**ShortSlow**25084\/5\-124**MediumFast**25094\/5\-127**MediumSlow**250104\/5\-130**LongFast**125114\/5\-133**LongModerate**125114\/8\-136**LongSlow**125124\/8\-137
## \*\*Limitations[<u>​</u>\*\*](https://meshtastic.org/docs/software/site-planner/#limitations)
The Site Planner uses terrain data from the NASA SRTM \(Shuttle Radar Topography\) mission\. This elevation dataset is accurate to around 90 meters\, and does not account for obstructions such as buildings or trees\. You can estimate the effect of random obstructions by entering their average height in **`Environment > Clutter Height`**\. It is a good idea to always verify predictions from this tool using real\-world testing\.
**Python**
### \*\*Sending\/receiving messages on mosquitto server using python[<u>​</u>\*\*](https://meshtastic.org/docs/software/integrations/mqtt/mqtt-python/#sendingreceiving-messages-on-mosquitto-server-using-python)
Here is an example publish message in python \(run **`pip install paho-mqtt`** first\)\:
```warp-runnable-command
#!/usr/bin/env python3import paho.mqtt.client as mqttfrom random import uniformimport timeclient = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)client.connect('localhost')while True:    randNumber = uniform(20.0, 21.0)    client.publish("env/test/TEMPERATURE", randNumber)    print("Just published " + str(randNumber) + " to topic TEMPERATURE")    time.sleep(1)


```
Here is example subscribe in python\:
```warp-runnable-command
#!/usr/bin/env python3import paho.mqtt.client as pahodef on_message(mosq, obj, msg):    print("%-20s %d %s" % (msg.topic, msg.qos, msg.payload))    mosq.publish('pong', 'ack', 0)def on_publish(mosq, obj, mid, reason_codes, properties):    passif __name__ == '__main__':    client = paho.Client(paho.CallbackAPIVersion.VERSION2)    client.on_message = on_message    client.on_publish = on_publish    client.connect("localhost", 1883, 60)    client.subscribe("env/test/TEMPERATURE", 0)    while client.loop() == 0:        pass
```
**Meshtastic Python DevelopmentBuilding**
A python release consists of publishing the release to PyPi [**<u>https\:\/\/pypi\.org\/project\/meshtastic\/</u>**](https://pypi.org/project/meshtastic/) as well as producing single\-executable files that are downloadable from Github [**<u>https\:\/\/github\.com\/meshtastic\/Meshtastic\-python\/releases</u>**](https://github.com/meshtastic/Meshtastic-python/releases)\.
### \*\*Pre\-requisites[<u>​</u>\*\*](https://meshtastic.org/docs/development/python/building/#pre-requisites)
No pre\-requisites are needed locally to make a release\. All builds are done via Github Actions currently\.
To test\/validate\, you will need to run\:
```warp-runnable-command
pip3 install poetrypoetry install

```
Note\: we now use the [**<u>poetry</u>**](https://python-poetry.org/) package manager for building meshtastic\. If you were familiar with our older \'venv\' base instructions you can still access that mechanism by running \"poetry shell\" to open a shell with the \(automatically maintained\) virtual environment activated\.
This can be handy if you want to run the \"meshtastic\" command without installing the package globally\.
### \*\*Instructions[<u>​</u>\*\*](https://meshtastic.org/docs/development/python/building/#instructions)
* Update protobufs by running the \"Update protobufs\" workflow in Actions\: [**<u>https\:\/\/github\.com\/meshtastic\/Meshtastic\-python\/actions\/workflows\/update\_protobufs\.yml</u>**](https://github.com/meshtastic/Meshtastic-python/actions/workflows/update_protobufs.yml)
* run the \"smoke1\" test \(optional\)\:
connect one device to the serial port and run\:
```warp-runnable-command
poetry run pytest -m smoke1

```
* run unit tests\: **`poetry run pytest`** \(optional\)
* run bin\/test\-release\.sh \(optional\)
* Run the \"Make Release\" workflow in Actions\: [**<u>https\:\/\/github\.com\/meshtastic\/Meshtastic\-python\/actions\/workflows\/release\.yml</u>**](https://github.com/meshtastic/Meshtastic-python/actions/workflows/release.yml)
* After the \"Make Release\" is done\, go into Releases\: [**<u>https\:\/\/github\.com\/meshtastic\/Meshtastic\-python\/releases</u>**](https://github.com/meshtastic/Meshtastic-python/releases) There should be a draft\. Add the title\, update the \"What\'s Changed\" \(Tip\: Click on the \"Auto\-generate release notes\" button\.\)\. Uncheck the \"This is a pre\-release\" \(if applicable\)\.
note
You need permissions in the GitHub project to make a build
### \*\*Instructions \- automated[<u>​</u>\*\*](https://meshtastic.org/docs/development/python/building/#instructions---automated)
* Go to Actions \/ Make Release \/ Run Workflow [**<u>https\:\/\/github\.com\/meshtastic\/Meshtastic\-gui\-installer\/actions\/workflows\/release\.yml</u>**](https://github.com/meshtastic/Meshtastic-gui-installer/actions/workflows/release.yml)
* Draft \& Publish release [\*\*<u>https\:\/\/github\.com\/meshtastic\/Meshtastic\-gui\-installer\/releases</u>](https://github.com/meshtastic/Meshtastic-gui-installer/releases)Building\*\*
A python release consists of publishing the release to PyPi [**<u>https\:\/\/pypi\.org\/project\/meshtastic\/</u>**](https://pypi.org/project/meshtastic/) as well as producing single\-executable files that are downloadable from Github [**<u>https\:\/\/github\.com\/meshtastic\/Meshtastic\-python\/releases</u>**](https://github.com/meshtastic/Meshtastic-python/releases)\.
### \*\*Pre\-requisites[<u>​</u>\*\*](https://meshtastic.org/docs/development/python/building/#pre-requisites)
No pre\-requisites are needed locally to make a release\. All builds are done via Github Actions currently\.
To test\/validate\, you will need to run\:
```warp-runnable-command
pip3 install poetrypoetry install

```
Note\: we now use the [**<u>poetry</u>**](https://python-poetry.org/) package manager for building meshtastic\. If you were familiar with our older \'venv\' base instructions you can still access that mechanism by running \"poetry shell\" to open a shell with the \(automatically maintained\) virtual environment activated\.
This can be handy if you want to run the \"meshtastic\" command without installing the package globally\.
### \*\*Instructions[<u>​</u>\*\*](https://meshtastic.org/docs/development/python/building/#instructions)
* Update protobufs by running the \"Update protobufs\" workflow in Actions\: [**<u>https\:\/\/github\.com\/meshtastic\/Meshtastic\-python\/actions\/workflows\/update\_protobufs\.yml</u>**](https://github.com/meshtastic/Meshtastic-python/actions/workflows/update_protobufs.yml)
* run the \"smoke1\" test \(optional\)\:
connect one device to the serial port and run\:
```warp-runnable-command
poetry run pytest -m smoke1

```
* run unit tests\: **`poetry run pytest`** \(optional\)
* run bin\/test\-release\.sh \(optional\)
* Run the \"Make Release\" workflow in Actions\: [**<u>https\:\/\/github\.com\/meshtastic\/Meshtastic\-python\/actions\/workflows\/release\.yml</u>**](https://github.com/meshtastic/Meshtastic-python/actions/workflows/release.yml)
* After the \"Make Release\" is done\, go into Releases\: [**<u>https\:\/\/github\.com\/meshtastic\/Meshtastic\-python\/releases</u>**](https://github.com/meshtastic/Meshtastic-python/releases) There should be a draft\. Add the title\, update the \"What\'s Changed\" \(Tip\: Click on the \"Auto\-generate release notes\" button\.\)\. Uncheck the \"This is a pre\-release\" \(if applicable\)\.
note
You need permissions in the GitHub project to make a build
### \*\*Instructions \- automated[<u>​</u>\*\*](https://meshtastic.org/docs/development/python/building/#instructions---automated)
* Go to Actions \/ Make Release \/ Run Workflow [**<u>https\:\/\/github\.com\/meshtastic\/Meshtastic\-gui\-installer\/actions\/workflows\/release\.yml</u>**](https://github.com/meshtastic/Meshtastic-gui-installer/actions/workflows/release.yml)
* Draft \& Publish release [\*\*<u>https\:\/\/github\.com\/meshtastic\/Meshtastic\-gui\-installer\/releases</u>](https://github.com/meshtastic/Meshtastic-gui-installer/releases)Building\*\*
A python release consists of publishing the release to PyPi [**<u>https\:\/\/pypi\.org\/project\/meshtastic\/</u>**](https://pypi.org/project/meshtastic/) as well as producing single\-executable files that are downloadable from Github [**<u>https\:\/\/github\.com\/meshtastic\/Meshtastic\-python\/releases</u>**](https://github.com/meshtastic/Meshtastic-python/releases)\.
### \*\*Pre\-requisites[<u>​</u>\*\*](https://meshtastic.org/docs/development/python/building/#pre-requisites)
No pre\-requisites are needed locally to make a release\. All builds are done via Github Actions currently\.
To test\/validate\, you will need to run\:
```warp-runnable-command
pip3 install poetrypoetry install

```
Note\: we now use the [**<u>poetry</u>**](https://python-poetry.org/) package manager for building meshtastic\. If you were familiar with our older \'venv\' base instructions you can still access that mechanism by running \"poetry shell\" to open a shell with the \(automatically maintained\) virtual environment activated\.
This can be handy if you want to run the \"meshtastic\" command without installing the package globally\.
### \*\*Instructions[<u>​</u>\*\*](https://meshtastic.org/docs/development/python/building/#instructions)
* Update protobufs by running the \"Update protobufs\" workflow in Actions\: [**<u>https\:\/\/github\.com\/meshtastic\/Meshtastic\-python\/actions\/workflows\/update\_protobufs\.yml</u>**](https://github.com/meshtastic/Meshtastic-python/actions/workflows/update_protobufs.yml)
* run the \"smoke1\" test \(optional\)\:
connect one device to the serial port and run\:
```warp-runnable-command
poetry run pytest -m smoke1

```
* run unit tests\: **`poetry run pytest`** \(optional\)
* run bin\/test\-release\.sh \(optional\)
* Run the \"Make Release\" workflow in Actions\: [**<u>https\:\/\/github\.com\/meshtastic\/Meshtastic\-python\/actions\/workflows\/release\.yml</u>**](https://github.com/meshtastic/Meshtastic-python/actions/workflows/release.yml)
* After the \"Make Release\" is done\, go into Releases\: [**<u>https\:\/\/github\.com\/meshtastic\/Meshtastic\-python\/releases</u>**](https://github.com/meshtastic/Meshtastic-python/releases) There should be a draft\. Add the title\, update the \"What\'s Changed\" \(Tip\: Click on the \"Auto\-generate release notes\" button\.\)\. Uncheck the \"This is a pre\-release\" \(if applicable\)\.
note
You need permissions in the GitHub project to make a build
### \*\*Instructions \- automated[<u>​</u>\*\*](https://meshtastic.org/docs/development/python/building/#instructions---automated)
* Go to Actions \/ Make Release \/ Run Workflow [**<u>https\:\/\/github\.com\/meshtastic\/Meshtastic\-gui\-installer\/actions\/workflows\/release\.yml</u>**](https://github.com/meshtastic/Meshtastic-gui-installer/actions/workflows/release.yml)
* Draft \& Publish release [\*\*<u>https\:\/\/github\.com\/meshtastic\/Meshtastic\-gui\-installer\/releases</u>](https://github.com/meshtastic/Meshtastic-gui-installer/releases)Building\*\*
A python release consists of publishing the release to PyPi [**<u>https\:\/\/pypi\.org\/project\/meshtastic\/</u>**](https://pypi.org/project/meshtastic/) as well as producing single\-executable files that are downloadable from Github [**<u>https\:\/\/github\.com\/meshtastic\/Meshtastic\-python\/releases</u>**](https://github.com/meshtastic/Meshtastic-python/releases)\.
### \*\*Pre\-requisites[<u>​</u>\*\*](https://meshtastic.org/docs/development/python/building/#pre-requisites)
No pre\-requisites are needed locally to make a release\. All builds are done via Github Actions currently\.
To test\/validate\, you will need to run\:
```warp-runnable-command
pip3 install poetrypoetry install

```
Note\: we now use the [**<u>poetry</u>**](https://python-poetry.org/) package manager for building meshtastic\. If you were familiar with our older \'venv\' base instructions you can still access that mechanism by running \"poetry shell\" to open a shell with the \(automatically maintained\) virtual environment activated\.
This can be handy if you want to run the \"meshtastic\" command without installing the package globally\.
### \*\*Instructions[<u>​</u>\*\*](https://meshtastic.org/docs/development/python/building/#instructions)
* Update protobufs by running the \"Update protobufs\" workflow in Actions\: [**<u>https\:\/\/github\.com\/meshtastic\/Meshtastic\-python\/actions\/workflows\/update\_protobufs\.yml</u>**](https://github.com/meshtastic/Meshtastic-python/actions/workflows/update_protobufs.yml)
* run the \"smoke1\" test \(optional\)\:
connect one device to the serial port and run\:
```warp-runnable-command
poetry run pytest -m smoke1

```
* run unit tests\: **`poetry run pytest`** \(optional\)
* run bin\/test\-release\.sh \(optional\)
* Run the \"Make Release\" workflow in Actions\: [**<u>https\:\/\/github\.com\/meshtastic\/Meshtastic\-python\/actions\/workflows\/release\.yml</u>**](https://github.com/meshtastic/Meshtastic-python/actions/workflows/release.yml)
* After the \"Make Release\" is done\, go into Releases\: [**<u>https\:\/\/github\.com\/meshtastic\/Meshtastic\-python\/releases</u>**](https://github.com/meshtastic/Meshtastic-python/releases) There should be a draft\. Add the title\, update the \"What\'s Changed\" \(Tip\: Click on the \"Auto\-generate release notes\" button\.\)\. Uncheck the \"This is a pre\-release\" \(if applicable\)\.
note
You need permissions in the GitHub project to make a build
### \*\*Instructions \- automated[<u>​</u>\*\*](https://meshtastic.org/docs/development/python/building/#instructions---automated)
* Go to Actions \/ Make Release \/ Run Workflow [**<u>https\:\/\/github\.com\/meshtastic\/Meshtastic\-gui\-installer\/actions\/workflows\/release\.yml</u>**](https://github.com/meshtastic/Meshtastic-gui-installer/actions/workflows/release.yml)
* Draft \& Publish release [\*\*<u>https\:\/\/github\.com\/meshtastic\/Meshtastic\-gui\-installer\/releases</u>](https://github.com/meshtastic/Meshtastic-gui-installer/releases)Building\*\*
A python release consists of publishing the release to PyPi [**<u>https\:\/\/pypi\.org\/project\/meshtastic\/</u>**](https://pypi.org/project/meshtastic/) as well as producing single\-executable files that are downloadable from Github [**<u>https\:\/\/github\.com\/meshtastic\/Meshtastic\-python\/releases</u>**](https://github.com/meshtastic/Meshtastic-python/releases)\.
### \*\*Pre\-requisites[<u>​</u>\*\*](https://meshtastic.org/docs/development/python/building/#pre-requisites)
No pre\-requisites are needed locally to make a release\. All builds are done via Github Actions currently\.
To test\/validate\, you will need to run\:
```warp-runnable-command
pip3 install poetrypoetry install

```
Note\: we now use the [**<u>poetry</u>**](https://python-poetry.org/) package manager for building meshtastic\. If you were familiar with our older \'venv\' base instructions you can still access that mechanism by running \"poetry shell\" to open a shell with the \(automatically maintained\) virtual environment activated\.
This can be handy if you want to run the \"meshtastic\" command without installing the package globally\.
### \*\*Instructions[<u>​</u>\*\*](https://meshtastic.org/docs/development/python/building/#instructions)
* Update protobufs by running the \"Update protobufs\" workflow in Actions\: [**<u>https\:\/\/github\.com\/meshtastic\/Meshtastic\-python\/actions\/workflows\/update\_protobufs\.yml</u>**](https://github.com/meshtastic/Meshtastic-python/actions/workflows/update_protobufs.yml)
* run the \"smoke1\" test \(optional\)\:
connect one device to the serial port and run\:
```warp-runnable-command
poetry run pytest -m smoke1

```
* run unit tests\: **`poetry run pytest`** \(optional\)
* run bin\/test\-release\.sh \(optional\)
* Run the \"Make Release\" workflow in Actions\: [**<u>https\:\/\/github\.com\/meshtastic\/Meshtastic\-python\/actions\/workflows\/release\.yml</u>**](https://github.com/meshtastic/Meshtastic-python/actions/workflows/release.yml)
* After the \"Make Release\" is done\, go into Releases\: [**<u>https\:\/\/github\.com\/meshtastic\/Meshtastic\-python\/releases</u>**](https://github.com/meshtastic/Meshtastic-python/releases) There should be a draft\. Add the title\, update the \"What\'s Changed\" \(Tip\: Click on the \"Auto\-generate release notes\" button\.\)\. Uncheck the \"This is a pre\-release\" \(if applicable\)\.
note
You need permissions in the GitHub project to make a build
### \*\*Instructions \- automated[<u>​</u>\*\*](https://meshtastic.org/docs/development/python/building/#instructions---automated)
* Go to Actions \/ Make Release \/ Run Workflow [**<u>https\:\/\/github\.com\/meshtastic\/Meshtastic\-gui\-installer\/actions\/workflows\/release\.yml</u>**](https://github.com/meshtastic/Meshtastic-gui-installer/actions/workflows/release.yml)
* Draft \& Publish release [**<u>https\:\/\/github\.com\/meshtastic\/Meshtastic\-gui\-installer\/releases</u>**](https://github.com/meshtastic/Meshtastic-gui-installer/releases)
## \*\*A note to developers of this lib[<u>​</u>\*\*](https://meshtastic.org/docs/development/python/#a-note-to-developers-of-this-lib)
We use the Visual Studio Code \(VScode\) default python formatting conventions \(autopep8\)\. So if you use that IDE you should be able to use \"Format Document\" and not generate unrelated diffs\. If you use some other editor\, please do not change formatting on lines you have not changed yourself\.
### \*\*Building[<u>​</u>\*\*](https://meshtastic.org/docs/development/python/#building)
To build a new release
```warp-runnable-command
apt install pandocsudo pip3 install markdown pdoc3 webencodings pyparsing twine autopep8 pylint pytest pytest-cov


```
For development
```warp-runnable-command
poetry install --all-extras --with dev,powermon

```
### \*\*Linting[<u>​</u>\*\*](https://meshtastic.org/docs/development/python/#linting)
```warp-runnable-command
pylint meshtastic

```
### \*\*Testing[<u>​</u>\*\*](https://meshtastic.org/docs/development/python/#testing)
Install and run pytest[**<u>​</u>**](https://meshtastic.org/docs/development/python/#install-and-run-pytest)
* For more verbosity\, add **`-v`** or even **`-vv`**
```warp-runnable-command
pip3 install .pytest -vv

```
Run just unit tests
```warp-runnable-command
pytest# or (more verbosely)pytest -m unit# ormake

```
Run just integration tests
```warp-runnable-command
pytest -m int

```
Run the smoke test with only one device connected serially \(aka smoke1\)
```warp-runnable-command
pytest -m smoke1

```
caution
Running **`smoke1`** will reset values on the device\, including the region to 1 \(US\)\. Be sure to hit the reset button on the device after the test is completed\.
Run the smoke test with only two device connected serially \(aka smoke2\)
```warp-runnable-command
pytest -m smoke2

```
Run the wifi smoke test
```warp-runnable-command
pytest -m smokewifi

```
Run a specific test
```warp-runnable-command
pytest -msmoke1 meshtastic/tests/test_smoke1.py::test_smoke1_info# or to run a specific smoke2 testpytest -m smoke2 meshtastic/tests/test_smoke2.py::test_smoke2_info# or to run a specific smoke_wifi testpytest -m smokewifi meshtastic/tests/test_smoke_wifi.py::test_smokewifi_info


```
**Add another classification of tests such as `unit` or `smoke1`**
See [**<u>pytest\.ini</u>**](https://github.com/meshtastic/Meshtastic-python/blob/master/pytest.ini)\.
To see the unit test code coverage
```warp-runnable-command
pytest --cov=meshtastic# or if want html coverage reportpytest --cov-report html --cov=meshtastic# ormake cov

```
To see slowest unit tests\, you can run
```warp-runnable-command
pytest --durations=0# ormake slow

```
## \*\*Wire encoding[<u>​</u>\*\*](https://meshtastic.org/docs/development/python/#wire-encoding)
When sending protobuf packets over serial or TCP each packet is preceded by uint32 sent in network byte order \(big endian\)\. The upper 16 bits must be 0x94C3\. The lower 16 bits are packet length \(this encoding gives room to eventually allow quite large packets\)\.
Implementations validate length against the maximum possible size of a BLE packet \(our lowest common denominator\) of 512 bytes\. If the length provided is larger than that we assume the packet is corrupted and begin again looking for 0x4403 framing\.
The packets flowing towards the device are ToRadio protobufs\, the packets flowing from the device are FromRadio protobufs\. The 0x94C3 marker can be used as framing to \(eventually\) resync if packets are corrupted over the wire\.
Note\: the 0x94C3 framing was chosen to prevent confusion with the 7 bit ascii character set\. It also doesn\'t collide with any valid utf8 encoding\. This makes it a bit easier to start a device outputting regular debug output on its serial port and then only after it has received a valid packet from the PC\, turn off unencoded debug printing and switch to this packet encoding\.


**Building**
A python release consists of publishing the release to PyPi [**<u>https\:\/\/pypi\.org\/project\/meshtastic\/</u>**](https://pypi.org/project/meshtastic/) as well as producing single\-executable files that are downloadable from Github [**<u>https\:\/\/github\.com\/meshtastic\/Meshtastic\-python\/releases</u>**](https://github.com/meshtastic/Meshtastic-python/releases)\.
### \*\*Pre\-requisites[<u>​</u>\*\*](https://meshtastic.org/docs/development/python/building/#pre-requisites)
No pre\-requisites are needed locally to make a release\. All builds are done via Github Actions currently\.
To test\/validate\, you will need to run\:
```warp-runnable-command
pip3 install poetrypoetry install

```
Note\: we now use the [**<u>poetry</u>**](https://python-poetry.org/) package manager for building meshtastic\. If you were familiar with our older \'venv\' base instructions you can still access that mechanism by running \"poetry shell\" to open a shell with the \(automatically maintained\) virtual environment activated\.
This can be handy if you want to run the \"meshtastic\" command without installing the package globally\.
### \*\*Instructions[<u>​</u>\*\*](https://meshtastic.org/docs/development/python/building/#instructions)
* Update protobufs by running the \"Update protobufs\" workflow in Actions\: [**<u>https\:\/\/github\.com\/meshtastic\/Meshtastic\-python\/actions\/workflows\/update\_protobufs\.yml</u>**](https://github.com/meshtastic/Meshtastic-python/actions/workflows/update_protobufs.yml)
* run the \"smoke1\" test \(optional\)\:
connect one device to the serial port and run\:
```warp-runnable-command
poetry run pytest -m smoke1

```
* run unit tests\: **`poetry run pytest`** \(optional\)
* run bin\/test\-release\.sh \(optional\)
* Run the \"Make Release\" workflow in Actions\: [**<u>https\:\/\/github\.com\/meshtastic\/Meshtastic\-python\/actions\/workflows\/release\.yml</u>**](https://github.com/meshtastic/Meshtastic-python/actions/workflows/release.yml)
* After the \"Make Release\" is done\, go into Releases\: [**<u>https\:\/\/github\.com\/meshtastic\/Meshtastic\-python\/releases</u>**](https://github.com/meshtastic/Meshtastic-python/releases) There should be a draft\. Add the title\, update the \"What\'s Changed\" \(Tip\: Click on the \"Auto\-generate release notes\" button\.\)\. Uncheck the \"This is a pre\-release\" \(if applicable\)\.
note
You need permissions in the GitHub project to make a build
### \*\*Instructions \- automated[<u>​</u>\*\*](https://meshtastic.org/docs/development/python/building/#instructions---automated)
* Go to Actions \/ Make Release \/ Run Workflow [**<u>https\:\/\/github\.com\/meshtastic\/Meshtastic\-gui\-installer\/actions\/workflows\/release\.yml</u>**](https://github.com/meshtastic/Meshtastic-gui-installer/actions/workflows/release.yml)
* Draft \& Publish release [**<u>https\:\/\/github\.com\/meshtastic\/Meshtastic\-gui\-installer\/releases</u>**](https://github.com/meshtastic/Meshtastic-gui-installer/releases)

**Using the Meshtastic Python Library**An example using Python 3 code to send a message to the mesh\, get and set a radio configuration preference\:*`import* meshtastic*import* meshtastic.serial_interface*# By default will try to find a meshtastic device,# otherwise provide a device path like /dev/ttyUSB0*interface = meshtastic.serial_interface.SerialInterface()*# or something like this# interface = meshtastic.serial_interface.SerialInterface(devPath='/dev/cu.usbmodem53230050571')# or sendData to send binary data, see documentations for other options.*interface.sendText("hello mesh")ourNode = interface.getNode('^local')*print*(f'Our node preferences:{ourNode.localConfig}')*# update a valueprint*('Changing a preference...')ourNode.localConfig.position.gps_update_interval = 60*print*(f'Our node preferences now:{ourNode.localConfig}')ourNode.writeConfig("position")interface.close()`Another example using Python 3 code to send a message to the mesh when WiFi is enabled\:*`import* time*import* meshtastic*import* meshtastic.tcp_interface*from* pubsub *import* pub*def* onReceive(packet, interface): *# called when a packet arrives*    *print*(f"Received: {packet}")*def* onConnection(interface, topic=pub.AUTO_TOPIC): *# called when we (re)connect to the radio*    *# defaults to broadcast, specify a destination ID if you wish*    interface.sendText("hello mesh")pub.subscribe(onReceive, "meshtastic.receive")pub.subscribe(onConnection, "meshtastic.connection.established")interface = meshtastic.tcp_interface.TCPInterface(hostname='192.168.68.74')*while* True:    time.sleep(1000)interface.close()`Note\: Be sure to change the IP address in the code above to a valid IP address for your setup\.For the rough notes\/implementation plan see [**<u>TODO</u>**](https://github.com/meshtastic/python/blob/master/TODO.md)\. See the API for full details of how to use the library\.**A note to developers of this lib[<u>​</u>\*\*](https://meshtastic.org/docs/development/python/library/#a-note-to-developers-of-this-lib)We use the visual\-studio\-code default python formatting conventions \(autopep8\)\. So if you use that IDE you should be able to use \"Format Document\" and not generate unrelated diffs\. If you use some other editor\, please don\'t change formatting on lines you haven\'t changed\.If you need to build a new release you\'ll need\:**`Command**apt install pandocsudo pip3 install markdown pandoc webencodings pyparsing twine autopep`
apt install pandoc
sudo pip3 install markdown pandoc webencodings pyparsing twine autopep8
