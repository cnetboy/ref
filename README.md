#Rapid Experimentation Framework (REF)

Online video streaming and Internet of Things (IoT) are becoming the main consumers of future networks, generating high throughput and highly dynamic traffic from large numbers of heterogeneous user devices. This places significant pressure on the underlying networks and deteriorates performance, efficiency and fairness. In order to address this issue, future networks must incorporate contextual network designs that recognize application and user-level requirements. However, new designs of network management components such as resource provisioning models are often tested within simulation environments which lack subtleties in how network protocols and relevant specifications are executed by network equipment in practice. This paper contributes the design and operational guidelines for an software-defined networking (SDN) experimentation framework (REF), which enables rapid evaluation of contextual networking designs using real network infrastructures. A use case study of a QoE-aware resource allocation model demonstrates the effectiveness of REF in facilitating design and validation of SDN-assisted networking.


##Getting started
In order to get started using REF, a few dependencies are required. Infrastructure control, client automation, and the REF controller

###Infrastructure
Using MiniStack with OpenStack to automate VM creation and environment cleanup at scale.
Visit the readme here:
https://github.com/lyndon160/REF/tree/master/ministack


###Client automation
Use cluster command to automate your clients across the network.
Visit the readme here:
https://github.com/lyndon160/REF/tree/master/cluster_command

TODO

