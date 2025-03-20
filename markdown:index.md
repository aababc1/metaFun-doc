<iframe src="https://dash-mag.onrender.com" width="100%" height="1200px"></iframe>

## FAQ & Troubleshooting

### Storage Management

- **Reducing Disk Usage**: After verifying your results, you can safely delete the Nextflow `work/` directory to free up significant disk space:
  ```bash
  # Remove work directory after successful run
  rm -rf work/
  ```
  
- **Temporary Files**: HUMAnN3 creates large temporary files during processing. These are automatically stored in sample-specific `*_humann_temp` directories and can be safely deleted after analysis is complete.

### Common Issues

- **Metadata Formatting**: The most common errors come from metadata file issues:
  - Ensure your sample IDs in the metadata CSV file exactly match the prefixes of your read filenames
  - Verify that the column numbers specified with `-s/--sampleIDcolumn` and `-a/--analysiscolumn` parameters are correct
  - Check that your CSV file uses comma (,) separators and not tabs or semicolons
  
- **Database Installation**: If you encounter database-related errors, verify that you've properly installed the required databases:
  ```bash
  # Check database installation status
  (metafun) metafun -module DOWNLOAD_DB -check
  ```

- **Memory Requirements**: Some modules (especially WMS_FUNCTION and ASSEMBLY_BINNING) require significant memory. If you encounter "Out of Memory" errors:
  - Run on a machine with more RAM
  - Reduce batch sizes or process samples in smaller groups
  - For HUMAnN3, adjust the number of threads to reduce memory usage with `-p` parameter

### Getting Support

- **GitHub Issues**: For bug reports, feature requests, or support:
  - Visit the [metaFun GitHub repository](https://github.com/aababc1/metaFun)
  - Create a new issue describing your problem or request
  - Include details about your environment, command used, and error messages
  
- **Documentation**: Refer to the specific module documentation for detailed parameter descriptions and usage examples

- **Citing metaFun**: If you use metaFun in your research, please cite:
  ```
  [Citation information to be added upon publication]
  ```

```{toctree}
:maxdepth: 2
:caption: Getting Started 