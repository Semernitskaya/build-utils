#### Python utilities for automation some processes and analysis during development of application (mainly Java + Maven application) 
Need Python version 3.6.8 or higher

__check_dependencies_in_tree.py__ - compares overlays from Jboss/Wildfly standalone.xml and 
dependencies from dependency tree   

view help:  
```bash
python3 check_dependencies_in_tree.py --help
``` 
run example:
```bash
python3 check_dependencies_in_tree.py --pom /home/usr/projects/discovery/pom.xml --mvn /opt/apache-maven-3.6.1/bin/mvn --xml /home/usr/Downloads/standalone.xml --platform_version 8.2
```
__convert_properties_to_yaml.py__ - converts properties-file to yaml-file

view help:  
```bash
python3 convert_properties_to_yaml.py --help
``` 
run example:
```bash
python3 convert_properties_to_yaml.py --f application.properties 
```
__copy_project_sources.py__ - copies Maven-project sources to the target directory, ignore git-files, 
idea-configs etc

view help:  
```bash
python3 copy_project_sources.py --help
``` 
run example:
```bash
python3 copy_project_sources.py --source /home/usr/projects/discovery --target /home/usr/projects/copy
```
__find_dependencies_diff.py__ - compares dependencies from two different war-files

view help:  
```bash
python3 find_dependencies_diff.py --help
``` 
run example:
```bash
python3 find_dependencies_diff.py --f1 /home/usr/projects/discovery/discovery-1.0.war --f2 /home/usr/projects/discovery/discovery-0.23.war
```
__maven_deploy_to_remote_repository.py__ - deploys artifacts from local Maven repository to remote

view help:  
```bash
python3 maven_deploy_to_remote_repository.py --help
``` 
run example:
```bash
 python3 maven_deploy_to_remote_repository.py --url http://mvn/artifactory/ --login olga --pwd secret --dir /home/usr/docs/repository_20190708/ --filters ru,mex
```
