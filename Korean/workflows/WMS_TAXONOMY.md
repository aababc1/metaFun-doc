# <span style="color:#0846FA">WMS_TAXONOMY</span>

<img src="../../_static/metafun6_ocean.png" style="height:200px; width:auto; float:right; margin-left:10px;" />
이 모듈은 Kraken2, Bracken 및 Sylph를 사용하여 전장 메타게놈 시퀀싱 데이터의 분류학적 분석을 위해 설계된 metaFun 파이프라인의 일부입니다.

## 개요
WMS_TAXONOMY 모듈은 전장 메타게놈 시퀀싱 데이터로부터 분류학적 분류 및 풍부도 추정을 수행합니다. 이 모듈은 k-mer 매칭에 기반한 빠른 분류학적 분류를 위한 Kraken2, 종 수준에서 개선된 풍부도 추정을 위한 Bracken, 그리고 선택적으로 초고속 분류학적 프로파일링을 위한 Sylph를 활용합니다. 이 모듈은 분류학적 프로필을 샘플 메타데이터와 통합하여 다운스트림 통계 분석 및 시각화를 위한 Phyloseq 객체를 생성합니다.

## 모듈 실행

```{code-block} bash
# Sylph를 사용한 기본 사용법(기본 프로파일러)
(metafun) metafun -module WMS_TAXONOMY -i results/metagenome/RAWREAD_QC/read_filtered -m metadata.csv --sampleIDcolumn 1

# Sylph 대신 Kraken2/Bracken 사용
(metafun) metafun -module WMS_TAXONOMY -i results/metagenome/RAWREAD_QC/read_filtered -m metadata.csv --sampleIDcolumn 1 --profiler kraken2

# 메타데이터 열에 기반한 통계 분석 포함
(metafun) metafun -module WMS_TAXONOMY -i results/metagenome/RAWREAD_QC/read_filtered -m metadata.csv --sampleIDcolumn 1 --analysiscolumn 2

# 짧은 인수 형식 사용
(metafun) metafun -module WMS_TAXONOMY -i results/metagenome/RAWREAD_QC/read_filtered -m metadata.csv -c 1 -a 2

# 개선된 Kraken2 성능을 위한 메모리 매핑 사용
(metafun) metafun -module WMS_TAXONOMY -i results/metagenome/RAWREAD_QC/read_filtered -m metadata.csv --sampleIDcolumn 1 --profiler kraken2 --kraken_method memory-mapping
```

## 모듈 작동 순서

이 모듈은 다음 단계를 수행합니다:

1. **분류학적 분류** - Sylph(기본값) 또는 Kraken2 사용:
   - Sylph: 스케치를 생성하고 GTDB 데이터베이스에 대해 리드를 프로파일링
   - Kraken2: GTDB 데이터베이스를 사용하여 리드의 k-mer를 분류학적 레이블에 매핑
2. **풍부도 추정** - Bracken 사용(Kraken2 사용 시):
   - Kraken2 결과에서 종 수준 풍부도 추정 개선
   - 상대적 풍부도 임계값에 기반하여 결과 필터링
3. **Phyloseq 객체 생성**:
   - 분류학적 프로필과 메타데이터 결합
   - 통계 분석을 위한 R 호환 객체 생성
4. **통계 분석**(선택 사항):
   - 알파 다양성 분석
   - 베타 다양성 서열화
   - 차등 풍부도 테스트

## 매개변수
**`${launchDir}`은 metaFun을 실행하는 디렉토리로, 출력 기본 디렉토리로 활용됩니다.** 

