
### Local 

If you want to use `ROOT`: 
```bash
docker run -it --rm -v $PWD/pyLCIO/examples:/home/ilc/data -p 8888:8888 ilcsoft/py3lcio bash
```

If you wish to use `matplotlib`:
```bash
docker run -it --rm -v $PWD/pyLCIO/examples:/home/ilc/data -p 8888:8888 ilcsoft/py3lcio:matplotlib bash
```

this will spin up a container with port mappings to your local PC as well as a local path mounted on to the container.

```bash
cd LCIO; source setup.sh; cd .. 
conda activate root_env ## if you wish to use matplotlib instead of ROOT
jupyter notebook --port=8888 --ip=0.0.0.0 --allow-root 
```

Click the link from your screen which starts with "http://127.0.0.1:8888/?token=XXxXXXXX...". Then you should see the notebook. You create a notebook from the upper-right cornet with 'python 3' kernel and then type `import pyLCIO`





