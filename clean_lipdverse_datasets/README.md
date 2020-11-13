### Predictions on LipdVerse Data

#### Requirements

1. You need to use python 3.8
2. Install the following packages

    ```
    conda install lipd
    ```

3. Run the notebook LiPDverse.ipynb

#### What are we trying to achieve
 
1. Get archiveType from Linked Earth Wiki Queries and the LinkedEarth Ontology and generate a mapping of archiveType : correctArchiveType<br>
eg. {'marine sediment': 'MarineSediment', 'lake sediment': 'LakeSediment', 'glacier ice': 'GlacierIce', 'documents': 'Documents', 'borehole': 'Rock', 'tree': 'Wood', 'bivalve': 'MollusckShell'}
2. Get proxyObservationType from LLinked Earth Wiki Queries and the LinkedEarth Ontology and generate a mapping of proxyObsType : correctProxyObsType<br>
eg. {'C37.concentration': '37:2AlkenoneConcentration', 'trsgi': 'Trsgi', 'd-excess': 'deuteriumExcess', 'deuteriumExcess': 'deuteriumExcess', 'd2H': 'dD', 'dD': 'dD', 'd18o': 'd18O'}
3. Similar mapping for Inferred Variable Type is generated.
4. Read LiPD files from lipdverse.org
    a. Temperature 12K
    b. iso2K
    c. PalMod
    d. Pages 2K Temperature
5. We have divided our work into 2 types based on the variableType: measured v/s inferred, NA
6. For each file we get the following details
    a. Dataset name	        b. Compilation name	
    c. ArchiveType	        d. Predicted ArchiveType	
    e. TSid	                f. VariableType	
    g. VariableName	        h. Predicted proxyObsType	
    i. Remainder(variableName)	j. ProxyObservationType	
    k. Final ProxyValue	    l. ProxyValue from
    m. Units	            n. hasProxySystem	
    o. ProxySystem.SensorType	p. Interpretation/variable	
    q. Interpretation/variableDetail

    Meaning : In many cases we do not get the proxyObservationType from the LiPD file, we can predict this value from the variableName using the mapping we have generated previously. (rank = 3)
    Predicted proxyObservationType is the value predicted from the variableName (rank = 2)
    Remainder(variableName) is the value left from the variableName after getting the predicted proxyObsType. example Mg/Ca.ruber This is useful to understand the Genus and Species = ruber in the proxySensor.
    ProxyObservationType is the actual value from the file.(rank = 1)
    Final ProxyValue = based on the availability of the above values, this column is filled in the increasing order of rank.
    ProxyValue from contains the rank of where the value was filled.
7. Generate a similar file for Inferred variable Type.
8. TSid is a unique value for every variable in every file. This means TSid should not repeat across files. We have created a master_flagged file where we capture the duplicates.
These files need to be looked at.


#### Outcome
    1. master_lipd.csv: archiveType and proxyObservationType
    2. master_lipd_inferred.csv: archiveType and inferredVariableType
    3. master_flagged.csv: to capture duplicate TSids across all the datasets
