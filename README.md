#REF

Online video streaming and Internet of Things (IoT) are becoming the main consumers of future networks, generating high throughput and highly dynamic traffic from large numbers of heterogeneous user devices. This places significant pressure on the underlying networks and deteriorates performance, efficiency and fairness. In order to address this issue, future networks must incorporate contextual network designs that recognize application and user-level requirements. However, new designs of network management components such as resource provisioning models are often tested within simulation environments which lack subtleties in how network protocols and relevant specifications are executed by network equipment in practice. This paper contributes the design and operational guidelines for an software-defined networking (SDN) experimentation framework (REF), which enables rapid evaluation of contextual networking designs using real network infrastructures. A use case study of a QoE-aware resource allocation model demonstrates the effectiveness of REF in facilitating design and validation of SDN-assisted networking.

#Utility model (UFair)

This is glues together the various elements. It includes both my integration code and Mu's QoE code, and can be found in the /UFair folder. The code to run is the /UFair/integration.py script. This will do the talking between the OpenFlow controller, Mu's QoE code and the REF framework. Try python integration.py -h to check out the parameters you can pass. To install the required packages, run pip install -r requirements.txt; that should install everything.

I've also included the config file used in the experiments (/UFair/config.json). It's basically a tree structure, describing the nodes (hosts, servers and switches) and the connections between them (the edges). The config is fairly self explanatory, but is rather tedious to build.

The /UFair/integration.py code has been documented pretty well, so it should be relatively easy to modify it for new Utility models.
