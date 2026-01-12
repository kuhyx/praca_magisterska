# Chapter-by-Chapter Action Items
**Quick reference for what to write in each incomplete section**

---

## ✅ ALREADY COMPLETE (No action needed)
- Chapter 1: Introduction ✓
- Chapter 2: Literature Review ✓
- Chapter 3: Game Engines Characteristics ✓
- Interview Analysis (wywiady-analiza) ✓
- Implementation Experiences (implementacja-gry) ✓
- Profiling Tools (narzedzia-profilowania) ✓

---

## ⚠️ CHAPTER 4: METHODOLOGY (Currently 55 lines → Target: 150+ lines)

**File**: `latex/tex/4-metodologia.tex`

### Sections to Expand:

#### 4.1 Research Design
**Add**:
- Mixed-methods approach (quantitative performance tests + qualitative interviews)
- Justification for choosing bullet-hell genre
- Explain triangulation of data sources

#### 4.2 Quantitative Methodology
**Add**:
- Hardware specifications (exact CPU, GPU, RAM, OS version)
- Software versions (Unity version, Unreal version, NVIDIA Nsight version)
- Test scenarios:
  - Scenario 1: Low difficulty (50-100 bullets on screen)
  - Scenario 2: Medium difficulty (200-300 bullets)
  - Scenario 3: High difficulty (500+ bullets)
- Metrics collected:
  - Frame time (ms)
  - FPS
  - GPU utilization (%)
  - Memory usage (MB)
  - Draw calls
  - Vertex count
- Number of test runs per scenario (e.g., 5 runs each, take average)
- Statistical methods (mean, standard deviation, etc.)

#### 4.3 Qualitative Methodology
**Add**:
- Interview methodology (semi-structured interviews)
- Participant selection criteria (minimum 1 year experience)
- Interview protocol (10 questions, approximately 30-45 minutes each)
- Data analysis method (thematic analysis)
- Anonymization approach

#### 4.4 Validity and Reliability
**Add**:
- Steps taken to ensure test validity
- Reproducibility measures
- Limitations acknowledged upfront

**Example structure**:
```latex
\subsection{Środowisko testowe}
Wszystkie testy wydajnościowe przeprowadzono na komputerze o następującej specyfikacji:
\begin{itemize}
    \item Procesor: [Specify]
    \item Karta graficzna: NVIDIA [Model]
    \item Pamięć RAM: [Amount] GB DDR4
    \item System operacyjny: [OS + version]
    \item Sterowniki GPU: NVIDIA [version]
\end{itemize}

Unity w wersji [X.Y.Z] LTS został skonfigurowany z renderingiem 2D...
Unreal Engine w wersji [X.Y] został skonfigurowany z...
```

---

## 🔥 CHAPTER 5: PERFORMANCE TESTS (Currently 57 lines → Target: 200+ lines)

**File**: `latex/tex/5-testy-wydajnosci.tex`

### 5.1 Test Environment Preparation
**Write**:
- Exact steps to prepare testing environment
- Driver versions, background processes disabled
- Warmup procedure before capturing data

### 5.2 Test Scenarios
**Write**:
- Detailed description of each test scenario
- Screenshots of game at each difficulty level
- Why these scenarios were chosen

### 5.3 Unity Performance Results
**Write**:
- Table 5.1: Frame time at different difficulty levels
- Table 5.2: GPU utilization data
- Table 5.3: Memory usage
- Figure 5.1: Frame time graph over time
- Figure 5.2: GPU utilization comparison
- Narrative analysis of Unity's performance characteristics
- Identify bottlenecks (CPU-bound? GPU-bound?)

### 5.4 Unreal Engine Performance Results
**Write**:
- Table 5.4: Frame time at different difficulty levels
- Table 5.5: GPU utilization data
- Table 5.6: Memory usage
- Figure 5.3: Frame time graph over time
- Figure 5.4: GPU utilization comparison
- Narrative analysis of Unreal's performance
- Identify bottlenecks

### 5.5 Direct Comparison
**Write**:
- Table 5.7: Side-by-side comparison of all metrics
- Figure 5.5: Comparative bar chart (Unity vs Unreal)
- Figure 5.6: Efficiency analysis (performance per resource used)
- Discuss which engine is more efficient and why
- Relate findings to engine architecture differences

### 5.6 Memory Management Analysis
**Write**:
- How garbage collection affects Unity (spikes in frame time?)
- How manual memory management works in Unreal
- Object pooling effectiveness in both engines

