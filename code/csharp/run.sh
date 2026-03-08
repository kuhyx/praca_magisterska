#!/bin/bash
# Build and run the C# shortest-path visualizer (requires .NET SDK + raylib native lib)
set -e
cd "$(dirname "$0")"
dotnet run
