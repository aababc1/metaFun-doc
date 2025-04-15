(COMPARATIVE_ANNOTATION_description)=

# <span style="color:#7FBDFF">COMPARATIVE_ANNOTATION</span>

<img src="../../_static/metafun5_sky.png" style="height:200px; width:auto; float:right; margin-left:10px;" />
이 모듈은 메타게놈 어셈블 게놈(MAG)의 비교 유전체 분석 및 기능 주석을 위해 설계된 metaFun 파이프라인의 일부입니다.

## 개요
COMPARATIVE_ANNOTATION 모듈은 게놈 기능의 포괄적인 분석과 서로 다른 샘플이나 조건 간의 비교를 제공합니다. 이 모듈은 팬게놈 분석, 유전자의 기능 주석을 수행하고, 비교 유전체학을 위한a 시각화를 생성합니다. 핵심, 보조 및 고유 유전자를 식별하고, KEGG, VFDB, CARD, CAZymes, eggNOG 등 다양한 기능 데이터베이스로 이들을 주석 처리합니다.

**이 모듈의 주요 출력물은 통합 시퀀스 데이터베이스(HDF5 형식)**으로, INTERACTIVE_COMPARATIVE 모듈에서 대화형 탐색의 기반이 됩니다. 이 데이터베이스는 모든 주석, 유전자 서열 및 메타데이터를 연결하여 강력한 온디맨드 분석 및 시각화를 가능하게 합니다.

## 모듈 실행

```{code-block} bash
# 주석만 포함한 기본 사용법(권장)
(metafun) metafun -module COMPARATIVE_ANNOTATION -i genomes/ -m metadata.csv --samplecol 1

# 시각화가 포함된 대사 경로 분석 포함(정적 플롯을 생성하려는 경우)
(metafun) metafun -module COMPARATIVE_ANNOTATION -i genomes/ -m metadata.csv --samplecol 1 --metacol 2

# 특정 분석을 위한 매개변수 사용자 지정
(metafun) metafun -module COMPARATIVE_ANNOTATION -i genomes/ -m metadata.csv --samplecol 1 --pan_identity 0.8 --pan_coverage 0.8
```

:::{admonition} 권장 워크플로우
:class: tip

더 나은 성능과 유연성을 위해 두 단계 접근 방식을 권장합니다:
1. 먼저 주석만 포함한 COMPARATIVE_ANNOTATION 실행(--samplecol만 지정하고 --metacol은 지정하지 않음)
2. 그런 다음 `metafun -module INTERACTIVE_COMPARATIVE -i results/path`를 사용하여 결과를 대화식으로 탐색

이 접근 방식은 유용하지 않을 수 있는 대량의 정적 플롯 생성을 방지하고, **대화형 모듈**은 데이터의 더 동적인 탐색을 가능하게 합니다.
:::

## 모듈 작동 순서

이 모듈은 다음 단계를 수행합니다:

1. **게놈 준비**: 입력 게놈 및 메타데이터 처리
2. **유전자 예측**: Prokka를 사용하여 각 게놈의 유전자 예측
3. **팬게놈 분석**: PPanGGOLiN을 사용하여 핵심 및 보조 유전자 식별
4. **기능 주석**:
   - KofamScan을 사용한 KEGG 직교 주석
   - VFDB를 사용한 독성 인자 감지
   - CARD를 사용한 항생제 내성 유전자 식별
   - dbCAN을 사용한 탄수화물 활성 효소 주석
   - eggNOG-mapper를 사용한 단백질 기능 예측
5. **비교 분석**:
   - skani를 사용한 게놈 유사성 계산
   - dRep를 사용한 게놈 중복 제거
   - 유전자 존재/부재 클러스터링 및 시각화
6. **시퀀스 데이터베이스 생성**: 모든 주석, 시퀀스 및 메타데이터를 연결하는 통합 HDF5 데이터베이스 구축(INTERACTIVE_COMPARATIVE에 중요)
7. **시각화**: 모든 주석에 대한 대화형 플롯 및 히트맵 생성
8. **통계 분석**: Scoary2를 사용한 유전자-특성 연관성 분석

## 매개변수
**`${launchDir}`은 metaFun을 실행하는 디렉토리로, 출력 기본 디렉토리로 활용됩니다.** 