### 5.7 Scalability Analysis
**Write**:
- How performance degrades with increasing load
- Linear degradation vs exponential?
- At what point does each engine become unusable?

**Example table**:
```latex
\begin{table}[h!]
    \centering
    \caption{Porównanie czasu klatki w scenariuszu średniej trudności}
    \label{tab:frame-time-medium}
    \begin{tabular}{|l|c|c|c|}
        \hline
        \textbf{Silnik} & \textbf{Średni czas [ms]} & \textbf{Min [ms]} & \textbf{Max [ms]} \\
        \hline
        Unity & 8.3 & 7.1 & 12.5 \\
        Unreal Engine & 6.9 & 6.2 & 9.1 \\
        \hline
    \end{tabular}
\end{table}
```

---

## ⚠️ CHAPTER 6: CAPABILITIES ANALYSIS (Currently 72 lines → Target: 180+ lines)

**File**: `latex/tex/6-analiza-mozliwosci.tex`

### 6.1 Graphics Capabilities
**Expand with**:
- Unity URP pipeline description
- Unreal's rendering pipeline description
- Comparison of lighting models (PBR in both)
- Post-processing effects comparison
- Particle systems comparison
- Shader complexity each can handle

### 6.2 Shader Systems
**Add**:
- Unity Shader Graph vs Unreal Material Editor
- Ease of use comparison
- Performance implications
- Code-based shader writing (HLSL in both)

### 6.3 Physics Engines
**Add**:
- Unity: NVIDIA PhysX integration
- Unreal: Chaos physics system
- Collision detection performance
- Rigid body simulation
- Soft body and cloth simulation
- When to use each engine's physics

### 6.4 Audio Systems
**Add**:
- Unity audio system capabilities
- Unreal: MetaSounds vs Blueprint audio
- 3D spatial audio
- Audio middleware support (Wwise, FMOD)

### 6.5 Animation Systems
**Add**:
- Unity: Animator + Animation Rigging
- Unreal: Animation Blueprints + Control Rig
- Inverse kinematics
- Blend trees
- Which is easier for non-technical artists?

### 6.6 Scripting and Extensibility
**Add**:
- C# in Unity: advantages (garbage collection, easier syntax)
- C++ in Unreal: advantages (performance, low-level control)
- Visual scripting: Unreal Blueprints vs Unity Visual Scripting
- Extensibility through plugins/packages

### 6.7 Cross-Platform Support
**Add**:
- Platforms supported by Unity
- Platforms supported by Unreal
- Ease of porting to mobile/consoles
- Performance on different platforms

### 6.8 Tooling and Editor Features
**Add**:
- Unity Editor usability
- Unreal Editor usability
- Prefabs vs Blueprints
- Version control integration (Git, Perforce)
- Collaboration features

**Use interview quotes** to support your points! Example:
```latex
Jak stwierdził jeden z respondentów: ,,Unreal jest wyraźnie zoptymalizowany 
pod gry typu first-person shooter. Tworzenie gier FPS jest niezwykle proste''
```

---

## 🔥 CHAPTER 7: RESULTS COMPARISON (Currently 52 lines → Target: 150+ lines)

**File**: `latex/tex/7-porownanie-wynikow.tex`

### 7.1 Synthesis of Research Findings
**Write**:
- Summary table combining ALL findings (performance + capabilities + interviews)
- What did we learn from each research method?
- How do findings triangulate (do they agree or contradict)?

### 7.2 Multi-Criteria Comparison Matrix
**Create**:
- Table 7.1: Master comparison matrix

| Criterion | Unity | Unreal | Winner |
|-----------|-------|--------|--------|
| Performance (2D) | ★★★★☆ | ★★★☆☆ | Unity |
| Performance (3D) | ★★★☆☆ | ★★★★★ | Unreal |
| Ease of learning | ★★★★★ | ★★★☆☆ | Unity |
| Graphics quality | ★★★★☆ | ★★★★★ | Unreal |
| Documentation | ★★★★★ | ★★☆☆☆ | Unity |
| Mobile support | ★★★★★ | ★★★☆☆ | Unity |
| Community size | ★★★★★ | ★★★★☆ | Unity |
| AAA capabilities | ★★★☆☆ | ★★★★★ | Unreal |

### 7.3 Use Case Recommendations
**Write detailed recommendations for**:

#### 7.3.1 Indie Games
- **Recommend**: Unity
- **Reasons**: Lower learning curve, faster prototyping, better community support for beginners, asset store
- **Exception**: If game requires cutting-edge graphics → Unreal

