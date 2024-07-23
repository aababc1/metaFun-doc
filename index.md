
# Welcome to  metaFun
## 

::::{grid}
:reverse:
:gutter: 2 1 1 1
:margin: 4 4 1 1

:::{grid-item}
:columns: 4

```{image} ./_static/ref_picture.jpg
:width: 150px
```
:::

:::{grid-item}
:columns: 8
:class: sd-fs-3

A Sphinx theme with a clean design, support for interactive content, and a modern book-like look and feel.
:::

::::


### metaFun : A genomic and ***meta***genomic analysis pipeline for fast and unified ***Fun***ctional searches


metaFun is implemented in Nextflow.You need Nextflow and apptainer to implement this pipeline. 

## Introduction   
metaFun is aimed at agile and scalable generation of metagenome assembled genomes and taxonomic profiling with statistical analysis. Using user  interested genomes with metadata, this pipeline enables fast comprative genomic analysis and functional annotation. 


```{figure} images/pipeline_flowchart.renew.png
---
width: 100%
figclass: margin-caption
alt: metafun_pipeline
name: myfig5
align: middle
---
Birdeye view of metaFun pipeline. This pipeline is comprised of seven workflows. For the broad application, all the workflows were enclosed into individual workflows. 
```




 ```{admonition} Here's my title
:class: warning
Here's my admonition content
```

> 1. [RAWREAD_QC](RAWREAD_QC)
> 1. [ASSEMBLY_BINNING](ASSEMBLY_BINNING)
> 1. [BIN_ASSESSMENT](BIN_ASSESSMENT)
> 1. [COMPARATIVE_ANNOTATION](COMPARATIVE_ANNOTATION)
> 1. [GENOME_ASSEMBLY](GENOME_ASSEMBLY)
> 1. [WMS_TAXONOMY](WMS_TAXONOMY)
> 1. [WMS_FUNCTION](WMS_FUNCTION)

```{raw} html
<iframe src="https://dash-mag.onrender.com" width="100%" height="1200px"></iframe>


Detailed documentation and interactive content on our assembly binning strategies can be found [here](workflows/test3.py).


Hmm what are you douing?[^sn1].
[^sn1]: Look at this!.



```{figure} images/malwang.jpg
---
figclass: margin
alt: My figure text
name: myfig4
---
Now you see me 
```






```{toctree}
:maxdepth: 2
:caption: Getting Started

Getstart/Getstart.md
Beginners/Beginners.md
Getstart/Input_preparation.md

tutorials/get-started
content/index
sections/index
components/index
reference
contributing/index
changelog
```
```{toctree}
:maxdepth: 2
:caption: metaFun workflows

workflows/workflow_list.md
workflows/RAWREAD_QC.md
workflows/ASSEMBLY_BINNING.md
workflows/BIN_ASSESSMENT.md
workflows/COMPARATIVE_ANNOTATION.md

```

```{toctree}
:maxdepth: 2
:caption: Guide for interactive visualization 

```



# Example pages

Examples pages demonstrate the visual look of this theme.

```{toctree}
:caption: Example pages
:maxdepth: 2

reference/kitchen-sink/index
reference/special-theme-elements
reference/extensions
reference/notebooks
reference/thebe
reference/blog
reference/api-numpy
reference/comments
```

# Inspiration

This theme draws inspiration and borrows design elements from the following themes:

- The [PyData Sphinx Theme](https://pydata-sphinx-theme.readthedocs.io/)
- The [Furo theme](https://pradyunsg.me/furo/)
- The [Edward Tufte CSS theme](https://edwardtufte.github.io/tufte-css/)
- [GitBook](https://docs.gitbook.com/)
- The [Tailwind CSS docs](https://tailwindcss.com/docs/installation)

[pypi-badge]: https://img.shields.io/pypi/v/sphinx-book-theme.svg
[pypi-link]: https://pypi.org/project/sphinx-book-theme
