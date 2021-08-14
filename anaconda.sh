conda install conda-build
conda install anaconda-client
pip install jinja2
conda-build .
conda login
conda config --set anaconda_upload yes
conda upload .....