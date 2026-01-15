#!/bin/bash
# Script to retrieve hardware specifications and format for LaTeX

echo "Gathering hardware specifications..."
echo ""

# Create output file
OUTPUT_FILE="hardware_specs.tex"

cat > "$OUTPUT_FILE" << 'LATEX_EOF'
% Hardware Specifications for Thesis
% Generated automatically - use in Chapter 4 Methodology

\subsection{Środowisko testowe}
\label{subsec:srodowisko-testowe}

Wszystkie testy wydajnościowe przeprowadzono na komputerze o następującej specyfikacji:

\begin{itemize}
LATEX_EOF

# Get CPU info
echo "Retrieving CPU information..."
CPU_MODEL=$(lscpu | grep "Model name" | cut -d':' -f2 | xargs)
CPU_CORES=$(lscpu | grep "^CPU(s):" | cut -d':' -f2 | xargs)
CPU_THREADS=$(lscpu | grep "Thread(s) per core" | cut -d':' -f2 | xargs)
TOTAL_THREADS=$((CPU_CORES * CPU_THREADS))

if [ -n "$CPU_MODEL" ]; then
    echo "    \\item \\textbf{Procesor}: $CPU_MODEL ($CPU_CORES rdzeni, $TOTAL_THREADS wątków)" >> "$OUTPUT_FILE"
fi

# Get GPU info
echo "Retrieving GPU information..."
if command -v nvidia-smi &> /dev/null; then
    GPU_MODEL=$(nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null | head -1)
    GPU_MEMORY=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits 2>/dev/null | head -1)
    DRIVER_VERSION=$(nvidia-smi --query-gpu=driver_version --format=csv,noheader 2>/dev/null | head -1)
    
    if [ -n "$GPU_MODEL" ]; then
        echo "    \\item \\textbf{Karta graficzna}: NVIDIA $GPU_MODEL" >> "$OUTPUT_FILE"
        if [ -n "$GPU_MEMORY" ]; then
            GPU_MEMORY_GB=$((GPU_MEMORY / 1024))
            echo "    \\item \\textbf{Pamięć GPU}: ${GPU_MEMORY_GB} GB GDDR" >> "$OUTPUT_FILE"
        fi
        if [ -n "$DRIVER_VERSION" ]; then
            echo "    \\item \\textbf{Sterowniki NVIDIA}: wersja $DRIVER_VERSION" >> "$OUTPUT_FILE"
        fi
    fi
else
    echo "    \\item \\textbf{Karta graficzna}: [Uruchom skrypt z dostępem do nvidia-smi]" >> "$OUTPUT_FILE"
fi

# Get RAM info
echo "Retrieving RAM information..."
RAM_TOTAL=$(free -h | grep "Mem:" | awk '{print $2}')
if [ -n "$RAM_TOTAL" ]; then
    echo "    \\item \\textbf{Pamięć RAM}: $RAM_TOTAL" >> "$OUTPUT_FILE"
fi

# Get OS info
echo "Retrieving OS information..."
if [ -f /etc/os-release ]; then
    OS_NAME=$(grep "^PRETTY_NAME=" /etc/os-release | cut -d'"' -f2)
    KERNEL_VERSION=$(uname -r)
    echo "    \\item \\textbf{System operacyjny}: $OS_NAME (jądro Linux $KERNEL_VERSION)" >> "$OUTPUT_FILE"
fi

# Get storage info
echo "Retrieving storage information..."
DISK_INFO=$(df -h / | tail -1 | awk '{print $2}')
if [ -n "$DISK_INFO" ]; then
    echo "    \\item \\textbf{Dysk}: $DISK_INFO całkowita pojemność" >> "$OUTPUT_FILE"
fi

# Close LaTeX itemize
cat >> "$OUTPUT_FILE" << 'LATEX_EOF'
\end{itemize}

\subsubsection{Wersje oprogramowania}

\begin{itemize}
    \item \textbf{Unity}: [Wpisz wersję, np. 2022.3.15f1 LTS]
    \item \textbf{Unreal Engine}: [Wpisz wersję, np. 5.3.2]
    \item \textbf{NVIDIA Nsight Graphics}: [Wpisz wersję po instalacji]
\end{itemize}

\subsubsection{Konfiguracja testowa}

Przed wykonaniem każdego testu:
\begin{enumerate}
    \item Zamknięto wszystkie aplikacje działające w tle
    \item Wyłączono automatyczne aktualizacje systemu
    \item Ustawiono tryb wydajności zasilania
    \item Odczekano 5 minut na stabilizację systemu
    \item Wykonano 3 pomiary dla każdego scenariusza testowego
\end{enumerate}
LATEX_EOF

echo ""
echo "✓ Hardware specifications saved to: $OUTPUT_FILE"
echo ""
echo "To use in your thesis:"
echo "1. Review and update Unity/Unreal/Nsight versions"
echo "2. Copy the content to latex/tex/4-metodologia.tex"
echo "3. Adjust any details as needed"
echo ""
cat "$OUTPUT_FILE"
