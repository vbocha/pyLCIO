
### Local 

```bash
docker run -it -p 8888:8888 ilcsoft/py3lcio bash  
```
this will spin up a container with port mappings to your local PC.

```bash
cd LCIO; source setup.sh; cd .. 
jupyter notebook --port=8888 --ip=0.0.0.0 --allow-root 
```

Click the link from your screen which starts with "http://127.0.0.1:8888/?token=XXxXXXXX...". Then you should see the notebook. You create a notebook from the upper-right cornet with 'python 3' kernel and then type `import pyLCIO`



