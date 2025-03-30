# fast-dataset-viewer
This is a tool for quickly viewing and cleaning a dataset. 

## Installation
To use the program you need:

1) Download repo:

```bash
git clone https://github.com/NMDanilovich/dataset-fast-viewer.git
cd dataset-fast-viewer
```

2) Activate Python enviremement (optional)

```bash
python3 -m venv .venv
source ./.venv/bin/activate
```

3) Install requariments:

```bash
pip install -r requariments.txt
```

## Usage

For run programm use

```bash
python3 dataset_viewer.py [-h] --images /path/to/images --labels /path/to/labels [--window_size width hight]
```

## Functionality

__WARNING! Clear and delete change data as soon as you press a keys without the possibility of recovery.__

### View

You can move from one annotation frame to another using the square brackets ("[" - backward, "]" - forward) in the window thet opens.  

### Clear

You can clear the annotation for the frame you stopped on by using the "c" key.

### Delete 

You can delete an unnecessary frame by pressing the "d" key.


