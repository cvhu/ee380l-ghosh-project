What does this folder contain?
--Output files obtained by running mallet

Files named <Input>-keys-v*.txt
--Contain a set of topics when run on file <Input>
--Data is formatted as [ topic id#, <importance of topic>, cluster of words associated with the topic ]
--The cluster of words give a good indication of some topic, but we need data expert (Maureen) to interpret it for us

Files named <Input>-composition-v*.txt
--Contains the correlation values for each original input file with each of the generated topics
--Data format [ original file #, file_name or content, <topic#, correlation>+ ]
