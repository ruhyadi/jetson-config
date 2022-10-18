# Jetson Nano Configuration
Jetson Nano Configuration 🚀

## Initial Configuration
This will be initial configuration to get most in Jetson Nano
### 1. Install Miniconda/Mamba
Download the latest Mamba for aarch64 (arm64) architecture that meet Jetson Nano
```bash
wget https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-Linux-aarch64.sh
```
Then, install Mamba and create your own environment
```bash
bash ./Mambaforge-Linux-aarch64.sh
```
```bash
mamba create -n your_env python=3.x numpy
```
To activate virtual env please run
```bash
mamba activate your_env
```
> Note: you can still use `conda` instead `mamba` for every function
### 2. Install Python-dev and Pip
Beside you have install virtual env with conda/mamba, it's good to have python that rooting on your system. Jetson Nano with Jetpack have already install it for you but not for Pip. So in order to update it please run
```bash
sudo apt-get install python3-dev python3-pip
```

### 3. Install Jetson Stats (`jtop`)
Jetson stats will give your information about your Jetson machine. Jetson Stats can only be install with `sudo pip3`
```bash
sudo pip3 install jetson-stats
sudo jtop
```
