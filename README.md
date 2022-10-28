# RaiSimQuadruped

## Setup
1. Init submodules
```
git submodule update --init
```
2. Install RaiSimLib - https://raisim.com/sections/Installation.html. Create a python virtual enviroment
```
python3 -m venv raisim-quadruped-env # Create a python virtual enviroment

cd $WORKSPACE/raisimLib
mkdir build
cd build
cmake .. -DCMAKE_INSTALL_PREFIX=$LOCAL_INSTALL -DRAISIM_EXAMPLE=ON -DRAISIM_PY=ON -DPYTHON_EXECUTABLE=$(python3 -c "import sys; print(sys.executable)")
make install -j4

```