| 매개변수 | 설명 | 기본값 | 참고 |
|-----------|-------------|---------------|------|
| `-i, --inputDir` | 게놈 파일이 포함된 입력 디렉토리 | `${launchDir}/results/metagenome/BIN_ASSESSMENT/bins_quality_passed` | genome_selector_result.csv 출력 게놈을 사용할 수도 있음 |
| `-m, --metadata` | 메타데이터 파일 경로 | 필수 | 샘플 정보가 있는 CSV 또는 TSV 파일 |
| `--samplecol` | 샘플 식별자가 있는 메타데이터의 열 | 필수 | 게놈 파일 이름의 샘플 ID와 일치 |
| `--metacol` | 통계 분석을 위한 메타데이터의 열 | 선택 사항 | 지정하지 않으면 주석만 수행됨 |
| `-p, --processors` | 사용할 CPU 수 | `40` | 시스템 능력에 따라 조정 |
| `--module_completeness` | KEGG 모듈 완전성 임계값 | `0.5` | 모듈이 완전하다고 간주하는 데 필요한 KO의 분수 |
| `--pan_identity` | PPanGGOLiN 동일성 임계값 | `0.8` | 유전자 클러스터링을 위한 시퀀스 동일성 |
| `--pan_coverage` | PPanGGOLiN 커버리지 임계값 | `0.8` | 유전자 클러스터링을 위한 시퀀스 커버리지 |
| `--kingdom` | 주석을 위한 왕국 | `bacteria` | 옵션: bacteria, archaea |
| `--kofamscan_eval` | KEGG KO e-값 임계값 | `0.00001` | KofamScan 일치 임계값 |
| `--VFDB_identity` | VFDB 동일성 임계값 | `50` | 독성 인자의 백분율 동일성 |
| `--VFDB_coverage` | VFDB 커버리지 임계값 | `80` | 독성 인자의 백분율 커버리지 |
| `--VFDB_e_value` | VFDB e-값 임계값 | `1e-10` | 독성 인자의 E-값 임계값 |
| `--CAZyme_hmm_eval` | CAZyme HMM e-값 임계값 | `1e-15` | CAZyme 검출을 위한 E-값 임계값 |
| `--CAZyme_hmm_cov` | CAZyme HMM 커버리지 임계값 | `0.35` | CAZyme 검출을 위한 커버리지 임계값 |
| `--run_drep` | dRep 실행 여부 | `true` | 중복 제거를 건너뛰려면 false로 설정 |
| `--drep_ani` | dRep ANI 임계값 | `0.995` | 아종 수준 중복 제거를 위한 평균 뉴클레오타이드 동일성 임계값 |
| `--drep_cov` | dRep 커버리지 임계값 | `0.3` | 게놈 커버리지 임계값 |
| `--drep_algorithm` | dRep 알고리즘 | `skani` | ANI 계산을 위한 알고리즘 |


## **입력 및 출력**

### 입력
* 게놈 FASTA 파일(<span style="color:#00B050">BIN_ASSESSMENT</span>의 출력 폴더) 
* 샘플 정보 및 조건이 있는 메타데이터 파일(CSV 또는 TSV 형식)(<span style="color:#00B050">GENOME_</span><span style="color:#7FBDFF">SELECTOR</span>로 선택된 게놈 메타데이터)

### 출력
* 각 게놈에 대한 주석이 달린 유전자
* 팬게놈 분석 결과
* 기능 주석(KEGG, VFDB, CARD, CAZymes, eggNOG)
* 게놈 유사성 행렬 및 중복 제거 결과
* 비교 시각화(정적 및 대화형)
* 유전자-특성 연관성 결과
* **통합 시퀀스 데이터베이스(HDF5)** - INTERACTIVE_COMPARATIVE 모듈에 중요

### 출력 디렉토리 구조

출력은 `${launchDir}/results/metagenome/COMPARATIVE_ANNOTATION/` 아래의 타임스탬프가 있는 디렉토리에 정리됩니다:

