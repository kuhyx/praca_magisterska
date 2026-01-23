#!/usr/bin/env python3
"""
Nsight Profiling Results Analyzer
=================================
Analyzes NVIDIA Nsight Systems profiling data and generates LaTeX output
for the master's thesis comparing Unity and Unreal Engine performance.

Usage:
    python analyze_nsight.py [--output OUTPUT_TEX] [--data-dir DATA_DIR]

Example:
    python analyze_nsight.py --output latex/tex/wyniki-nsight.tex
"""

import argparse
import csv
import os
import sqlite3
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class ProfilingResult:
    """Container for profiling results from a single run."""
    name: str
    engine: str
    duration_seconds: float
    total_frames: int
    avg_fps: float
    report_path: str
    sqlite_path: Optional[str]
    vulkan_csv_path: Optional[str]
    osrt_csv_path: Optional[str]


@dataclass
class VulkanApiCall:
    """Single Vulkan API call statistics."""
    name: str
    time_percent: float
    total_time_ns: int
    num_calls: int
    avg_time_ns: float
    min_time_ns: int
    max_time_ns: int


@dataclass
class OsRuntimeCall:
    """Single OS runtime call statistics."""
    name: str
    time_percent: float
    total_time_ns: int
    num_calls: int
    avg_time_ns: float
    min_time_ns: int
    max_time_ns: int


