#REF

Online video streaming and Internet of Things (IoT) are becoming the main consumers of future networks, generating high throughput and highly dynamic traffic from large numbers of heterogeneous user devices. This places significant pressure on the underlying networks and deteriorates performance, efficiency and fairness. In order to address this issue, future networks must incorporate contextual network designs that recognize application and user-level requirements. However, new designs of network management components such as resource provisioning models are often tested within simulation environments which lack subtleties in how network protocols and relevant specifications are executed by network equipment in practice. This paper contributes the design and operational guidelines for an software-defined networking (SDN) experimentation framework (REF), which enables rapid evaluation of contextual networking designs using real network infrastructures. A use case study of a QoE-aware resource allocation model demonstrates the effectiveness of REF in facilitating design and validation of SDN-assisted networking.

#Utility model (UFair)

This is glues together the various elements. It includes both my integration code and Mu's QoE code, and can be found in the /UFair folder. The code to run is the /UFair/integration.py script. This will do the talking between the OpenFlow controller, Mu's QoE code and the REF framework. Try python integration.py -h to check out the parameters you can pass. To install the required packages, run pip install -r requirements.txt; that should install everything.

I've also included the config file used in the experiments (/UFair/config.json). It's basically a tree structure, describing the nodes (hosts, servers and switches) and the connections between them (the edges). The config is fairly self explanatory, but is rather tedious to build.

The /UFair/integration.py code has been documented pretty well, so it should be relatively easy to modify it for new Utility models.


#OpenFlow Bandwidth (OpenFlow controller)

The modified Ryu controller used in our experiments can be found in the /openflow_bandwidth folder.
A modification of a the ryu (http://osrg.github.io/ryu/) simple learning switch controller app to report and enforce bandwidth. Reporting by monotring the maximum passive throughput and enforcing using OpenFlow meters, both on a per port and per flow basis. The controller runs a JSON-RPC server for interfacing.

#Scootplayer

An experimental MPEG-DASH request engine with support for accurate logging. This is used on the clients for the QoE usecase.

#Patch Controller

This is a simple bridge SDN controller that rate-limits on a per port basis. This is only used when the target OpenFlow hardware does not support metering on muliple tables within a single pipeline.

#Tools

There is a number of additional scripts I used in the experimentation. For example, the /tools/reboot.sh script is used to reboot all the nodes via the nova interface. It could be used again (assuming we naming the hosts and servers the same). This naming shouldn't be an issue if we use the /tools/specmuall.py script in conjunction with Nic's ministack tools. This will recreate the exact same configuration of VMs and networks that we used in the experiment. The only think missing is the configuration of the HP switches and the VLAN trickery used to ensure VMs appear on particular ports on each of the virtual switches present on the physical HP switch.

There is two bash scripts used during the experiments. These were run simultaneously on each of the VMs using cluster SSH. The /tools/pre.sh script was run before experiments started and basically ensured that there was connectivity between each of the hosts and the server. It prints a nice green message if there is, a big red [FAIL] if not. This helped debug connectivity issued before even before we started. The /tools/go.sh was run in a similar manner ()using cluster SSH) to start the tests. The one included is for the background traffic generation using wget; evidently, it will different on the hosts playing video (I forgot to retrieve that one, but it basically started Scootplayer pointing at the server and playing the desired version of Big Buck Bunny). I just called it the same so that you could simply hit $ ./go.sh and start the damned thing!

An alternative to cssh was created because it had a tendency to close sessions or fail to open some. The experiments can be ran using cluster command simple RPC program which contains scripts specific to this experiment. The server is already installed and running on the clients. (Included in the REF repository as /cluster_command)

#Samples

I included a sample output from the integration code in /samples/debug.log. This is basically so that you know what the output will be like. This is also what Mu needs to plot. I also included the /samples/history.txt which is a dump of the bash history. It should give you an idea of what I was doing to run the experiment (and test things earlier on).

#Publications
To be updated