```{code-block} bash
:caption: 출력 디렉토리 구조

${launchDir}/results/metagenome/COMPARATIVE_ANNOTATION/YYYYMMDDHHMMSS/
├── selected_genomes/                     # 처리된 입력 게놈
├── prokka/                               # Prokka 유전자 예측
│   ├── [genome1]/
│   │   ├── [genome1].ffn                 # 뉴클레오타이드 시퀀스
│   │   ├── [genome1].faa                 # 단백질 시퀀스
│   │   ├── [genome1].gff                 # 게놈 주석
│   │   └── ...
│   ├── [genome2]/
│   └── ...
├── ppanggolin_result/                    # 팬게놈 분석 결과
│   ├── pangenome.h5                      # 팬게놈 데이터베이스
│   ├── gene_presence_absence.Rtab        # 유전자 존재/부재 행렬
│   ├── gene_count_matrix.tsv             # 유전자 카운트 행렬
│   ├── gene_families.tsv                 # 유전자 패밀리 정보
│   └── ...
├── annotation_results/                   # 모든 도구의 주석 결과
│   ├── kofamscan/                        # KEGG 직교 주석
│   │   ├── ko_matrix.csv                 # KO 존재/부재 행렬
│   │   └── KO_definition_GeneID_countgenomes.csv # KO 정의
│   ├── VFDB/                             # 독성 인자 주석
│   │   ├── pangene_vfdb_result.txt       # 원시 VFDB 결과
│   │   ├── gene_PA_VFDB_added.csv        # 독성 인자 존재/부재
│   │   └── gene_count_VFDB_added.csv     # 독성 인자 카운트
│   ├── CARD/                             # 항생제 내성 주석
│   │   ├── pangene_rgi_CARD_result.txt   # 원시 RGI 결과
│   │   ├── gene_PA_CARD_added.csv        # ARG 존재/부재
│   │   └── gene_count_CARD_added.csv     # ARG 카운트
│   ├── dbCAN/                            # CAZyme 주석
│   │   ├── db_can_out/                   # 원시 dbCAN 결과
│   │   ├── dbcan_HMMER_count_gene_PA_matrix.csv    # CAZyme 존재/부재
│   │   ├── dbcan_HMMER_count_gene_count_matrix.csv # CAZyme 카운트
│   │   └── ...
│   ├── ani/                              # 게놈 유사성 분석
│   │   ├── skani_fullmatrix             # 게놈 유사성 행렬
│   │   └── skani_ANI_dist.tsv           # ANI 거리 행렬
│   └── eggNOG/                           # 단백질 기능 주석
│   │   ├── eggnog_mmseqs.emapper.annotations       # eggNOG 주석
│   │   └── ...
├── visualization_results/                # 생성된 플롯 및 그림
│   ├── kofamscan/                        # KEGG 시각화
│   │   ├── column_*/                     # 메타데이터 열별 시각화
│   │   ├── KEGG_module_visualization_shiny/  # 대화형 KEGG 시각화
│   │   └── KEGG_module_completeness.csv  # 모듈 완전성 데이터
│   ├── VFDB/                             # 독성 인자 시각화
│   │   ├── heatmap_VFDB_gene_PA_*.pdf    # 정적 VFDB 히트맵
│   │   └── VFDB_interactive_*/          # 대화형 VFDB 시각화
│   ├── CARD/                             # 항생제 내성 시각화
│   │   ├── heatmap_CARD_gene_PA_*.pdf    # 정적 CARD 히트맵
│   │   └── CARD_interactive_*/          # 대화형 CARD 시각화
│   ├── dbCAN/                            # CAZyme 시각화
│   │   ├── heatmap_dbCAN_gene_PA_*.pdf   # 정적 dbCAN 히트맵
│   │   └── dbCAN_interactive_*/         # 대화형 dbCAN 시각화
│   ├── defensefinder/                    # 방어 시스템 시각화
│   │   ├── heatmap_defensefinder_*.pdf   # 정적 방어 시스템 히트맵
│   │   └── defensefinder_interactive_*/  # 대화형 방어 시스템 시각화
│   ├── ani/                              # 게놈 유사성 시각화
│   │   ├── column_*/                     # 메타데이터 열별 시각화
│   │   ├── heatmap_skani.pdf             # 정적 skani 히트맵
│   │   └── skani_interactive/           # 대화형 skani 시각화
│   └── scoary2/                          # 유전자-특성 연관성 결과
│       └── scoary_out/                   # Scoary 출력 파일
├── genePA_cluster/                       # 유전자 존재/부재 클러스터링
│   └── pcoa_plot_interactive.html        # 유전자 존재/부재의 PCoA 플롯
├── drep/                                 # 게놈 중복 제거 결과
│   ├── drep_output/                      # dRep 출력 파일
│   ├── dereplicated_genomes/            # 중복 제거된 게놈 파일
│   └── subspecies_clusters.tsv          # 아종 클러스터 정보
└── sequence_db/                          # 시퀀스 데이터베이스
    └── sequences.h5                      # 시퀀스의 HDF5 데이터베이스
```

