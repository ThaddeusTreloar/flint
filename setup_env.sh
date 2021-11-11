#!/bin/bash

if ! command -v pip &> /dev/null
then
	echo "pip not installed. Install python-pip using your distro package manager - e.g. sudo pacman -S python-pip."
	exit
fi

py_pip_packages=("PyYAML" "numpy" "sklearn")

echo "Determining pip packages"
for package in ${py_pip_packages[@]}; do
	if [[ $(pip list | grep $package) ]]; then
		echo $package "... already installed!"
	else
		pip install $package
	fi
done

