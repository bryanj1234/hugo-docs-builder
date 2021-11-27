---
title: Google MLCC
chapter: false
---

## Google MLCC (Machine Learning Crash Course) exercises

Taken from https://developers.google.com/machine-learning/crash-course.

Python environment configured as specified here:

https://developers.google.com/machine-learning/crash-course/running-exercises-locally.

Requires Anaconda.

### Local Anaconda environment: mlcc (details below).

As of 2021-11-20, the Google Colab notebook was using Python 3.6.13,
so that's what I'm using locally for this project.


    conda list -n mlcc
    # packages in environment at /home/bryan/anaconda3/envs/mlcc:
    #
    # Name                    Version                   Build  Channel
    _libgcc_mutex             0.1                        main  
    _openmp_mutex             4.5                       1_gnu  
    absl-py                   0.15.0                   pypi_0    pypi
    argon2-cffi               20.1.0           py36h27cfd23_1  
    astunparse                1.6.3                    pypi_0    pypi
    async_generator           1.10             py36h28b3542_0  
    attrs                     21.2.0             pyhd3eb1b0_0  
    backcall                  0.2.0              pyhd3eb1b0_0  
    bleach                    4.0.0              pyhd3eb1b0_0  
    ca-certificates           2021.10.26           h06a4308_2  
    cached-property           1.5.2                    pypi_0    pypi
    cachetools                4.2.4                    pypi_0    pypi
    certifi                   2021.10.8                pypi_0    pypi
    cffi                      1.14.6           py36h400218f_0  
    charset-normalizer        2.0.7                    pypi_0    pypi
    clang                     5.0                      pypi_0    pypi
    cycler                    0.11.0                   pypi_0    pypi
    dataclasses               0.8                      pypi_0    pypi
    decorator                 5.1.0              pyhd3eb1b0_0  
    defusedxml                0.7.1              pyhd3eb1b0_0  
    entrypoints               0.3                      py36_0  
    flatbuffers               1.12                     pypi_0    pypi
    gast                      0.4.0                    pypi_0    pypi
    google-auth               1.35.0                   pypi_0    pypi
    google-auth-oauthlib      0.4.6                    pypi_0    pypi
    google-pasta              0.2.0                    pypi_0    pypi
    grpcio                    1.41.1                   pypi_0    pypi
    h5py                      3.1.0                    pypi_0    pypi
    idna                      3.3                      pypi_0    pypi
    importlib-metadata        4.8.2                    pypi_0    pypi
    importlib_metadata        4.8.1                hd3eb1b0_0  
    ipykernel                 5.3.4            py36h5ca1d4c_0  
    ipython                   7.16.1           py36h5ca1d4c_0  
    ipython_genutils          0.2.0              pyhd3eb1b0_1  
    jedi                      0.17.0                   py36_0  
    jinja2                    3.0.2              pyhd3eb1b0_0  
    joblib                    1.1.0                    pypi_0    pypi
    jsonschema                3.2.0              pyhd3eb1b0_2  
    jupyter_client            7.0.1              pyhd3eb1b0_0  
    jupyter_core              4.8.1            py36h06a4308_0  
    jupyterlab_pygments       0.1.2                      py_0  
    keras                     2.6.0                    pypi_0    pypi
    keras-preprocessing       1.1.2                    pypi_0    pypi
    kiwisolver                1.3.1                    pypi_0    pypi
    ld_impl_linux-64          2.35.1               h7274673_9  
    libffi                    3.3                  he6710b0_2  
    libgcc-ng                 9.3.0               h5101ec6_17  
    libgomp                   9.3.0               h5101ec6_17  
    libsodium                 1.0.18               h7b6447c_0  
    libstdcxx-ng              9.3.0               hd4cf53a_17  
    markdown                  3.3.4                    pypi_0    pypi
    markupsafe                2.0.1            py36h27cfd23_0  
    matplotlib                3.3.4                    pypi_0    pypi
    mistune                   0.8.4            py36h7b6447c_0  
    nbclient                  0.5.3              pyhd3eb1b0_0  
    nbconvert                 6.0.7                    py36_0  
    nbformat                  5.1.3              pyhd3eb1b0_0  
    ncurses                   6.3                  h7f8727e_2  
    nest-asyncio              1.5.1              pyhd3eb1b0_0  
    notebook                  6.4.3            py36h06a4308_0  
    numpy                     1.19.5                   pypi_0    pypi
    oauthlib                  3.1.1                    pypi_0    pypi
    openssl                   1.1.1l               h7f8727e_0  
    opt-einsum                3.3.0                    pypi_0    pypi
    packaging                 21.0               pyhd3eb1b0_0  
    pandas                    1.1.5                    pypi_0    pypi
    pandoc                    2.12                 h06a4308_0  
    pandocfilters             1.4.3            py36h06a4308_1  
    parso                     0.8.2              pyhd3eb1b0_0  
    pexpect                   4.8.0              pyhd3eb1b0_3  
    pickleshare               0.7.5           pyhd3eb1b0_1003  
    pillow                    8.4.0                    pypi_0    pypi
    pip                       21.0.1           py36h06a4308_0  
    prometheus_client         0.11.0             pyhd3eb1b0_0  
    prompt-toolkit            3.0.20             pyhd3eb1b0_0  
    protobuf                  3.19.1                   pypi_0    pypi
    ptyprocess                0.7.0              pyhd3eb1b0_2  
    pyasn1                    0.4.8                    pypi_0    pypi
    pyasn1-modules            0.2.8                    pypi_0    pypi
    pycparser                 2.21               pyhd3eb1b0_0  
    pygments                  2.10.0             pyhd3eb1b0_0  
    pyparsing                 3.0.6                    pypi_0    pypi
    pyrsistent                0.17.3           py36h7b6447c_0  
    python                    3.6.13               h12debd9_1  
    python-dateutil           2.8.2              pyhd3eb1b0_0  
    pytz                      2021.3                   pypi_0    pypi
    pyzmq                     22.2.1           py36h295c915_1  
    readline                  8.1                  h27cfd23_0  
    requests                  2.26.0                   pypi_0    pypi
    requests-oauthlib         1.3.0                    pypi_0    pypi
    rsa                       4.7.2                    pypi_0    pypi
    scikit-learn              0.24.2                   pypi_0    pypi
    scipy                     1.5.4                    pypi_0    pypi
    seaborn                   0.11.2                   pypi_0    pypi
    send2trash                1.8.0              pyhd3eb1b0_1  
    setuptools                58.5.3                   pypi_0    pypi
    six                       1.15.0                   pypi_0    pypi
    sklearn                   0.0                      pypi_0    pypi
    sqlite                    3.36.0               hc218d9a_0  
    tensorboard               2.6.0                    pypi_0    pypi
    tensorboard-data-server   0.6.1                    pypi_0    pypi
    tensorboard-plugin-wit    1.8.0                    pypi_0    pypi
    tensorflow                2.6.2                    pypi_0    pypi
    tensorflow-estimator      2.6.0                    pypi_0    pypi
    termcolor                 1.1.0                    pypi_0    pypi
    terminado                 0.9.4            py36h06a4308_0  
    testpath                  0.5.0              pyhd3eb1b0_0  
    threadpoolctl             3.0.0                    pypi_0    pypi
    tk                        8.6.11               h1ccaba5_0  
    tornado                   6.1              py36h27cfd23_0  
    traitlets                 4.3.3            py36h06a4308_0  
    typing-extensions         3.7.4.3                  pypi_0    pypi
    typing_extensions         3.10.0.2           pyh06a4308_0  
    urllib3                   1.26.7                   pypi_0    pypi
    wcwidth                   0.2.5              pyhd3eb1b0_0  
    webencodings              0.5.1                    py36_1  
    werkzeug                  2.0.2                    pypi_0    pypi
    wheel                     0.37.0                   pypi_0    pypi
    wrapt                     1.12.1                   pypi_0    pypi
    xz                        5.2.5                h7b6447c_0  
    zeromq                    4.3.4                h2531618_0  
    zipp                      3.6.0              pyhd3eb1b0_0  
    zlib                      1.2.11               h7b6447c_3