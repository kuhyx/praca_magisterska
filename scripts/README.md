# Scripts Directory

This directory contains helper scripts for thesis work and data collection.

---

## Hardware Specs Script

### `get_hardware_specs.sh`

**Purpose**: Automatically retrieve hardware specifications and format them for LaTeX.

**Usage**:
```bash
cd /home/runner/work/praca_magisterska/praca_magisterska/scripts
./get_hardware_specs.sh
```

**Output**:
- Creates `hardware_specs.tex` in the current directory
- Contains LaTeX-formatted hardware information ready to copy into Chapter 4

**What it captures**:
- CPU model, cores, and threads
- GPU model and memory (if NVIDIA GPU available)
- RAM amount
- Operating system and kernel version
- Disk space

**Next steps**:
1. Run the script
2. Review the generated `hardware_specs.tex` file
3. Update Unity, Unreal Engine, and NVIDIA Nsight version numbers
4. Copy the content to `latex/tex/4-metodologia.tex`

---

## Test Scenarios Document

### `test_scenarios.md`

**Purpose**: Comprehensive guide for performance testing methodology.

**Contents**:
- Detailed test scenarios (Low, Medium, High difficulty)
- Performance metrics to capture
- Step-by-step data collection procedure
- Quality assurance checklist
- Expected outputs and timeline

**How to use**:
1. Read through the entire document before starting tests
2. Follow the procedure for each scenario
3. Use as a checklist during testing
4. Reference when writing Chapter 5 (Performance Tests)

---

## Unity Testing Helper

### `run_unity_test.sh`

**Purpose**: Interactive guide for running Unity performance tests with NVIDIA Nsight.

**Usage**:
```bash
cd /home/runner/work/praca_magisterska/praca_magisterska/scripts
./run_unity_test.sh
```

**Features**:
- Interactive prompts for scenario selection (Low/Medium/High)
- Pre-test checklist reminder
- Timed prompts for frame captures at correct intervals
- File naming conventions for organized data
- Step-by-step guidance through the testing process

**What it does**:
1. Checks if NVIDIA Nsight is installed
2. Prompts for scenario selection
3. Guides through pre-test setup
4. Provides timed reminders for 5 frame captures
5. Reminds about exporting metrics and taking screenshots

**Output organization**:
- `unity_[scenario]_capture_[1-5].nsight` - Nsight capture files
- `unity_[scenario]_capture_[1-5]_metrics.csv` - Exported metrics
- `screenshots/unity/[scenario]/*.png` - Screenshots

---

## Creating Additional Scripts

If you need to create more helper scripts, follow these conventions:

1. **Naming**: Use lowercase with underscores (e.g., `analyze_results.sh`)
2. **Permissions**: Make executable with `chmod +x script_name.sh`
3. **Documentation**: Add a section to this README explaining the script
4. **Error handling**: Include checks for required tools/files
5. **Output**: Save generated files to appropriate directories

---

## Tips for Using Scripts

1. **Run from repository root**: Most scripts assume you're in the main repository directory
2. **Check dependencies**: Scripts may require `nvidia-smi`, `lscpu`, etc.
3. **Review outputs**: Always review generated files before using them in the thesis
4. **Customize as needed**: Scripts are templates - adjust for your specific setup

---

## Troubleshooting

**"Command not found" errors**:
- Ensure the script is executable: `chmod +x script_name.sh`
- Run with explicit bash: `bash script_name.sh`

**NVIDIA tools not found**:
- Verify NVIDIA Nsight Graphics is installed
- Add to PATH or use full path to executable

**Permission denied**:
- Scripts need execute permission: `chmod +x script_name.sh`
- May need to run some system info commands with appropriate permissions

---

**Last updated**: January 14, 2026
