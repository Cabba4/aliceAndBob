## Steps to run script

1.	Extract data from samples folder 
```
tar -zxvf samples.tar.gz
```
2.	Install python requirements if any
```
pip install <missing package>
```
3.	Setup openfhe-python - https://github.com/openfheorg/openfhe-python/tree/main 

    The instructions in readme should work fine if openfhe-development is working. Remember to use sudo make install so its accessible globally, that cause a lot of issues.  
    Also check after openfhe-python is installed that python has it in pythonpath.
    My openfhe-python installed in /usr/local so i had to add
    to my terminal env to make it run
```
export PYTHONPATH=/usr/local:$PYTHONPATH 
```

4.	Run the script. python3 dataset.py