## 실행 예제 및 결과

### metaFun 명령줄 실행 예제


```{figure} ../../images/COMPARATIVE_ANNOTATION_command.png
---
width: 100%
figclass: margin-caption
alt: metafun_pipeline
name: COMPARATIVE_ANNOTATION_command
align: middle
---
```

:::{admonition} 결과의 대화형 시각화
:class: note

COMPARATIVE_ANNOTATION을 실행한 후, 다음을 사용하여 결과를 대화식으로 탐색할 수 있습니다:

```bash
metafun -module INTERACTIVE_COMPARATIVE -i ${launchDir}/results/metagenome/COMPARATIVE_ANNOTATION/YYYYMMDDHHMMSS
```

이는 주석 탐색, 게놈 비교 및 사용자 정의 시각화 생성을 위한 대화형 인터페이스를 실행합니다.
:::

### 시각화 예제

이 모듈은 다음과 같은 다양한 시각화를 생성합니다:

- 기능 프로필의 PCA 플롯
- 유전자 존재/부재의 히트맵
- 게놈의 계층적 클러스터링
- 기능 풍부도 플롯
- 게놈 유사성 네트워크

<iframe src="../../_static/pcoa_plot_interactive.html" width="100%" height="800px%"></iframe>



## <span style="color:#7FBDFF">COMPARATIVE_ANNOTATION</span> 모듈의 주요 프로세스

| 프로세스 | 목적 | 입력 | 출력 |
|---------|---------|-------|--------|
| `prepare_genomes` | 분석을 위한 게놈 준비 | 메타데이터 파일, 입력 게놈 디렉토리 | 선택된 게놈 파일 |
| `create_metadata_summary` | 메타데이터 정보 생성 | 메타데이터 파일 | 열 요약 파일 |
| `run_prokka` | 유전자 예측 | 게놈 FASTA 파일 | 예측된 유전자 및 단백질 |
| `run_ppanggolin` | 팬게놈 분석 | Prokka 출력 | 핵심 및 보조 유전자 |
| `run_panaroo` | 대체 팬게놈 분석 | Prokka 출력 | 팬게놈 결과 |
| `run_genePA_cluster` | 유전자 존재/부재 클러스터링 | 팬게놈, 메타데이터 | PCoA 시각화 |
| `run_kofamscan_annotation` | KEGG 주석 | 단백질 시퀀스 | KO 주석 |
| `run_kofamscan_visualization` | KEGG 시각화 | KO 행렬, 메타데이터 | 대화형 KEGG 시각화 |
| `run_VFDB_annotation` | 독성 인자 주석 | 단백질 시퀀스 | 독성 인자 식별 |
| `run_VFDB_visualization` | 독성 인자 시각화 | VFDB 결과, 메타데이터 | VFDB 히트맵 및 대화형 플롯 |
| `run_rgi_CARD_annotation` | 항생제 내성 주석 | 단백질 시퀀스 | 내성 유전자 식별 |
| `run_rgi_CARD_visualization` | 내성 유전자 시각화 | CARD 결과, 메타데이터 | CARD 히트맵 및 대화형 플롯 |
| `run_defensefinder_annotation` | 방어 시스템 분석 | 단백질 시퀀스 | 방어 시스템 식별 |
| `run_defensefinder_visualization` | 방어 시스템 시각화 | Defense finder 결과, 메타데이터 | 방어 시스템 히트맵 |
| `run_dbCAN_annotation` | CAZyme 주석 | 단백질 시퀀스 | 탄수화물 활성 효소 주석 |
| `run_dbCAN_visualization` | CAZyme 시각화 | dbCAN 결과, 메타데이터 | CAZyme 히트맵 및 대화형 플롯 |
| `run_skani_annotation` | 게놈 유사성 계산 | 게놈 FASTA 파일 | ANI 유사성 행렬 |
| `run_skani_visualization` | 게놈 유사성 시각화 | Skani 행렬, 메타데이터 | ANI 히트맵 |
| `run_eggNOG` | 단백질 기능 예측 | 단백질 시퀀스 | 상세 기능 주석 |
| `run_scoary2` | 유전자-특성 연관성 | 유전자 행렬, 메타데이터 | 통계적으로 유의한 연관성 |
</rewritten_file>
