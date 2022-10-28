#!/usr/bin/env bash
git submodule update --init

ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"
EXEC_PATH=$PWD
LOCAL_INSTALL=$EXEC_PATH/raisim_build

cd $EXEC_PATH
python3 -m venv raisim-quadruped-env # Create a python virtual enviroment
source raisim-quadruped-env/bin/activate
# pip install numpy


cd $EXEC_PATH/raisimLib
mkdir build
cd build
cmake .. -DCMAKE_INSTALL_PREFIX=$LOCAL_INSTALL -DRAISIM_EXAMPLE=ON -DRAISIM_PY=ON -DPYTHON_EXECUTABLE=$EXEC_PATH/raisim-quadruped-env/bin/python3
make install -j8

cd $EXEC_PATHec

if [[ $1 = "--addpath" ]]
then
    case $SHELL in
    */zsh) 
        echo "export LD_LIBRARY_PATH=$LOCAL_INSTALL/lib\${LD_LIBRARY_PATH:+:\${LD_LIBRARY_PATH}}"  >> ~/.zshrc && \
        echo "export PYTHONPATH=$LOCAL_INSTALL/lib/python3.8/site-packages\${PYTHONPATH:+:\${PYTHONPATH}}"  >> ~/.zshrc
    ;;
    */bash)
        echo "export LD_LIBRARY_PATH=$LOCAL_INSTALL/lib\${LD_LIBRARY_PATH:+:\${LD_LIBRARY_PATH}}"  >> ~/.bashrc && \
        echo "export PYTHONPATH=$LOCAL_INSTALL/lib/python3.8/site-packages\${PYTHONPATH:+:\${PYTHONPATH}}"  >> ~/.bashrc
    ;;
    *)
    echo $SHELL
    esac
else
echo "Check add path"
fi
