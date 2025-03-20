## Interface Components

The web interface is divided into multiple tabs, each providing specialized tools for different types of taxonomic analysis.

### Main Interface Structure

![Main Interface](../images/INT_WMS_TAXONOMY_interface.png)

<span style="color:#0846FA; font-family:Arial; font-size:20px">①</span> **Master Controller Panel**: This control center allows you to:
   - Load Phyloseq objects directly from your local server by specifying file paths
   - Import additional metadata or taxonomic data for analysis
   - Set global parameters that affect all analysis modules
   - The interface automatically detects both Kraken2/Bracken and Sylph phyloseq objects in the specified directory

<span style="color:#0846FA; font-family:Arial; font-size:20px">②</span> **<span style="color:#FF0000; font-weight:bold">Master Run Analysis Button</span>**: This crucial button triggers data processing for Composition Boxplot and Composition Barplot tabs. You **must click this button** before these tabs will display results.

<span style="color:#0846FA; font-family:Arial; font-size:20px">③</span> **Sample Metadata Panel**: Displays summary information about your dataset:
   - Number of samples and their distribution across metadata categories
   - Key statistics about taxonomic diversity
   - Quick access to dataset filters

<span style="color:#0846FA; font-family:Arial; font-size:20px">④</span> **Interactive Analysis Module Selection**: The interface is organized into 7 analytical modules, each represented by a tab:
   - Composition Explorer (with 4 sub-modules)
   - Diversity Explorer (Alpha and Beta diversity analysis)
   - DAA Analyzer (Differential Abundance Analysis)
   - Each module offers specialized tools for different aspects of taxonomic analysis

<span style="color:#0846FA; font-family:Arial; font-size:20px">⑤</span> **Module-Specific UI Elements**: Each tab has its own customized interface elements:
   - Parameter selectors for statistical methods
   - Taxonomic rank filters
   - Visualization controls
   - Export options for results

### Composition Explorer

This versatile analysis module includes four distinct analytical tools:

1. **Metadata Explorer**: 
   - Visualizes the distribution of samples across metadata categories
   - Provides summary statistics for both categorical and numerical metadata
   - Helps identify patterns and potential batch effects in your experimental design

2. **Taxon Analyzer**:
   - Examines the distribution of individual taxa across metadata variables
   - Creates boxplots, scatterplots, or violin plots for selected taxa
   - Tests for statistical significance in taxon abundance differences between groups

3. **Composition Barplot**:
   - Visualizes the relative distribution of all taxonomic groups across samples
   - Samples can be ordered by metadata categories
   - Allows filtering by abundance threshold and taxonomic groups
   - Shows stacked bars representing the taxonomic composition of each sample
   - *Requires clicking the <span style="color:#FF0000; font-weight:bold">Master Run Analysis Button</span> before viewing*

4. **Composition Boxplot**:
   - For categorical metadata: Shows the distribution of dominant taxa across different categories
   - For numerical metadata: Visualizes how dominant taxa change along a numerical gradient
   - Provides statistical tests for significant differences
   - *Requires clicking the <span style="color:#FF0000; font-weight:bold">Master Run Analysis Button</span> before viewing*

### Diversity Explorer

This section features two complementary approaches to analyzing community diversity:

1. **Alpha Diversity Explorer**:
   - Calculates various diversity metrics (Shannon, Simpson, Observed richness, Chao1)
   - Shows how within-sample diversity varies across metadata categories
   - Provides statistical tests to compare diversity between groups
   - Supports correlation analysis between diversity metrics and numerical metadata

2. **Beta Diversity Explorer**:
   - Analyzes between-sample diversity using multiple distance metrics:
     - Jaccard distance (presence/absence)
     - Bray-Curtis dissimilarity (abundance-weighted)
     - Aitchison distance (compositional data analysis)
   - Supports ordination using PCoA, NMDS, t-SNE, or UMAP
   - Allows exploration at any taxonomic rank
   - Offers data transformation options (log, CLR, etc.)
   - Performs statistical testing (PERMANOVA, ANOSIM) to quantify metadata effects

### Differential Abundance Analysis

![DAA Analyzer](../images/INT_WMS_TAXONOMY_daa.png)

<span style="color:#0846FA; font-family:Arial; font-size:20px">⑥</span> **Differential Abundance Analysis**:
   - Integrates [MaAsLin2](https://github.com/biobakery/Maaslin2) for sophisticated statistical modeling
   - Supports multiple data transformations:
     - Center log-ratio (CLR) transformation
     - Log transformation
     - Relative abundance (raw data)
   - Builds linear regression models to identify significant associations between taxa and metadata
   - Works with all taxonomic ranks from phylum to species
   - Produces comprehensive statistical outputs including:
     - Effect sizes (coefficients)
     - p-values and FDR corrected q-values
     - Model fit statistics
   - Visualizes results through volcano plots, heatmaps, and effect plots

### Usage Workflow

A typical analysis workflow in the INTERACTIVE_WMS_TAXONOMY module includes:

1. Load your Phyloseq data using the Master Controller Panel
2. Click the <span style="color:#FF0000; font-weight:bold">Master Run Analysis Button</span> to process data for composition analysis
3. Use Composition Explorer to get an overview of your taxonomic profiles
4. Explore community diversity patterns using Alpha and Beta Diversity Explorers
5. Identify statistically significant associations with the Differential Abundance Analysis
6. Export results as publication-ready figures and data tables

:::{admonition} Tips for optimal performance
:class: tip

- For large datasets, focus your analysis by filtering to specific taxonomic groups of interest
- Use appropriate data transformations for compositional data (CLR for Differential Abundance Analysis)
- Consider the biological relevance of results alongside statistical significance
- Export both visualizations and raw statistical outputs for comprehensive documentation
:::

:::{admonition} Loading phyloseq objects from non-standard locations
:class: note

If your phyloseq objects are stored in a location other than the standard WMS_TAXONOMY output directory, you can:
1. Navigate to the Master Controller Panel
2. Use the file selection option to point to your specific .RDS files
3. The application will automatically validate and load compatible phyloseq objects
4. This feature is particularly useful when working with phyloseq objects created outside the metaFun pipeline
:::

### Welcome Tab

The welcome page introduces the INTERACTIVE_WMS_TAXONOMY module and provides basic instructions for navigating the interface.

### Taxonomic Composition Tab

This tab allows visualization of taxonomic profiles at different taxonomic levels:

- **Level Selection**: Choose taxonomic level (Phylum, Class, Order, Family, Genus, Species)
- **Sample Grouping**: Group samples by metadata variables
- **Visualization Options**: Bar plots, heatmaps, bubble plots, or treemaps
- **Filtering Controls**: Filter taxa by prevalence, abundance, or specific taxonomic groups
- **Download Options**: Export plots in various formats and resolutions 