| 매개변수 | 설명 | 기본값 | 참고 |
|-----------|-------------|---------------|------|
| `-i, --inputDir` | 필터링된 리드가 포함된 입력 디렉토리 | `"${launchDir}/results/metagenome/RAWREAD_QC/read_filtered"` | **필수**. <span style="color:#FF0000">RAWREAD_QC</span> 워크플로우의 출력 |
| `-m, --metadata` | 메타데이터 파일 경로 | 없음 | **필수**. 샘플 정보가 포함된 CSV 파일 |
| `-c, --sampleIDcolumn` | 메타데이터의 샘플 ID 열 번호 | `1` | **필수**. 리드 파일 이름의 샘플 ID와 일치 |
| `-a, --analysiscolumn` | 분석 그룹화를 위한 열 번호 | `0` | 선택 사항. 0으로 설정하면 통계 분석이 수행되지 않음 |
| `--profiler` | 사용할 분류학적 프로파일러 | `sylph` | 선택 사항. 옵션: `sylph`, `kraken2` |
| `--kraken_method` | Kraken2 방법 | `default` | 선택 사항. 옵션: `default`, `memory-mapping` |
| `--confidence_filter` | Kraken2의 신뢰도 임계값 | `0.1` | 선택 사항. 값이 높을수록 더 구체적인 분류 |
| `--relab_filter` | Bracken 결과의 상대적 풍부도 필터 | `0.0001` | 선택 사항. 이 임계값 미만의 종을 필터링 |
| `--sylph_abundance_type` | Sylph 출력의 풍부도 유형 | `relative_abundance` | 선택 사항. 보고할 풍부도 값의 유형 |
| `-p, --cpus` | 사용할 CPU 수 | `15` | 선택 사항. 시스템 기능에 따라 조정 |
| `-o, --outdir` | 출력 디렉토리 | `"${launchDir}/results/metagenome/WMS_TAXONOMY"` | 선택 사항. 결과가 저장될 위치 |

## **입력 및 출력**

### 입력
* 품질 제어된 페어드 엔드 메타게놈 리드(<span style="color:#FF0000">RAWREAD_QC</span> 워크플로우의 출력)
* 샘플 정보와 조건이 포함된 메타데이터 파일(CSV 형식)

### 출력
* Kraken2 분류 보고서
* Bracken 풍부도 추정치(Kraken2 사용 시)
* Sylph 프로파일링 결과(Sylph 사용 시)
* 통계 분석을 위한 Phyloseq 객체(RDS 파일)
* 통계 분석 결과 및 시각화(--analysiscolumn이 지정된 경우)

### 출력 디렉토리 구조

출력은 다음 디렉토리 구조로 구성됩니다:

```{code-block} bash
:caption: 출력 디렉토리 구조

${launchDir}/results/metagenome/WMS_TAXONOMY/
├── kraken2/                          # Kraken2 분류 결과
│   ├── ${sample_id}_kraken2.report    # 각 샘플에 대한 분류 보고서
│   └── ...
├── bracken/                          # Bracken 풍부도 추정 결과
│   ├── ${sample_id}_bracken.out       # 각 샘플에 대한 풍부도 추정치
│   └── ...
├── sylph/                            # Sylph 프로파일링 결과(선택한 경우)
│   ├── ${sample_id}.paired.sylsp      # 각 샘플에 대한 Sylph 스케치
│   ├── all.profile-sylph.tsv         # 결합된 Sylph 프로필
│   ├── merged_sylph_species.tsv      # 병합된 종 풍부도 테이블
│   └── ...
├── phyloseq/                         # Phyloseq 객체
│   ├── phyloseq_object.RDS           # Kraken2/Bracken 결과용(사용한 경우)
│   ├── phyloseq_object_sylph.RDS     # Sylph 결과용
│   └── ...
└── stats_analysis/                   # 통계 분석 결과
    ├── alpha_diversity/              # 알파 다양성 측정 및 플롯
    ├── beta_diversity/               # 서열화 플롯 및 PERMANOVA 결과
    ├── differential_abundance/       # 차등 풍부도 테스트 결과
    └── ...
```

## 실행 예제 및 결과

### metaFun 명령줄 실행 예제

```{figure} ../../images/WMS_TAXONOMY_command.png
---
width: 100%
figclass: margin-caption
alt: metafun_pipeline
name: WMS_TAXONOMY_command
align: middle
---
```

### Kraken2 출력 예제

```{code-block} bash
:caption: Kraken2 보고서 출력 예제

$ head -n 10 ${launchDir}/results/metagenome/WMS_TAXONOMY/kraken2/SRR6915091_kraken2.report

100.00  3652288 3652288 U       0       unclassified
0.00    0       0       R       1       root
0.00    0       0       R1      131567  cellular organisms
0.00    0       0       D       2157    Archaea
0.00    0       0       D       2       Bacteria
0.00    0       0       P       1224    Pseudomonadota
0.00    0       0       C       28211   Alphaproteobacteria
0.00    0       0       O       356     Hyphomicrobiales
0.00    0       0       F       41294   Bradyrhizobiaceae
0.00    0       0       G       1073    Rhodopseudomonas
```

### Bracken 출력 예제