class NsightAnalyzer:
    """Analyzes Nsight profiling data and generates LaTeX output."""

    def __init__(self, data_dir: str):
        self.data_dir = Path(data_dir)
        self.results: list[ProfilingResult] = []
        self.vulkan_calls: dict[str, list[VulkanApiCall]] = {}
        self.osrt_calls: dict[str, list[OsRuntimeCall]] = {}

    def discover_reports(self) -> list[str]:
        """Find all .nsys-rep files in the data directory."""
        reports = []
        for f in self.data_dir.glob("**/*.nsys-rep"):
            reports.append(str(f))
        return sorted(reports)

    def parse_vulkan_csv(self, csv_path: str) -> list[VulkanApiCall]:
        """Parse Vulkan API summary CSV file."""
        calls = []
        try:
            with open(csv_path, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        calls.append(VulkanApiCall(
                            name=row.get('Name', row.get('name', '')),
                            time_percent=float(row.get('Time (%)', row.get('time_percent', 0))),
                            total_time_ns=int(row.get('Total Time (ns)', row.get('total_time', 0))),
                            num_calls=int(row.get('Num Calls', row.get('num_calls', 0))),
                            avg_time_ns=float(row.get('Avg (ns)', row.get('avg_time', 0))),
                            min_time_ns=int(row.get('Min (ns)', row.get('min_time', 0))),
                            max_time_ns=int(row.get('Max (ns)', row.get('max_time', 0))),
                        ))
                    except (ValueError, KeyError) as e:
                        continue
        except FileNotFoundError:
            print(f"Warning: CSV file not found: {csv_path}")
        return calls

    def parse_osrt_csv(self, csv_path: str) -> list[OsRuntimeCall]:
        """Parse OS Runtime summary CSV file."""
        calls = []
        try:
            with open(csv_path, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        calls.append(OsRuntimeCall(
                            name=row.get('Name', row.get('name', '')),
                            time_percent=float(row.get('Time (%)', row.get('time_percent', 0))),
                            total_time_ns=int(row.get('Total Time (ns)', row.get('total_time', 0))),
                            num_calls=int(row.get('Num Calls', row.get('num_calls', 0))),
                            avg_time_ns=float(row.get('Avg (ns)', row.get('avg_time', 0))),
                            min_time_ns=int(row.get('Min (ns)', row.get('min_time', 0))),
                            max_time_ns=int(row.get('Max (ns)', row.get('max_time', 0))),
                        ))
                    except (ValueError, KeyError):
                        continue
        except FileNotFoundError:
            print(f"Warning: CSV file not found: {csv_path}")
        return calls

    def get_frame_count_from_sqlite(self, sqlite_path: str) -> int:
        """Extract frame count from SQLite database."""
        try:
            conn = sqlite3.connect(sqlite_path)
            cursor = conn.cursor()
            # Count vkQueuePresentKHR calls (each = 1 frame)
            cursor.execute("""
                SELECT COUNT(*) FROM VULKAN_API 
                WHERE nameId IN (
                    SELECT id FROM StringIds WHERE value='vkQueuePresentKHR'
                )
            """)
            result = cursor.fetchone()
            conn.close()
            return result[0] if result else 0
        except Exception as e:
            print(f"Warning: Could not read SQLite: {e}")
            return 0

    def get_frame_times_from_sqlite(self, sqlite_path: str) -> list[float]:
        """Extract individual frame times from SQLite database."""
        frame_times = []
        try:
            conn = sqlite3.connect(sqlite_path)
            cursor = conn.cursor()
            # Get timestamps of vkQueuePresentKHR calls
            cursor.execute("""
                SELECT start FROM VULKAN_API 
                WHERE nameId IN (
                    SELECT id FROM StringIds WHERE value='vkQueuePresentKHR'
                )
                ORDER BY start
            """)
            timestamps = [row[0] for row in cursor.fetchall()]
            conn.close()
            
            # Calculate frame times (differences between presents)
            for i in range(1, len(timestamps)):
                frame_time_ns = timestamps[i] - timestamps[i-1]
                frame_times.append(frame_time_ns / 1_000_000)  # Convert to ms
        except Exception as e:
            print(f"Warning: Could not extract frame times: {e}")
        return frame_times

    def analyze_report(self, report_path: str) -> Optional[ProfilingResult]:
        """Analyze a single Nsight report file."""
        report_path = Path(report_path)
        base_name = report_path.stem
        
        # Determine engine from filename
        if 'unity' in base_name.lower():
            engine = 'Unity'
        elif 'unreal' in base_name.lower():
            engine = 'Unreal Engine'
        else:
            engine = 'Unknown'

        # Find associated files
        sqlite_path = report_path.with_suffix('.sqlite')
        
        # Look for CSV files with various naming patterns
        vulkan_csv = None
        osrt_csv = None
        
        for pattern in [f"{base_name}_vulkan*sum*.csv", f"{base_name}*vulkan*.csv"]:
            matches = list(self.data_dir.glob(pattern))
            if matches:
                vulkan_csv = str(matches[0])
                break
                
        for pattern in [f"{base_name}_osrt*sum*.csv", f"{base_name}*osrt*.csv"]:
            matches = list(self.data_dir.glob(pattern))
            if matches:
                osrt_csv = str(matches[0])
                break

        # Extract duration from filename if present (e.g., unity_full_95s)
        duration = 95  # default
        import re
        match = re.search(r'(\d+)s', base_name)
        if match:
            duration = int(match.group(1))

        # Get frame count
        frames = 0
        if sqlite_path.exists():
            frames = self.get_frame_count_from_sqlite(str(sqlite_path))

        fps = frames / duration if duration > 0 else 0

        result = ProfilingResult(
            name=base_name,
            engine=engine,
            duration_seconds=duration,
            total_frames=frames,
            avg_fps=fps,
            report_path=str(report_path),
            sqlite_path=str(sqlite_path) if sqlite_path.exists() else None,
            vulkan_csv_path=vulkan_csv,
            osrt_csv_path=osrt_csv,
        )

        # Parse CSV files
        if vulkan_csv:
            self.vulkan_calls[base_name] = self.parse_vulkan_csv(vulkan_csv)
        if osrt_csv:
            self.osrt_calls[base_name] = self.parse_osrt_csv(osrt_csv)

        return result

    def analyze_all(self):
        """Analyze all discovered reports."""
        reports = self.discover_reports()
        print(f"Found {len(reports)} Nsight report(s)")
        
        for report in reports:
            print(f"  Analyzing: {os.path.basename(report)}")
            result = self.analyze_report(report)
            if result:
                self.results.append(result)

    def format_time_ns(self, ns: float) -> str:
        """Format nanoseconds to human readable string."""
        if ns >= 1_000_000_000:
            return f"{ns / 1_000_000_000:.2f} s"
        elif ns >= 1_000_000:
            return f"{ns / 1_000_000:.2f} ms"
        elif ns >= 1_000:
            return f"{ns / 1_000:.2f} μs"
        else:
            return f"{ns:.0f} ns"

    def generate_latex(self) -> str:
        """Generate LaTeX document with analysis results."""
        lines = []
        
        # Header
        lines.append("% =============================================================================")
        lines.append("% Wyniki profilowania NVIDIA Nsight Systems")
        lines.append(f"% Wygenerowano automatycznie: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("% =============================================================================")
        lines.append("")
        
        # Section header
        lines.append("\\section{Wyniki profilowania NVIDIA Nsight Systems}")
        lines.append("\\label{sec:wyniki-nsight}")
        lines.append("")
        
        lines.append("W niniejszej sekcji przedstawiono wyniki profilowania wydajności")
        lines.append("przeprowadzonego przy użyciu narzędzia NVIDIA Nsight Systems.")
        lines.append("Profilowanie obejmowało analizę wywołań API Vulkan oraz funkcji")
        lines.append("systemowych (OS Runtime).")
        lines.append("")
        
        # Performance summary table
        if self.results:
            lines.append("\\subsection{Podsumowanie wydajności}")
            lines.append("\\label{subsec:nsight-podsumowanie}")
            lines.append("")
            lines.append("Tabela~\\ref{tab:nsight-summary} przedstawia podsumowanie")
            lines.append("wyników profilowania dla poszczególnych testów.")
            lines.append("")
            lines.append("\\begin{table}[htbp]")
            lines.append("\\centering")
            lines.append("\\caption{Podsumowanie wyników profilowania Nsight}")
            lines.append("\\label{tab:nsight-summary}")
            lines.append("\\begin{tabular}{|l|c|c|c|c|}")
            lines.append("\\hline")
            lines.append("\\textbf{Test} & \\textbf{Silnik} & \\textbf{Czas [s]} & \\textbf{Klatki} & \\textbf{Śr. FPS} \\\\")
            lines.append("\\hline")
            
            for r in self.results:
                name_escaped = r.name.replace('_', '\\_')
                lines.append(f"{name_escaped} & {r.engine} & {r.duration_seconds:.0f} & {r.total_frames} & {r.avg_fps:.2f} \\\\")
            
            lines.append("\\hline")
            lines.append("\\end{tabular}")
            lines.append("\\end{table}")
            lines.append("")

        # Vulkan API analysis
        for result in self.results:
            if result.name in self.vulkan_calls and self.vulkan_calls[result.name]:
                calls = self.vulkan_calls[result.name]
                
                lines.append(f"\\subsection{{Analiza wywołań Vulkan API -- {result.engine}}}")
                lines.append(f"\\label{{subsec:vulkan-{result.name.replace('_', '-')}}}")
                lines.append("")
                
                lines.append(f"Podczas {result.duration_seconds:.0f}-sekundowego testu zarejestrowano")
                total_calls = sum(c.num_calls for c in calls)
                lines.append(f"łącznie {total_calls:,} wywołań API Vulkan.".replace(',', '\\,'))
                lines.append("")
                
                # Top 10 by time
                top_by_time = sorted(calls, key=lambda x: x.time_percent, reverse=True)[:10]
                
                lines.append("\\begin{table}[htbp]")
                lines.append("\\centering")
                lines.append("\\caption{Najczęstsze wywołania Vulkan API według czasu wykonania}")
                lines.append(f"\\label{{tab:vulkan-time-{result.name.replace('_', '-')}}}")
                lines.append("\\begin{tabular}{|l|r|r|r|r|}")
                lines.append("\\hline")
                lines.append("\\textbf{Funkcja} & \\textbf{Czas [\\%]} & \\textbf{Wywołania} & \\textbf{Śr. czas} & \\textbf{Maks. czas} \\\\")
                lines.append("\\hline")
                
                for call in top_by_time:
                    name = call.name.replace('_', '\\_')
                    avg_time = self.format_time_ns(call.avg_time_ns)
                    max_time = self.format_time_ns(call.max_time_ns)
                    num_calls = f"{call.num_calls:,}".replace(',', '\\,')
                    lines.append(f"{name} & {call.time_percent:.1f} & {num_calls} & {avg_time} & {max_time} \\\\")
                
                lines.append("\\hline")
                lines.append("\\end{tabular}")
                lines.append("\\end{table}")
                lines.append("")
                
                # Analysis text
                if top_by_time:
                    top_call = top_by_time[0]
                    lines.append(f"Dominującą funkcją pod względem czasu wykonania jest")
                    lines.append(f"\\texttt{{{top_call.name.replace('_', '\\_')}}}, która zajmuje")
                    lines.append(f"{top_call.time_percent:.1f}\\% całkowitego czasu profilowania.")
                    
                    if 'WaitForFences' in top_call.name:
                        lines.append("Funkcja ta odpowiada za synchronizację CPU z GPU,")
                        lines.append("co wskazuje na to, że aplikacja jest ograniczona przez GPU")
                        lines.append("(ang. \\textit{GPU-bound}).")
                    elif 'QueuePresent' in top_call.name:
                        lines.append("Funkcja ta odpowiada za prezentację wyrenderowanej klatki,")
                        lines.append("co jest oczekiwane w aplikacji graficznej.")
                    lines.append("")

        # OS Runtime analysis
        for result in self.results:
            if result.name in self.osrt_calls and self.osrt_calls[result.name]:
                calls = self.osrt_calls[result.name]
                
                lines.append(f"\\subsection{{Analiza wywołań systemowych -- {result.engine}}}")
                lines.append(f"\\label{{subsec:osrt-{result.name.replace('_', '-')}}}")
                lines.append("")
                
                total_calls = sum(c.num_calls for c in calls)
                lines.append(f"Zarejestrowano {total_calls:,} wywołań funkcji systemowych.".replace(',', '\\,'))
                lines.append("")
                
                # Top 10 by time
                top_by_time = sorted(calls, key=lambda x: x.time_percent, reverse=True)[:10]
                
                lines.append("\\begin{table}[htbp]")
                lines.append("\\centering")
                lines.append("\\caption{Najczęstsze wywołania systemowe według czasu wykonania}")
                lines.append(f"\\label{{tab:osrt-time-{result.name.replace('_', '-')}}}")
                lines.append("\\begin{tabular}{|l|r|r|r|r|}")
                lines.append("\\hline")
                lines.append("\\textbf{Funkcja} & \\textbf{Czas [\\%]} & \\textbf{Wywołania} & \\textbf{Śr. czas} & \\textbf{Maks. czas} \\\\")
                lines.append("\\hline")
                
                for call in top_by_time:
                    name = call.name.replace('_', '\\_')
                    avg_time = self.format_time_ns(call.avg_time_ns)
                    max_time = self.format_time_ns(call.max_time_ns)
                    num_calls = f"{call.num_calls:,}".replace(',', '\\,')
                    lines.append(f"{name} & {call.time_percent:.1f} & {num_calls} & {avg_time} & {max_time} \\\\")
                
                lines.append("\\hline")
                lines.append("\\end{tabular}")
                lines.append("\\end{table}")
                lines.append("")
                
                # Analysis text
                if top_by_time:
                    top_call = top_by_time[0]
                    lines.append(f"Najczęściej wywoływaną funkcją systemową jest")
                    lines.append(f"\\texttt{{{top_call.name.replace('_', '\\_')}}}, zajmująca")
                    lines.append(f"{top_call.time_percent:.1f}\\% czasu.")
                    
                    if 'futex' in top_call.name.lower():
                        lines.append("Jest to mechanizm synchronizacji wątków w systemie Linux,")
                        lines.append("co wskazuje na intensywne wykorzystanie wielowątkowości")
                        lines.append("przez silnik gry.")
                    elif 'pthread' in top_call.name.lower():
                        lines.append("Funkcje pthread odpowiadają za zarządzanie wątkami POSIX,")
                        lines.append("co potwierdza wielowątkową architekturę silnika.")
                    lines.append("")

        # Frame time analysis (if SQLite available)
        for result in self.results:
            if result.sqlite_path and os.path.exists(result.sqlite_path):
                frame_times = self.get_frame_times_from_sqlite(result.sqlite_path)
                
                if frame_times:
                    lines.append(f"\\subsection{{Analiza czasów klatek -- {result.engine}}}")
                    lines.append(f"\\label{{subsec:frametime-{result.name.replace('_', '-')}}}")
                    lines.append("")
                    
                    import statistics
                    avg_ft = statistics.mean(frame_times)
                    min_ft = min(frame_times)
                    max_ft = max(frame_times)
                    std_ft = statistics.stdev(frame_times) if len(frame_times) > 1 else 0
                    
                    # Calculate percentiles
                    sorted_ft = sorted(frame_times)
                    p1 = sorted_ft[int(len(sorted_ft) * 0.01)] if len(sorted_ft) > 100 else min_ft
                    p99 = sorted_ft[int(len(sorted_ft) * 0.99)] if len(sorted_ft) > 100 else max_ft
                    
                    lines.append("\\begin{table}[htbp]")
                    lines.append("\\centering")
                    lines.append("\\caption{Statystyki czasów klatek}")
                    lines.append(f"\\label{{tab:frametime-stats-{result.name.replace('_', '-')}}}")
                    lines.append("\\begin{tabular}{|l|r|}")
                    lines.append("\\hline")
                    lines.append("\\textbf{Metryka} & \\textbf{Wartość} \\\\")
                    lines.append("\\hline")
                    lines.append(f"Liczba klatek & {len(frame_times)} \\\\")
                    lines.append(f"Średni czas klatki & {avg_ft:.2f} ms \\\\")
                    lines.append(f"Minimalny czas klatki & {min_ft:.2f} ms \\\\")
                    lines.append(f"Maksymalny czas klatki & {max_ft:.2f} ms \\\\")
                    lines.append(f"Odchylenie standardowe & {std_ft:.2f} ms \\\\")
                    lines.append(f"1. percentyl & {p1:.2f} ms \\\\")
                    lines.append(f"99. percentyl & {p99:.2f} ms \\\\")
                    lines.append(f"Średnia liczba FPS & {1000/avg_ft:.2f} \\\\")
                    lines.append("\\hline")
                    lines.append("\\end{tabular}")
                    lines.append("\\end{table}")
                    lines.append("")
                    
                    # Stability analysis
                    cv = (std_ft / avg_ft) * 100 if avg_ft > 0 else 0
                    lines.append(f"Współczynnik zmienności czasów klatek wynosi {cv:.1f}\\%,")
                    if cv < 5:
                        lines.append("co wskazuje na bardzo stabilną wydajność renderowania.")
                    elif cv < 15:
                        lines.append("co wskazuje na stabilną wydajność z niewielkimi wahaniami.")
                    else:
                        lines.append("co wskazuje na znaczne wahania wydajności.")
                    lines.append("")

        # Summary section
        lines.append("\\subsection{Podsumowanie analizy profilowania}")
        lines.append("\\label{subsec:nsight-wnioski}")
        lines.append("")
        
        if self.results:
            unity_results = [r for r in self.results if r.engine == 'Unity']
            unreal_results = [r for r in self.results if r.engine == 'Unreal Engine']
            
            if unity_results:
                avg_unity_fps = sum(r.avg_fps for r in unity_results) / len(unity_results)
                lines.append(f"Silnik Unity osiągnął średnią wydajność {avg_unity_fps:.2f} FPS")
                lines.append(f"w przeprowadzonych testach.")
                lines.append("")
            
            if unreal_results:
                avg_unreal_fps = sum(r.avg_fps for r in unreal_results) / len(unreal_results)
                lines.append(f"Silnik Unreal Engine osiągnął średnią wydajność {avg_unreal_fps:.2f} FPS")
                lines.append(f"w przeprowadzonych testach.")
                lines.append("")
            
            if unity_results and unreal_results:
                diff = avg_unity_fps - avg_unreal_fps
                if abs(diff) > 5:
                    better = "Unity" if diff > 0 else "Unreal Engine"
                    lines.append(f"Silnik {better} wykazał lepszą wydajność w przeprowadzonych testach,")
                    lines.append(f"osiągając o {abs(diff):.1f} FPS więcej.")
                else:
                    lines.append("Oba silniki wykazały zbliżoną wydajność w przeprowadzonych testach.")
                lines.append("")

        lines.append("% Koniec sekcji wyników Nsight")
        lines.append("")
        
        return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Analyze Nsight profiling data and generate LaTeX output'
    )
    parser.add_argument(
        '--data-dir', '-d',
        default='data/nsight',
        help='Directory containing Nsight data files (default: data/nsight)'
    )
    parser.add_argument(
        '--output', '-o',
        default='latex/tex/wyniki-nsight.tex',
        help='Output LaTeX file path (default: latex/tex/wyniki-nsight.tex)'
    )
    parser.add_argument(
        '--print', '-p',
        action='store_true',
        help='Print LaTeX to stdout instead of writing to file'
    )
    
    args = parser.parse_args()
    
    # Find project root
    script_dir = Path(__file__).parent
    project_dir = script_dir.parent
    
    data_dir = project_dir / args.data_dir
    output_path = project_dir / args.output
    
    if not data_dir.exists():
        print(f"Error: Data directory not found: {data_dir}")
        sys.exit(1)
    
    print(f"Nsight Profiling Analyzer")
    print(f"=" * 50)
    print(f"Data directory: {data_dir}")
    print(f"Output file:    {output_path}")
    print()
    
    analyzer = NsightAnalyzer(str(data_dir))
    analyzer.analyze_all()
    
    if not analyzer.results:
        print("Warning: No profiling results found!")
        sys.exit(1)
    
    print()
    print("Generating LaTeX output...")
    latex_content = analyzer.generate_latex()
    
    if args.print:
        print()
        print(latex_content)
    else:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(latex_content)
        print(f"LaTeX output written to: {output_path}")
    
    print()
    print("Done!")


if __name__ == '__main__':
    main()
