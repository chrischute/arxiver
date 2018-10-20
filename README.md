## ArXiver

ArXiver is a script for collecting papers from ArXiv.

You can collect your own papers and generate header notes as follows:

  - Create a text file with one arXiv.org URL on each line
  - Create a conda environment with `conda env create -f environment.yml`
  - Run `python get_papers.py --input_file <FILE> --output_dir <DIR>`

The script will download the PDF for each paper, and it will auto-generate
a header file for taking notes in markdown format.

Example output from ArXiver: 
[ResNet papers](https://github.com/chrischute/papers/tree/master/01-resnets).