```{code-block} bash
:caption: Bracken 풍부도 출력 예제

$ head -n 10 ${launchDir}/results/metagenome/WMS_TAXONOMY/bracken/SRR6915091_bracken.out

name                                                            taxonomy_id     taxonomy_lvl     kraken_assigned_reads        added_reads     new_est_reads   fraction_total_reads
Bacteroides vulgatus                                            435590          S                62479                        3214            65693           0.01798
Faecalibacterium prausnitzii                                    853                S                41682                        2143            43825           0.01199
Prevotella copri                                                418267          S                38769                        1993            40762           0.01116
Bacteroides uniformis                                            820                S                23683                        1218            24901           0.00682
Blautia obeum                                                   40520           S                22395                        1151            23546           0.00644
Agathobacter rectale                                            39491           S                22009                        1131            23140           0.00633
Bacteroides dorei                                               338188          S                20912                        1075            21987           0.00602
Bacteroides stercoris                                           46506           S                20614                        1060            21674           0.00593
Clostridium bolteae                                             208479          S                18229                        937             19166           0.00525
```

## <span style="color:#0846FA">WMS_TAXONOMY</span> 모듈의 Nextflow 프로세스

| 프로세스 | InputDir | OutputDir | 참고 |
|---------|----------|-----------|------|
| kraken2_run | `${params.inputDir}` | `${params.outdir}/kraken2` | Kraken2를 사용한 분류학적 분류 수행 |
| bracken_run | kraken2_run의 출력 | `${params.outdir}/bracken` | Bracken을 사용한 풍부도 추정 |
| sylph_sketch_all | `${params.inputDir}` | `${params.outdir}/sylph` | 리드에서 Sylph 스케치 생성 |
| sylph_process_all | sylph_sketch_all의 출력 | `${params.outdir}/sylph` | Sylph 스케치를 처리하고 분류학적 프로필 생성 |
| phyloseq_creation | bracken_run의 출력 | `${params.outdir}/phyloseq` | Bracken 결과에서 Phyloseq 객체 생성 |
| phyloseq_creation_sylph | sylph_process_all의 출력 | `${params.outdir}/phyloseq` | Sylph 결과에서 Phyloseq 객체 생성 |
| statistical_analysis | phyloseq_creation 또는 phyloseq_creation_sylph의 출력 | `${params.outdir}/stats_analysis` | --analysiscolumn이 지정된 경우 통계 분석 수행 |

## <span style="color:#0846FA">WMS_TAXONOMY</span> 워크플로우의 프로세스 설명

1. **kraken2_run**: 메타게놈 리드를 k-mer 기반 분류학적 분류기인 Kraken2를 사용하여 분류합니다.
   - 입력: 페어드 엔드 품질 필터링된 메타게놈 리드
   - 출력: 각 샘플에 대한 Kraken2 분류 보고서
   - 분류학적 할당을 위해 GTDB 데이터베이스 사용
   - 성능 향상을 위해 메모리 매핑 사용 가능

2. **bracken_run**: Bracken을 사용하여 Kraken2 결과에서 종 풍부도를 추정합니다.
   - 입력: Kraken2 보고서
   - 출력: 각 샘플에 대한 Bracken 풍부도 추정치
   - Bracken 데이터베이스에 적합한 리드 길이 자동 결정
   - 상대적 풍부도 임계값에 기반하여 결과 필터링

3. **sylph_sketch_all**: Sylph를 사용하여 메타게놈 리드의 압축된 스케치를 생성합니다.
   - 입력: 페어드 엔드 품질 필터링된 메타게놈 리드
   - 출력: 각 샘플에 대한 Sylph 스케치(.sylsp 파일)
   - 분류학적 프로파일링을 위한 Kraken2의 빠른 대안

4. **sylph_process_all**: Sylph 스케치를 처리하여 분류학적 프로필을 생성합니다.
   - 입력: 모든 샘플의 Sylph 스케치
   - 출력: 결합된 Sylph 프로필 및 종 풍부도 테이블
   - 프로필을 분류학적 분석과 호환되는 형식으로 변환

5. **phyloseq_creation**: Bracken 결과에서 Phyloseq 객체를 생성합니다.
   - 입력: Bracken 풍부도 파일 및 메타데이터
   - 출력: RDS 형식의 Phyloseq 객체
   - R에서 분석을 위해 분류학적 및 샘플 메타데이터 통합

6. **phyloseq_creation_sylph**: Sylph 결과에서 Phyloseq 객체를 생성합니다.
   - 입력: 병합된 Sylph 종 풍부도 테이블 및 메타데이터
   - 출력: Sylph 결과를 위한 RDS 형식의 Phyloseq 객체
   - phyloseq_creation과 유사하지만 Sylph 특정 형식을 처리

