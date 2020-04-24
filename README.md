## G9 Instructions

#### Evan Mi, Blake Weis, Justin Chiu, Ruican Zhong

### Data Preparation: 

- **System**: [MongoDB 4.2.5](https://www.mongodb.com/download-center/community)
  - Installed through Homebrew (any recent version should work with what we have)
- **Data Summary**:
  - Overview of data collection and dataset can be found [here](https://github.com/jamesqo/gun-violence-data) 
  - To download the data, follow [this link](https://github.com/jamesqo/gun-violence-data/blob/master/DATA_01-2013_03-2018.tar.gz?raw=true). You can unzip the tar file to retrieve the csv file. However, we have included a smaller version with 1000 data points here named *shortStage3.csv*
- **Loading Data & Preprocessing**:
  - Run `python3 preprocessing.py` in terminal to load and preprocess the data
    - Make sure numpy, pandas, and pymongo are installed
    - mongo daemon is running in a separate terminal
    - The csv file extracted is in the same directory as the script
  - Note: if you are trying to run the preprocessing script on the shorter 1000 data point version, you need to change pd.read_csv("stage3.csv") to pd.read_csv("shortStage3.csv") in the script

### Application and Code:
- **Setup Requirements (Programming Languages Versions)**
  - Python 3 (for preprocessing)
  - Third-party libaries: Numpy, Pandas, PyMongo (for preprocessing)
  - Java 8 (for setting up the Cloud9Agent of Knowi)
- **For Knowi**:
  - **Setup**:
    1. Make sure the mongo daemon is running by `mongod` command in a terminal
    2. Sign up for a free trial
    3. Install the [Cloud 9 Agent](https://www.knowi.com/docs/cloud9Agent.html) (Java 8 required, anything higher does not work)
    4. To start the agent, change directory to the Cloud 9 Agent folder in a new terminal window, then run command `./run.sh` (Mac) or `run.bat` (Windows)
    5. Next, sign in to your account on Knowi
    6. To create a data source, go to *Data sources* tab on the left hand side of the screen and input localhost into Hosts and 27017 into Port. For Database Name, you should use gunviolence (based on our preprocessing script, that is the name of our collection). Then click *Use Agent* and select the API key for the agent you downloaded. 
   
  - **Querying & Visualizing**:
    1. To create and run queries, go to *Queries* tab and create a new query. You can just copy and paste our queries from *Query.docx* here into *Mongo Query Box* and click *Save and Run* now. 
    2. Navigating to the dashboard, you can now add visualizations to it by dragging a widget (generated from executing the query in previous step) into the dashboard and selecting the type of visualization you want by clicking the three dots at the top right and choose *Analyze*
    3. Using this [link](https://www.knowi.com/d/cIbLJXLFpR90plRTfFAb78kGisvjhviiSrEK1DC81BQMEie), you can see the visualizations we created, and the specific parameters we used to set up the visualizations. Each visualization has a title and a number, corresponding to the name listed in the query document as well as the last slide of our presentation

### Code Documentation and References: 

- Everything was written by us. We did not use Github code or anything else. 
  
### List of Documents:

| File Name  | Description |
| ------------- |-------------|
| shortStage3.csv    | Small portion of the data used (1000 data point) |
| preprocessing.py | Script for preprocessing | 
| Query.docx | Doc that contains all the queries and their brief descriptions corresponding to the visualizations on the dashboard | 





