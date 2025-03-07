advanced installation: (high performance)
for ease of use it is recommended to use visual studio code when loading this project

1) install anaconda https://www.anaconda.com/download
2) install python 3.9.20 either via https://www.python.org/downloads/release/python-3920/ or by installing the VS studio python extension
3) create and enter a virtual envrionment either by adding anaconda to the VS studio environment variables then selecting new virtual environment,
   or by running:

   conda create --name myenv python=3.9
   conda activate myenv

   in your terminal

4) add cuda and cudatoolkit to your virtual environment either by running:
   conda install -c conda-forge cudatoolkit=11.2 cudnn=8.1.0

   if you have conda-forge or else by adding your existing cuda and cudatoolkit installs to the environment variables for your conda environment (found in its
   activation script)

5) install the master_dictionary_refactor_branch branch of this project

6) verify cuda by checking that running nvcc --version returns your cuda version, then run trial_runner_main on its own to ensure tensorflow has discoverd
    your GPU, if tensorflow has not discoverd your GPU then follow these instructions: https://medium.com/analytics-vidhya/solution-to-tensorflow-2-not-using-gpu-119fb3e04daa

7) run pip install -r requirements.txt to install python library dependencies.

simple installation:
1) acquire visual studio code from here: https://code.visualstudio.com/
2) once installed, find the extensions tab in the vertical toolbar, search python and install.
3) download all the files in the 'master dictionary refactor' branch of the github (click on the icon that by default says main and scroll to this one)
4) put those files in a single folder
5) back in vs-code click file in the horizontal toolbar at the top, then open folder, navigate into the folder you just created
6) in the same hotbar, click terminal + new terminal
7) paste pip pip install -r windows_requirements.txt into the field that pops up and click enter
8) once that is finished put python src\\GUI\\pages\\front_end_main.py in the same field
9) the application window should now open and you can follow the steps in 'running'

running:
1) run front_end_main.py
2) select the attack and model you wish to use as directed.
3) set the number of trials you wish to run and the number of images which should be involved in each trial.
4) copy in your settings for each of your attacks hyperparameters in CSV format.
     any hyperparameters for which your do not specify values will take default values
     if you specify less settings than the number of trials (n) you are running then your setting will repeat.
     if you specify more settings than the number of trials (n) you are running then only the first n settings will be used.
5) click continue
6) wait for your trial to terminate
7) if you wish to store your results persistently, the results of your trial will be stored in a new folder 'results' in the same directory as the src for this
  project.
