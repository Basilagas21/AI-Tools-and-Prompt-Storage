---
tags:
  - prompt
  - prompt/technical
  - prompt/analytical
---
This prompt for creating a program where it generates two dataset. One for constant dataset and the other one is a real time changing dataset to simulate real time data changes within the dataset. The data of the patients' data are medical related data as shown in the image below:

![[Patient's Data.png| Patient's Data]]
### The Prompt
given the program that I have uploaded here, I have a very hard to explain kind of goal u need to achieve here. Basically, I want u to implement the program where it generates two csv file. Make sure to keep the flow of the program the same where when I run with python run_analysis.py, initially, it should ggenerate the dataset and it is controlled form the config.yaml file. After that, when after it generates the data set which is the patient_data.csv, it uses nbformat to automate all of the newly and fresh generated data to be used into the PatientDataExploratory.ipynb immediately. Basically this work flow, introduce laziness where I only need to run it by just typing python run_analysis.py and it should generate the dataset and then update the data to be used in the PatientDataExploratory.ipynb immediately.

So right now, I have a new task for u. Basically, try to maintain the flow of the current program and we need the program to generate two dataset. Both will have some kind of window to view some of the data in the dataset and the window will move across the dataset according to time interval. The time interval can also be changed in the yaml file. The size of the window can be changed in the yaml file. 

However, the first dataset should be constant with the applied window.I will use the brackets to represent the moving window across the dataset For example:

Time_intereval set = Every 1 minutes
Size of window = 1

The first minute:
Dataset A= [("1"),"2","3","4","5","6"]

The second minute:
Dataset A= [("1",("2"),"3","4","5","6"]

The third minute:
Dataset A= [("1","2",("3"),"4","5","6"]

and once it reaches the last item in the list, it should iterate back to the first. For the first dataset generated. The data should be constant and should not change


this is the second dataset that should be generated after the first one:

The second dataset should also have the applied window. However, the values/items in the dataset are constantly changing outside the window. I will use the brackets to represent the moving window across the dataset For example:

Time_intereval set = Every 1 minutes
Size of window = 1
Note: Alpahbet variable used in this example may be varied based on what is stored in the variable. It should change when not being viewed through the "applied window"


The first minute:
Dataset A= [("A"),"B","C","D","E","F"]

The second minute:
Dataset A= ["A",("B"),"C","D","E","F"]

The third minute:
Dataset A= ["A","B",("C"),"D","E","F"]

now don't use this simple example that I have given to u. Use the patient_data's parameters instead

how bout this, when i run the program, it should the flow as such where it generates the datasets and then updates the PatientDataExploratory.ipynb. Since its based i want the the dataset (the want that should keep changing the dataset outside the window) while the other one stays completely unchange when running this program. like i said, the time interval can be changed in the yaml file

wait how to change the time interval? Coz so how i want the real time tracking to work for the second dataset is every single time, some new data are created within the dataset, some are removed with the same amount. This is how i want to simulate the real time tracking for the program at this current stat. Also when i run using the comamnd python run_analysis.py, i dont want the program to stop until i mannaulyl stop it in the terminal. I only want the process of constatly adding new data and removing data at the same time for the second dataset. The first one? no need changes after the generation of it.


so i ran the program and notice that it add one new data every interval time at the very bottom of the csv file. But how bout the deletion of the data? does choose random data to delete or deletes the old old ones?


ok so right now, i want to control how much the second dataset adds and remove data in the yaml file. Keep the randomness

### Prompt Output

[[README | Patient Data Simulator Program]]