# Input generator
Uses an artificial neural network to generate an input based on the absence or presence of a hidden state.

![Figure 1](zeldenrust_fig1.JPG)

The method is described in the following paper:<br>
Zeldenrust, F., de Knecht, S., Wadman, W. J., Denève, S., Gutkin, B., Knecht, S. De, Denève, S. (2017). Estimating the Information Extracted by a Single Spiking Neuron from a Continuous Input Time Series. _Frontiers in Computational Neuroscience_, 11(June), 49. [doi:10.3389/FNCOM.2017.00049](https://doi.org/10.3389/fncom.2017.00049)<br>Please cite this reference when using this method.

## Setup
Work somthing out with the requirements.txt format

## Usage
Specify your parameters like duration, mean firing rate and qon/qoff generator type in the main.py file.
Run "python main.py", to generate results (with the newest version installed as per requirements.txt). Alternative tweaks as the number of artificial neurons and kernel type van be adjusted in the code/make_input_experiments.py file.

## Structure
The repository is organised into x main folders. The root contains the main.py file, used to run the program.
* /code: Contains the classes and functions used in the program.
  - 


## Math?
$$E = mc^2$$

## Visualisation
matplotlib it all

## License
This repository has licensed under the MIT licence. Read [LICENCE.txt](https://github.com/) for the full terms and conditions.
 