# Dynamic input generator
Uses an artificial neural network (ANN) to generate an excitatory and inhibitory conductance based on the absence or presence of a hidden state.

![Figure 1](https://www.frontiersin.org/files/Articles/237283/fncom-11-00049-HTML/image_m/fncom-11-00049-g001.jpg)

The method is described in the following paper:<br>
Zeldenrust, F., de Knecht, S., Wadman, W. J., Denève, S., Gutkin, B., Knecht, S. De, Denève, S. (2017). Estimating the Information Extracted by a Single Spiking Neuron from a Continuous Input Time Series. _Frontiers in Computational Neuroscience_, 11(June), 49. [doi:10.3389/FNCOM.2017.00049](https://doi.org/10.3389/fncom.2017.00049)

However, in the dynamic setup the spike trains of the ANN now generate seperated excitatory and inhibitoty conductances in stead of currents. In practice this conductance is multiplied by the membrane voltage of the neuron to inject a current. <br>Please cite this reference when using this method. 

## Setup
The requirements.txt file contains the packages that have been used to run the code and determine chip layout. Install packages using:

`conda install --file requirements.txt`

Or by

`pip install -r requirements.txt`

One of the functions `analyze_exp` is imported from Matlab. In chase dependence is flawed, see [this file](file:///C:/Users/miksc/OneDrive/Documenten/Study/Internship/Zeldenrust/Scripts/analyze_exp/for_redistribution_files_only/.html).


## Usage
Specify your parameters like duration, mean firing rate, qon/qoff generator type and input type in the main.py file.
Run "python main.py", to generate results (with the newest version installed as per requirements.txt). Alternative tweaks as the number of artificial neurons and kernel type van be adjusted in the code/make_input_experiments.py file.

## Structure
The repository is organised into x main folders. The root contains the main.py file, used to run the program.
* /code: Contains the classes and functions used in the program.

  - /classes: Contains the Input class used to generate an input
  - /functions: Contains the make_input/dynamic_experiments function that creates the hiddenstate and input.
* /results: Contains the input generated by main.py and a function plotter.py to quickly visualise it.

## Visualisation
Run "python results/plotter.py" to visualize some of the results. Additional 'sanity checks' can be found within the code to check your data. 

## License
This repository has licensed under the MIT licence. Read [LICENCE.txt](https://github.com/Sargos-coder/internship/blob/master/LICENSE) for the full terms and conditions.
 