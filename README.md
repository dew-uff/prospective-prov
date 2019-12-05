# Prospective-prov

Copyright (c) 2019 Universidade Federal Fluminense (UFF). All rights reserved.

ProspectiveProv is a provenance visualization tool that uses provenance data collected by 
[noWorkflow](https://github.com/gems-uff/noworkflow) to generate a provenance graph based on the prospective provenance, allowing scientists to obtain details about the scientific experiments developed in Python. We expect that prospectiveProv can be helpful to allow developers and scientists to have a better understanding of the programming structure of Python script experiments. 

Using prospectiveProv is simple. For generate provenance graphs using prospectiveProv, the users only need to run a Python script experiment using [noWorkflow](https://github.com/gems-uff/noworkflow) and perform prospectiveProv right away. Currently, this version of prospectiveProv supports [Python 3.6](https://www.python.org/downloads/release/python-360/) and [noWorkflow-2.0 Alpha](https://github.com/gems-uff/noworkflow/tree/2.0-alpha).


Developers:
- [Vítor Gama Lemos (UFF)](https://github.com/vitorglemos)
- [Charles Luiz de Souza Mendes (UFF)](https://www.linkedin.com/in/charles-mendes-0a790bb6/)

## System Requirement
   - [Python 3.6](https://www.python.org/downloads/release/python-360/)
   - [noWorkflow-2.0](https://github.com/gems-uff/noworkflow/tree/2.0-alpha)
   - [GraphViz version 2.40.1 or higher](https://www.graphviz.org/)

## Quick Installation

## Basic Usage
To use the ProspectiveProv, you must execute your script Python using noWorkflow. After running your script, in the ".noworkflow" folder, you could call the prospectiveProv as follow: 
```
prospective trial <trial_id> 
```
After that, the prospectiveProv will use the information available in the SQLite database created by noWorkflow to generate a provenance graph based on script structure, displaying calls, functions, conditional sentences, loops, variables, and classes.

To see all functions available in ProspectiveProv, just run the following command:
```
prospective --help 
```
### Inspecting variables

To check the contents of all variables in the provenance graph, just run the command:
```
prospective --trial <id> --var 1 
```
### Showing executed code blocks

ProspectiveProv also allows to display in the provenance graph all lines of code that are activated during the execution of the script, just type:
```
prospective --trial <id> --act 1 
```

### 

## License Terms
The MIT License (MIT)

Copyright (c) 2019 Universidade Federal Fluminense (UFF). All rights reserved.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
