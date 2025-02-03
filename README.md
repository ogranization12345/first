# Accompanying repository to the paper

This repo contains Jupyter Notebooks and scripts for research on moral bias of LLM. 
Script for scenarios generation and postprocessing are taken (or heavily based) on [code](https://github.com/kztakemoto/mmllm) and [research](https://doi.org/10.1098/rsos.231393) of Kazuhiro Takemoto.

## Usage

### Generation
The folder contains Jupyter notebook which could generate Moral Machine like scenarios in batch. Currently, Russian and English, German and French languages are available. Each language generator divided into section, example subsection contain blocks for simple print and generation into json for different scenarios.

### Requests 
At the moment, three of notebooks are written for purpose of interaction with Yandex GPT, Sber's Gigachat and open-source models, available from LM Studio. In first blocks json with scenarios should be provided. Output of code running is pickle file with responses of respected LLM.

### Processing
Pickle files with requests should be processed with python script of corresponding language to be convert in csv file. Output table could be analyzed with MoralMachinesStatistics notebook.

### Data
Folder contains subfolders with csv's of each experiment mentioned in paper, devided by language

### Images
Higher resolution of images used in paper