7. **statistical_analysis**: 분류학적 프로필에 대한 통계 분석을 수행합니다.
   - 입력: Phyloseq 객체
   - 출력: 알파 다양성, 베타 다양성 및 차등 풍부도 결과
   - --analysiscolumn이 지정된 경우에만 실행

## <span style="color:#0846FA">WMS_TAXONOMY</span>에서 사용되는 도구

| 도구 | 목적 | 버전 | 기본 매개변수 | 선택할 수 있는 매개변수 |
|------|---------|---------|---------------------|--------------------------------|
| Kraken2 | 분류학적 분류 | 2.1.2 | `--confidence 0.1`, `--paired` | `--memory-mapping` |
| Bracken | 풍부도 추정 | 2.7 | `-l S` (종 수준) | `-r ${read_length}` |
| Sylph | 빠른 분류학적 프로파일링 | 0.6.1 | `-c 200` (압축 수준) | 이 워크플로우에 특정한 것 없음 |
| R (phyloseq) | 통계 분석 및 시각화 | 4.3.2 | N/A | N/A |

## 사용 참고 사항

- **<span style="color:#0846FA">WMS_TAXONOMY</span>** 모듈은 <span style="color:#FF0000">RAWREAD_QC</span> 모듈의 출력과 함께 작동하도록 설계되었습니다.
- 메타데이터 파일은 CSV 형식이어야 하며, 적어도 하나의 열에는 리드 파일 이름의 접두사와 일치하는 샘플 ID가 포함되어야 합니다.
- 대규모 데이터셋의 경우, `--kraken_method memory-mapping`을 사용하면 성능이 크게 향상될 수 있지만, 충분한 시스템 메모리가 필요합니다.
- 상대적 풍부도 필터(`--relab_filter`)를 조정하여 종 감지의 민감도를 제어할 수 있습니다 - 값이 낮을수록 희귀한 종이 포함됩니다.
- Sylph 프로파일러(`--profiler sylph`)는 Kraken2/Bracken보다 훨씬 빠른 분류학적 프로파일링을 제공하며, 대규모 데이터셋에 좋은 대안이 될 수 있습니다.
- 이 모듈에서 생성된 Phyloseq 객체는 사용자 정의 분석을 위해 다른 R 패키지와 함께 사용하거나 **<span style="color:#0846FA">INTERACTIVE_WMS_TAXONOMY</span>** 모듈과 함께 사용할 수 있습니다.
- **중요한 풍부도 추정 차이**: 이 모듈에 포함된 두 프로파일러는 근본적으로 다른 접근 방식을 사용합니다:
  - **Sylph**는 참조 시퀀스에 대한 전체 게놈 매칭을 기반으로 **분류학적 풍부도**를 추정하고, **Kraken2와 Bracken**은 개별 리드를 분류군에 할당하고 데이터베이스 편향을 조정하여 **시퀀스 풍부도**(리드 수)를 추정합니다([doi: 10.1038/s41592-021-01141-3](https://doi.org/10.1038/s41592-021-01141-3)).
  - 이러한 차이는 프로파일러 간 결과를 비교하거나 다른 분석 방법과 결합할 때 고려해야 합니다.

## 다음 단계

<span style="color:#0846FA">WMS_TAXONOMY</span>를 실행한 후, 다음과 같은 작업을 수행할 수 있습니다:

1. **<span style="color:#0846FA">INTERACTIVE_WMS_TAXONOMY</span>** 모듈을 사용하여 결과를 대화형으로 탐색:
   ```bash
   (metafun) metafun -module INTERACTIVE_WMS_TAXONOMY -i results/metagenome/WMS_TAXONOMY
   ```

   :::{admonition} 대화형 분석 유연성
   :class: tip

   **<span style="color:#0846FA">INTERACTIVE_WMS_TAXONOMY</span>** 모듈을 사용하면 다음과 같은 작업을 수행할 수 있습니다:
   - `-i` 매개변수를 사용하여 phyloseq 객체가 포함된 WMS_TAXONOMY 출력 디렉토리를 직접 가리킬 수 있습니다.
   - **WMS_TAXONOMY 실행에서 `--analysiscolumn`을 지정하지 않았더라도** 메타데이터 기반 분석을 수행할 수 있습니다.
   - 분류학적 분류를 다시 실행하지 않고도 분석을 위해 서로 다른 메타데이터 변수를 선택할 수 있습니다.
   - 데이터셋의 모든 메타데이터 변수에 걸쳐 분류학적 패턴을 대화형으로 시각화하고 테스트할 수 있습니다.
   :::