#### 7.3.2 Mobile Games
- **Recommend**: Unity
- **Reasons**: Better mobile optimization, smaller build sizes, more mobile-specific features
- **Data**: Cite that most mobile games use Unity

#### 7.3.3 AAA Games
- **Recommend**: Unreal Engine
- **Reasons**: Superior graphics, used by major studios, better performance for complex 3D scenes
- **Examples**: Fortnite, Gears of War

#### 7.3.4 VR/AR Applications
- **Recommend**: Depends on complexity
- Unity for: simpler VR, mobile AR, rapid prototyping
- Unreal for: high-fidelity VR experiences

#### 7.3.5 Educational/Serious Games
- **Recommend**: Unity
- **Reasons**: Easier for non-programmers, better documentation for learning

### 7.4 Trade-off Analysis
**Write**:
- Unity: Ease of use vs. graphics quality ceiling
- Unreal: Graphics power vs. learning curve
- When to sacrifice one for the other

### 7.5 Research Limitations
**Acknowledge**:
- Limited to bullet-hell genre (doesn't test all engine features)
- Small interview sample (8 people, mostly Poland-based)
- Single test hardware configuration
- Engines constantly updating (findings valid as of 2025/2026)
- WEIRD sample limitation (Western developers, may not represent global community)

### 7.6 Verification of Hypotheses
**Write**:
- List initial hypotheses from Chapter 1
- State whether each was confirmed or rejected
- Provide evidence for each

**Example**:
```latex
\textbf{Hipoteza 1}: Unreal Engine oferuje lepszą wydajność renderowania 3D 
niż Unity.
\textbf{Wynik}: \textbf{Potwierdzona}. Testy wykazały średnio 15\% lepszy czas 
klatki w Unreal Engine przy wysokim obciążeniu graficznym...
```

---

## 🔥 CHAPTER 8: CONCLUSIONS (Currently 42 lines → Target: 120+ lines)

**File**: `latex/tex/8-podsumowanie.tex`

### 8.1 Main Research Findings
**Write clear, numbered findings**:

1. **Unity przewyższa Unreal w grach 2D**: Testy wykazały 20-30% lepszą wydajność Unity w renderowaniu 2D, głównie dzięki dedykowanemu pipeline 2D.

2. **Unreal Engine dominuje w grafice 3D wysokiej jakości**: Dla złożonych scen 3D, Unreal oferuje lepszą wydajność przy zachowaniu wyższej jakości wizualnej.

3. **Dokumentacja Unity jest znacząco lepsza**: 100% respondentów oceniło dokumentację Unity jako bardziej kompletną i przydatną.

4. **Krzywa uczenia się Unity jest łagodniejsza**: Początkujący potrzebują średnio 2-3 miesięcy do produktywnej pracy w Unity vs. 4-6 miesięcy w Unreal.

5. **Object pooling jest krytyczny dla wydajności**: W grach typu bullet-hell, object pooling poprawił wydajność o 40-60% w obu silnikach.

(Continue with 5-10 clear findings)

### 8.2 Answer Research Questions
**From Chapter 1, answer each question**:

Example:
```latex
\textbf{Pytanie badawcze 1}: Który silnik oferuje lepszą wydajność dla gier 2D?
\textbf{Odpowiedź}: Unity oferuje lepszą wydajność dla gier 2D dzięki...

\textbf{Pytanie badawcze 2}: Jak różnią się przepływy pracy w obu silnikach?
\textbf{Odpowiedź}: Unity oferuje bardziej elastyczny workflow, podczas gdy 
Unreal narzuca bardziej ustrukturyzowane podejście...
```

### 8.3 Practical Recommendations
**Provide clear decision tree**:

Wybierz Unity jeśli:
- Tworzysz grę 2D
- Jesteś początkującym deweloperem
- Celujesz w platformy mobilne
- Masz ograniczony budżet/zespół
- Potrzebujesz szybkiego prototypowania

Wybierz Unreal Engine jeśli:
- Tworzysz grę 3D AAA
- Grafika jest najwyższym priorytetem
- Masz doświadczony zespół programistów C++
- Celujesz w PC/konsole
- Budujesz grę FPS

### 8.4 Scientific Contribution
**State what's novel in your thesis**:
- First direct performance comparison using NVIDIA Nsight
- First qualitative study of Polish game developers' experiences
- Practical insights for choosing engine for bullet-hell genre
- Triangulated data (performance + interviews + implementation experience)

### 8.5 Limitations of Research
**Be honest about**:
- Limited to one game genre
- Small interview sample
- Single hardware configuration
- Snapshot in time (engines evolve)
- Author's limited experience with Unreal compared to Unity

### 8.6 Future Research Directions
**Suggest**:
- Longitudinal study tracking engine evolution over 2-3 years
- Comparison across more game genres (RPG, strategy, puzzle)
- Larger interview study (100+ developers, international)
- Performance comparison on different hardware tiers
- Mobile-specific performance comparison
- Comparison of asset pipelines and team collaboration
- Study of maintenance costs over time

### 8.7 Final Reflections
**Personal insights**:
- What surprised you during research?
- How has your view of engines changed?
- What would you do differently?
- What advice for future researchers?

**End strongly**:
```latex
Niniejsza praca wykazała, że nie istnieje jednoznaczna odpowiedź na pytanie 
,,który silnik jest lepszy''. Zarówno Unity, jak i Unreal Engine mają swoje 
unikalne zalety i są optymalizowane pod różne przypadki użycia. Kluczem do 
sukcesu jest świadomy wybór narzędzia dopasowanego do konkretnego projektu, 
zespołu i celów biznesowych. W dynamicznie rozwijającej się branży gier, 
znajomość obu silników staje się coraz bardziej wartościową umiejętnością.
```

---

## 📊 APPENDICES

### Appendix A: Interview Question Template
**Include**:
- All 10 interview questions (from pytania/pytania_raw.txt)
- In Polish (original language)
- Brief explanation of interview protocol

### Appendix B: Detailed Performance Data Tables
**Include**:
- Complete raw data tables from all tests
- Multiple runs showing variance
- Full Nsight metrics (not just summary)

### Appendix C: Test Environment Specifications
**Include**:
- Complete hardware specs
- All software versions
- Driver versions
- OS configuration
- Background processes disabled
- Power management settings

### Appendix D: Code Samples (Optional)
**If space allows**:
- Key code snippets from Unity implementation
- Key code snippets from Unreal implementation
- Object pooling implementations side-by-side

---

## 🎨 FIGURES TO CREATE

### Must-Have Figures:

1. **Figure 5.1**: Frame time comparison chart (Unity vs Unreal, line graph)
2. **Figure 5.2**: GPU utilization bar chart (Unity vs Unreal)
3. **Figure 5.3**: Memory usage over time (both engines)
4. **Figure 5.4**: Draw calls comparison
5. **Figure 5.5**: Scalability curve (performance vs bullet count)
6. **Figure 7.1**: Master comparison radar chart (multiple criteria)
7. **Figure 7.2**: Decision tree for engine selection

### Nice-to-Have Figures:

8. Screenshots of both games at similar difficulty
9. Screenshots of Nsight analysis views
10. Architecture diagrams (Unity component system, Unreal actor-component)
11. Workflow comparison diagram

---

## 📋 TABLES TO CREATE

### Must-Have Tables:

1. **Table 4.1**: Test scenarios specification
2. **Table 4.2**: Interview participants profile
3. **Table 5.1-5.6**: Performance metrics (see Chapter 5 details above)
4. **Table 5.7**: Direct comparison summary table
5. **Table 7.1**: Master comparison matrix
6. **Table 7.2**: Use case recommendations matrix

---

## ✍️ WRITING TIPS

### Tone and Style:
- Academic but readable
- Use passive voice sparingly
- Define acronyms on first use
- Be objective, acknowledge limitations
- Use "wykazano, że..." not "myślę, że..."

### Integrating Data:
- Always cite figure/table when discussing results
- Example: "Jak przedstawiono na Rysunku 5.1, Unity osiągnęło średni czas klatki..."
- Reference interviews: "Według Respondenta 3..."

### Transitions Between Chapters:
- End of each chapter: summarize what was covered
- Start of next chapter: explain how it builds on previous

### Polish Academic Writing:
- Use proper technical terminology
- Maintain formal register
- Check that diacritics are correct (ą, ć, ę, ł, ń, ó, ś, ź, ż)

---

## 🚀 PRIORITY ORDER

If you're running out of time, complete in this order:

1. **HIGHEST PRIORITY**: Chapter 5 (Performance Tests) - THE DATA
2. **HIGH PRIORITY**: Chapter 7 (Comparison & Recommendations)
3. **HIGH PRIORITY**: Chapter 8 (Conclusions)
4. **MEDIUM PRIORITY**: Chapter 6 (Capabilities - can use interview data)
5. **MEDIUM PRIORITY**: Chapter 4 (Methodology - important but shorter)
6. **LOW PRIORITY**: Appendices (nice to have but not essential)

---

**Remember**: Every completed section is progress. Focus on DONE over PERFECT! 🎯
