# Iris Seika Module

An interface module for Seika.io and Iris to automatically enrich IOCs with Seika.io insight.  
**Module type** : ``Processor``  
**Min IRIS version required** : ``> 1.4.0`` 

The module is preinstalled by default on IRIS. For a manual installation please see the Installation section of this readme.

## Configuration 
Please refer to the [IRIS documentation](https://docs.dfir-iris.org/operations/modules/natives/IrisSeika/). 

## Installation 
 The installation can however be done manually if required, 
either from sources or existing packages (go to step 3.)

1. Git clone this repository ``git clone https://github.com/dfir-iris/iris-seika-module.git && cd iris-seika-module``
2. Build the wheel : ``python3 setup.py bdist_wheel`` 
3. Copy the wheel into the IRIS app docker container ``docker cp iris_seika_module-XX-py3-none-any.whl container:/iriswebapp/dependencies/``
4. Get an interactive shell on the docker : ``docker exec -it container /bin/sh``
5. Install the new package ``pip3 install dependencies/iris_seika_module-XX-py3-none-any.whl``
