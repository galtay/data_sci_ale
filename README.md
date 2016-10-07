# Put Data Science On Your Computer!

A practical guide to a grab bag of data science techniques with a bias towards medical data.

# Anaconda Software Distribution


## Environment Setup

A handy dandy Python (+ other stuff) universe can be at your fingertips thanks to the folks at [Continuum Analytics](https://www.continuum.io/).  To get started, go to their download page and install the Anaconda software distribution (the Python 3 version),

 * https://www.continuum.io/downloads

You can use either the graphical installer or the command line installer (I recommend the command line installer).  Clicking on the command line installer link will begin downloading a file named something like `Anaconda3-4.2.0-MacOSX-x86_64.sh`.  In your terminal, navigate to where that file lives and run it using the following command,

```shell
bash Anaconda3-4.2.0-MacOSX-x86_64.sh
```

When the file is run, you will be asked to accept the license agreement and to choose an installation location (the default is your home directory and is fine).  Once you select an install location, you will see package names scroll by as they are installed.  As the final step, the installer will ask you,

```shell
Do you wish the installer to prepend the Anaconda3 install location
to PATH in your /Users/galtay/.bash_profile ? [yes|no]
[yes] >>>
```

Say yes to this.  It will append something like,

```shell
# added by Anaconda3 4.2.0 installer
export PATH="/Users/galtay/anaconda3/bin:$PATH"
```

to your `.bash_profile` file and it will advise you that this change will not become active until you open another terminal (which you should do).  Even if you don't use the bash shell you can copy the `export` command into the appropriate startup file (e.g. .zshrc for zsh).


## Environment Notes

When you are done, you should have a directory called `anaconda3` in your home directory.  This is an isolated little nugget of computing power.  You may have other Python version managing tools on your system (e.g. pyenv).  The above command will override those tools.  If you prefer to not use the Anaconda distribution at some later time, you can comment out the `export` line from your startup script (i.e. `.bash_profile`) and open a new terminal.  If you ever want to totally remove the distribution, simply delete this directory `anaconda3`.


## Random Posts About Anaconda

  * [conda docs](http://conda.pydata.org/docs/get-started.html)
  * [reddit on Anaconda](https://www.reddit.com/r/Python/comments/3t23vv/what_advantages_are_there_of_using_anaconda/?st=itp15vj9&sh=4e9c8ef1)
  * [Conda: Myths and Misconceptions](https://jakevdp.github.io/blog/2016/08/25/conda-myths-and-misconceptions/)


# Centers for Medicare & Medicaid Services (CMS) Data

  * [Synthetic Public Use Files (SynPUFs)](https://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/)
  * [Limited Data Set (LDS) Files](https://www.cms.gov/Research-Statistics-Data-and-Systems/Files-for-Order/LimitedDataSets/index.html)


# Grab Bag of Machine Learning Links

## Tools
  * [scikit-learn](http://scikit-learn.org/stable/)


## Wikipedia
  * [Machine Learning](https://en.wikipedia.org/wiki/Machine_learning)

## R2D3
  * [Trees](http://www.r2d3.us/visual-intro-to-machine-learning-part-1/)

## TopTal

  * [Machine Learning Intro](https://www.toptal.com/machine-learning/machine-learning-theory-an-introductory-primer)

  * [Clustering](https://www.toptal.com/machine-learning/clustering-algorithms)

  * [Ensemble Methods](https://www.toptal.com/machine-learning/ensemble-methods-machine-learning)


  * [Big Data Hiring Guide](https://www.toptal.com/big-data#hiring-guide)

    * [Big Data Algorithms](https://www.toptal.com/big-data#big_data_algorithms)
    * [Big Data Technologies](https://www.toptal.com/big-data#big_data_technologies)