###REF controller
The REF controller is a modified version of the Ryu controller (http://osrg.github.io/ryu/) , it can be found in the /openflow_bandwidth folder. The applciation supports the basic forwarding applications available in Ryu and offers control of the network through an RPC intereface. It reports context in the network by monitoring all flows, meters and ports, it also keeps a track of the maximum throughput seen on the switch and on any single flow, port, or meter. The controller runs a JSON-RPC server for interfacing (see below for API). 

Install depedencies. Python, Python-pip, and the Ryu controller.

Next, to install the REF controller clone this repository and change directory to bandwidth_control/:

`% git clone http://github.com/lyndon160/REF`

Assuming the dependencies are correctly installed, you can run the controller with:

`% ryu-manager bandwidth_control_simple_switch_13.py`

###Creating and running your first application

Copy the sample skeleteon program provided in this repository under samples (samples/skeleton.py).

Run bandwidth_control_simple_switch_13.py as a Ryu app

`% ryu-manager bandwidth_control_simple_switch_13.py`

Make sure that any switches you have are configure to point to use a controller at the IP address which you're running bandwidth_control_simple_switch_13.py.

By default the RPC server is running on `http://localhost:4000/jsonrpc`

Now run your REF application (your utility application)

`% python ./my_REF_app.py`

The default application maintains a periodic state-transfer with the controller. In this simple example, the total bandwidth observed by all switches on the network is reported.

For other features, look at the API available on the JSON RPC server's interface (see below).

## JSON RPC interface
The JSON-RPC server is a HTTP server.
The following examples would be used to develop a python application using the python-jspnrpc library (https://pypi.python.org/pypi/python-jsonrpc), but procedures can be called using any JSON-RPC method. (I think)

Install 

`% pip install python-jsonrpc`

Import

`import pyjsonrpc`

Connection

`http_client = pyjsonrpc.HttpClient(url = "http://localhost:4000/jsonrpc")`

Procedure calling. 

```
# Direct call
result = http_client.call("<procedure>", arg1, arg2)

# Use the *method* name as *attribute* name
result = http_client.procedure(arg1, arg2)

# Notifcations send messages to the serevr without reply
http_client.notify("<procedure>", arg1, arg2)
```

<h3> Procedures </h3>

<b> report_port </b>
<br>Reports the maximum seen throughput of a specific port on a specific switch.
<br>Params: `[<switch_id>, <port_no>]` 
<br>Result: `[upload B/s, download B/s]`

```
--> {"jsonrpc": "2.0", "method": "report_port", "params": [<switch_id>, <port_no>], "id": 1}
<-- {"jsonrpc": "2.0", "result": [<upload B/s>, <download B/s>], "id": 1}
```

<b> report_flow -  Not implemented </b>
<br>Reports the throughout of a specific flow on a specific switch.
<br>Params: `[<switch_id>, <flow_id>]`
<br>Result: `<B/s>` 

<b> report_switch_ports </b>
<br>Reports the throughput of all ports on a specific switch.
<br>Params: `<switch_id>`
<br>Result: JSON formatted port list
```
{
  <port_no>:[<upload B/s>, <download B/s>],
  ...
  <port_no>:[<upload B/s>, <download B/s>]
}
```

<b> report_switch_flows - Not implemented </b>
<br>Reports the througput of all flows on a specific switch.
<br>Params: `<switch_id>`
<br>Result: JSON formatted flow list
```
{
  <flow_id>:<B/s>,
  ...
  <flow_id>:<B/s>
}
```

<b> report_all_ports </b>
<br>Report the throughput of all ports on all switches under the control of the controller.
<br>Result: JSON formatted switch & port list
```
{
  <switch_id>:{
    <port_no>:[<upload B/s>, download B/s],
    ...
    <port_no>:[<upload B/s>, download B/s]
  },
  ...
  <switch_id>:{
    <port_no>:[<upload B/s>, <download B/s>],
    ...
    <port_no>:[<upload B/s>, <download B/s>]
  }
}
```

<b> report_all_flows </b>
<br>Report the throughput of all flows on all switches under the control of the controller.
<br>Result: JSON formatted switch & flow list

```
{
  <switch_id>:{
    <flow_id>:<B/s>,
    ...
    <flow_id>:<B/s>
  },
  ...
  <switch_id>:{
    <flow_id>:<B/s>,
    ...
    <flow_id>:<B/s>
  }
}
```

<b> reset_port </b> - Notification
<br>Resets the throughput of a specific port. To be recalculated.
<br>Params: `[<switch_id>, <port_no>]`

<b> reset_flow </b> - Notification - <b> Not implemented </b>
<br>Resets the throughput of a specific flow. To be recalculated.
<br>Params: `[<switch_id>, <flow_id>]`

<b> reset_switch_ports </b> - Notification
<br>Resets all recorder throughputs of all ports on a specific switch.
<br>Params: `<switch_id>`

<b> reset_switch_flows </b> - Notification
<br>Resets all recorder throughputs of all ports on a specific switch.
<br>Params: `<switch_id>`

<b> reset_all_ports </b> - Notification
<br>Resets all recorder throughputs of all ports on all swtiches under the control of the controller.

<b> reset_all_flows </b> - Notification
<br>Resets all recorder throughputs of all flows on all swtiches under the control of the controller.

<b> Enforce procedures in progress </b>

<b> enforce_port_outbound </b> - Notification
<br>Enforces an outbound bandwidth restriction on a specific port. Any previous enforcements will be replaced.
<br>Params: `[<switch_id>, <port_no>, <speed B/s>]`

<b> enforce_port_inbound </b> - Notification
<br>Enforces an inbound bandwidth restriction on a specific port. Any previous enforcements will be replaced.
<br>Params: `[<switch_id>, <port_no>, <speed B/s>]`

<b> enforce_flow </b> - Notification -
<br>Enforces a bandwidth restricion on an existing flow. Any previous enforcements will be replaced.
<br>Params:`[<switch_id>, <flow_id>]`

<b> enfore_service </b>
<br>Enforces a bandwith restricting on a service donated by the source and destination address pair.
<br>Params: `[<switch_id>, <src_addr>, <dst_addr>, <speed B/s>]`


<b> block_flow </b>
<br>Blocks a flow for a set duration on the specified switch.
<br>Params: `[<switch_id>, <src_addr>, <dst_addr>, <duration seconds>]`


<h2>CLI</h2>
<b> report_throughput.py </b> -

Show everything

`% python report_througput.py -a`

Show all ports on a switch

`% python report_throughput.py -s <switch_id>`

Show specifc port on a switch

`% python report_throughput.py -s <switch_id> -p <port_no>`

<b> enforce_throughput_port.py </b>

`% python enforce_throughput_port.py <switch_id> <port_no> <speed B/s>`

<b> enforce_throughput_service.py </b>

`% python enforce_throughput_service.py <switch_id> <src_ip> <dst_ip> <speed B/s>`


<b> block_flow.py </b>

`% python block flow.py <switch_id> <src_ip> <dst_ip> <duration seconds>`

##Scootplayer (Tool for usecase)

An experimental MPEG-DASH request engine with support for accurate logging. This is used on the clients for the QoE usecase.

##Patch Controller

This is a simple bridge SDN controller that rate-limits on a per port basis. This is only used when the target OpenFlow hardware does not support metering on muliple tables within a single pipeline.

##Tools

There is a number of additional scripts I used in the experimentation. For example, the /tools/reboot.sh script is used to reboot all the nodes via the nova interface. It could be used again (assuming we naming the hosts and servers the same). This naming shouldn't be an issue if we use the /tools/specmuall.py script in conjunction with Nic's ministack tools. This will recreate the exact same configuration of VMs and networks that we used in the experiment. The only think missing is the configuration of the HP switches and the VLAN trickery used to ensure VMs appear on particular ports on each of the virtual switches present on the physical HP switch.

There is two bash scripts used during the experiments. These were run simultaneously on each of the VMs using cluster SSH. The /tools/pre.sh script was run before experiments started and basically ensured that there was connectivity between each of the hosts and the server. It prints a nice green message if there is, a big red [FAIL] if not. This helped debug connectivity issued before even before we started. The /tools/go.sh was run in a similar manner ()using cluster SSH) to start the tests. The one included is for the background traffic generation using wget; evidently, it will different on the hosts playing video (I forgot to retrieve that one, but it basically started Scootplayer pointing at the server and playing the desired version of Big Buck Bunny). I just called it the same so that you could simply hit $ ./go.sh and start the damned thing!

An alternative to cssh was created because it had a tendency to close sessions or fail to open some. The experiments can be ran using cluster command simple RPC program which contains scripts specific to this experiment. The server is already installed and running on the clients. (Included in the REF repository as /cluster_command)

##Samples

I included a sample output from the integration code in /samples/debug.log. This is basically so that you know what the output will be like. This data can then be transformed and plotted. The /samples/history.txt file is a dump of the bash history, it shows as an example on how to run the experiment.

##Utility model 1 (UFair. Example usecase 1)

This glues together the various elements. It includes both my integration code and Mu's QoE code, and can be found in the /UFair folder. The code to run is the /UFair/integration.py script. This will do the talking between the OpenFlow controller, Mu's QoE code and the REF framework. Try python integration.py -h to check out the parameters you can pass. To install the required packages, run pip install -r requirements.txt; that should install everything.

The configuration file used in the experiments (/UFair/config.json) is a tree structure, describing the nodes (hosts, servers and switches) and the connections between them (the edges). The config is fairly self explanatory, but is rather tedious to build.

##Utility model 2 (Smart-ACL. Example usecase 2)
This uses the REF framework to get information about the throughput of all current flows in the network. Then using a whitelist, it determines how much bandwidth each node in the network should be delegated. Further more, it uses infromations about meters from REF including the drop rate to determine whether an attack is taking place, with this information it can decide if it wants to block the flow or not. This is highly dependant on the amount of available bandwidth.
https://github.com/lyndon160/Smart-ACL

##Publications
UFair paper published available to be read.
Smart-ACL currently in submission.
REF paper currently in submission.
