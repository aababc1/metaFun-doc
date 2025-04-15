(ASSEMBLY_BINNING_description)=

# <span style="color:#FF9300">ASSEMBLY_BINNING</span>

<img src="../../_static/metafun2_orange.png" style="height:200px; width:auto; float:right; margin-left:10px;" />
이 모듈은 메타게놈 데이터의 de novo 어셈블리, 빈닝 및 빈 정제를 위해 설계된 metaFun 파이프라인의 일부입니다.

## 개요
ASSEMBLY_BINNING 모듈은 *de novo* 어셈블리와 빈닝 및 정제 과정을 위한 모듈입니다. 이 모듈은 품질 제어된 메타게놈 리드의 de novo 어셈블리를 수행한 후, 메타게놈 빈닝을 통해 정제 과정을 거친 메타게놈 어셈블 게놈(MAG)을 복원합니다.

## 모듈 실행

```{code-block} bash
# 기본 사용법
(metafun) metafun -module ASSEMBLY_BINNING

# RAWREAD_QC에서 사용자 정의 출력 경로를 사용한 경우 입력 디렉토리 지정
(metafun) metafun -module ASSEMBLY_BINNING -i /path/to/filtered_reads

# MEGAHIT 어셈블리 매개변수 변경
(metafun) metafun -module ASSEMBLY_BINNING --megahit_presets meta-large

# 자체 학습 모드에서 SemiBin2 사용 (입력 데이터에서 특성 학습, 더 오래 걸림)
(metafun) metafun -module ASSEMBLY_BINNING --semibin2_mode self

# SemiBin2에 특정 환경 모델 사용 (여러 환경 모델 사용 가능)
# 'human_gut','dog_gut','ocean','soil','cat_gut','human_oral','mouse_gut','pig_gut','built_environment','wastewater','chicken_caecum','global'
(metafun) metafun -module ASSEMBLY_BINNING --semibin2_mode human_gut
```

:::{admonition} 어셈블리 및 빈닝 옵션
:class: note

어셈블리 및 빈닝 프로세스를 최적화하기 위한 여러 옵션이 있습니다:
모든 옵션을 한 명령줄에 지정할 수 있습니다.

**MEGAHIT 어셈블리 프리셋:**
- 기본값은 대부분의 메타게놈에 균형이 맞는 `default`로 설정되어 있습니다.
- 토양과 같은 크고 복잡한 메타게놈의 경우 `--megahit_presets meta-large` 사용:
```{code-block} bash
:caption: 복잡한 메타게놈에 meta-large 프리셋 사용

(metafun) metafun -module ASSEMBLY_BINNING --megahit_presets meta-large
```
- 더 민감하지만 느린 어셈블리의 경우 `--megahit_presets meta-sensitive` 사용:
```{code-block} bash
:caption: 더 높은 민감도를 위해 meta-sensitive 프리셋 사용

(metafun) metafun -module ASSEMBLY_BINNING --megahit_presets meta-sensitive
```

**SemiBin2 환경 모델:**
- 기본값은 `self`(참조 모델 없이 자체 감독 학습)로 설정되어 있습니다.
- 참조 데이터가 없는 새로운 환경의 경우 자체 감독 모드 사용:
```{code-block} bash
:caption: 새로운 환경에 자체 감독 모드 사용

(metafun) metafun -module ASSEMBLY_BINNING --semibin2_mode self
```
- 특정 환경의 경우 사용 가능한 모델 중에서 선택:
```{code-block} bash
:caption: 환경별 모델 사용

# 인간 마이크로바이옴
(metafun) metafun -module ASSEMBLY_BINNING --semibin2_mode human_gut
(metafun) metafun -module ASSEMBLY_BINNING --semibin2_mode human_oral

# 동물 마이크로바이옴
(metafun) metafun -module ASSEMBLY_BINNING --semibin2_mode dog_gut
(metafun) metafun -module ASSEMBLY_BINNING --semibin2_mode cat_gut
(metafun) metafun -module ASSEMBLY_BINNING --semibin2_mode mouse_gut
(metafun) metafun -module ASSEMBLY_BINNING --semibin2_mode pig_gut
(metafun) metafun -module ASSEMBLY_BINNING --semibin2_mode chicken_caecum

# 환경 샘플
(metafun) metafun -module ASSEMBLY_BINNING --semibin2_mode ocean
(metafun) metafun -module ASSEMBLY_BINNING --semibin2_mode soil
(metafun) metafun -module ASSEMBLY_BINNING --semibin2_mode wastewater
(metafun) metafun -module ASSEMBLY_BINNING --semibin2_mode built_environment

# 범용 모델
(metafun) metafun -module ASSEMBLY_BINNING --semibin2_mode global
```
:::

## 모듈 작동 순서

이 모듈은 다음 단계를 수행합니다:

1. MEGAHIT를 사용한 *De novo* 어셈블리
2. 일관된 형식을 위한 컨티그 이름 변경
3. 어셈블된 컨티그에 대한 Bowtie2 인덱스 구축
4. 컨티그에 메타게놈 리드 매핑
5. MetaBAT2 및 SemiBin2를 사용한 메타게놈 빈닝
6. DAS Tool을 사용한 빈 정제

## 매개변수
**`${launchDir}`은 metaFun을 실행하는 디렉토리로, 출력 기본 디렉토리로 활용됩니다.**

| 매개변수 | 설명 | 기본값 | 참고 |
|-----------|-------------|---------------|------|
| `-i, --inputDir` | 필터링된 리드가 있는 입력 디렉토리 | `${launchDir}/results/metagenome/RAWREAD_QC/read_filtered` | <span style="color:#FF0000">RAWREAD_QC</span> 모듈의 출력 또는 품질 필터링된 리드가 포함된 자체 디렉토리를 지정합니다. <span style="color:#FF0000">RAWREAD_QC</span> 모듈에서 출력 디렉토리를 지정하지 않은 경우 입력 디렉토리 없이 실행할 수 있습니다. |
| `-o, --outdir` | 출력 디렉토리 | `${launchDir}/results/metagenome/ASSEMBLY_BINNING` | 다운스트림 분석을 위해 기본값 권장 |
| `--megahit_presets` | MEGAHIT 어셈블리 프리셋 | `default` | 옵션: `default`, `meta-large`, `meta-sensitive` |
| `--semibin2_mode` | SemiBin2 환경 모델 | `self` | 옵션: `self`, `human_gut`, `dog_gut`, `ocean`, `soil` 등 |
| `-p, --processors` | 사용할 CPU 수 | `8` | |

## **입력 및 출력**

### 입력
* 품질 제어된 페어드 엔드 메타게놈 리드(<span style="color:#FF0000">RAWREAD_QC</span> 워크플로우에서)
* 이 리드는 호스트 필터링 및 품질 트리밍이 되어 있어야 함
* 기본 입력 디렉토리: `${launchDir}/results/metagenome/RAWREAD_QC/read_filtered`

(ASSEMBLY_BINNING_output)=

### 출력
* 어셈블된 컨티그(FASTA 형식)
* 여러 빈닝 방법으로부터의 메타게놈 어셈블 게놈(MAG):
  * MetaBAT2 빈
  * SemiBin2 빈
  * MetaBAT2와 SemiBin2를 사용한 DAS Tool 정제 빈
* 관련 매핑 파일 및 중간 결과(Nextflow의 작업 디렉토리에서 확인 가능)

### 출력 디렉토리 구조

출력 디렉토리는 ${launchDir}/results/metagenome/ASSEMBLY_BINNING 또는 `-o outdir`로 지정한 디렉토리 경로에 있습니다.

```{admonition} 입력 및 출력 디렉토리 전환
:class: note

`-o ${output directory}`로 사용자 정의 출력 디렉토리를 정의하는 경우, 다운스트림 워크플로우에서 입력 매개변수를 적절히 수정해야 합니다.
기본 출력 디렉토리는 ${launchDir}의 `results/metagenome/ASSEMBLY_BINNING`입니다.
```

```{code-block} bash
:caption: 출력 디렉토리 구조

${launchDir}/results/metagenome/ASSEMBLY_BINNING/
├── assembled_contigs/                # MEGAHIT 어셈블리 결과
│   ├── results/
│   │   ├── assembly/
│   │   │   ├── ${sample_id}/
│   │   │   │   ├── ${sample_id}_renamed_MH.contigs.fa  # 어셈블되고 이름이 변경된 컨티그
│   ├── ...
├── metabat2_bins/                    # MetaBAT2 빈닝 결과
│   ├── ${sample_id}_MB2.1.fa         # 개별 MetaBAT2 빈
│   ├── ${sample_id}_MB2.2.fa
│   ├── ${sample_id}_MB2.3.fa
│   ├── ...
├── semibin2_bins/                    # SemiBin2 빈닝 결과
│   ├── ${sample_id}_${mode}_SB2_0.fa     # 개별 SemiBin2 빈
│   │                                  # 여기서 ${mode}는 선택한 환경 모델임(예: self, human_gut)
│   ├── ${sample_id}_${mode}_SB2_1.fa
│   ├── ${sample_id}_${mode}_SB2_2.fa
│   ├── ...
├── dastool_bins/                     # DAS Tool 정제 빈
│   ├── ${sample_id}_dastool_DASTool_bins/
│   │   ├── ${sample_id}_*.fa      # DAS Tool 정제 빈
│   │   ├── ...
│   ├── ...
└── final_bins/                       # 다운스트림 분석을 위한 모든 빈의 최종 모음
    ├── ${sample_id}_*.fa         # 모든 방법에서 최상의 빈 복사본
    ├── ...
```

## 실행 예제 및 결과

### metaFun 명령줄 실행 예제

```{figure} ../../images/ASSEMBLY_BINNING_command.png
---
width: 100%
figclass: margin-caption
alt: metafun_pipeline
name: ASSEMBLY_BINNING_command
align: middle
---
```


::::{admonition} SemiBin2 출력 파일 이름 지정에 대해
:class: note

SemiBin2 출력 파일 이름은 다음 패턴을 따릅니다: `${sample_id}_${mode}_SB2_${number}.fa`

- `${sample_id}`: 입력 리드의 샘플 식별자
- `${mode}`: `--semibin2_mode`로 선택한 SemiBin2 환경 모델
  - 예: `self`, `human_gut`, `ocean` 등
- `${number}`: 순차적 빈 번호

예: `SRR6915091_human_gut_SB2_14.fa`
::::
**assembled_contigs 폴더의 어셈블리와 final_bins 디렉토리의 게놈이 이 모듈의 주요 출력 파일입니다.**

생성된 빈의 품질은 <span style="color:#00B050">BIN_ASSESSMENT</span> 모듈에서 평가할 수 있습니다.

## <span style="color:#FF9300">ASSEMBLY_BINNING</span> 모듈의 Nextflow 프로세스

| 프로세스 | InputDir | OutputDir | 참고 |
|---------|----------|-----------|------|
| AssemblyAndRename | `${params.inputDir}` | `${params.outdir}/assembled_contigs` | MEGAHIT 어셈블리 및 컨티그 이름 변경 |
| Bowtie2IndexBuild | AssemblyAndRename의 출력 | 중간 결과 | 컨티그에 대한 Bowtie2 인덱스 구축 |
| MHcontig2sortedbam | 리드 및 Bowtie2 인덱스 | 중간 결과 | 컨티그에 리드를 매핑하고 정렬된 BAM 생성 |
| MB2_binning | 정렬된 BAM 및 컨티그 | `${params.outdir}/metabat2_bins` | MetaBAT2 빈닝 |
| SB2_binning | 정렬된 BAM 및 컨티그 | `${params.outdir}/semibin2_bins` | SemiBin2 빈닝 |
| Contigs2bin_prep_mb2 | MetaBAT2 빈 | 중간 결과 | DAS Tool을 위한 MetaBAT2 빈 정보 준비 |
| Contigs2bin_prep_sb2 | SemiBin2 빈 | 중간 결과 | DAS Tool을 위한 SemiBin2 빈 정보 준비 |
| Dastool | MetaBAT2 및 SemiBin2 빈 정보, 컨티그 | `${params.outdir}/dastool_bins` | DAS Tool 빈 정제 |
| get_bins | DAS Tool의 모든 빈 | `${params.outdir}/final_bins` | 다운스트림 분석을 위한 모든 빈 수집 |

## <span style="color:#FF9300">ASSEMBLY_BINNING</span> 워크플로우의 프로세스 설명

1. **AssemblyAndRename**: MEGAHIT를 사용하여 de novo 어셈블리를 수행하고 일관된 형식을 위해 컨티그 이름을 변경합니다. `assembled_contigs/results/assembly/${sample_id}/${sample_id}_renamed_MH.contigs.fa`에 출력을 생성합니다.

2. **Bowtie2IndexBuild**: 리드 매핑을 용이하게 하기 위해 어셈블된 컨티그에 대한 Bowtie2 인덱스를 구축합니다. 매핑 단계에서 사용되는 `${sample_id}_MH_bt2_index.*.bt2` 이름의 인덱스 파일을 생성합니다.

3. **MHcontig2sortedbam**: Bowtie2를 사용하여 컨티그에 리드를 매핑하고 빈닝을 위한 정렬된 BAM 파일을 생성합니다. 두 빈닝 방법 모두에 필요한 `${sample_id}_sorted.bam` 및 `${sample_id}_sorted.bam.bai` 파일을 생성합니다.

4. **MB2_binning**: MetaBAT2를 사용하여 메타게놈 빈닝을 수행합니다. 이는 커버리지와 시퀀스 구성을 기반으로 컨티그를 빈닝합니다. `${sample_id}_MB2.${number}.fa` 명명 패턴으로 빈을 생성합니다.

5. **SB2_binning**: SemiBin2를 사용하여 메타게놈 빈닝을 수행합니다. 이는 딥 러닝을 사용하여 빈닝합니다. `${sample_id}_${mode}_SB2_${number}.fa` 명명 패턴으로 빈을 생성합니다. 여기서 `${mode}`는 선택한 환경 모델입니다.

6. **Contigs2bin_prep_mb2** 및 **Contigs2bin_prep_sb2**: DAS Tool 통합을 위한 컨티그-빈 파일을 준비합니다. 이 프로세스는 DAS Tool이 필요로 하는 컨티그와 빈 사이의 매핑 파일을 생성합니다.

7. **Dastool**: 두 빈닝 방법에서 빈을 정제하고 통합하여 더 높은 품질의 MAG를 생성합니다. `${sample_id}_dastool_DASTool_bins/` 디렉토리에 정제된 빈을 출력합니다.

8. **get_bins**: 모든 생성된 빈을 수집하여 다운스트림 분석에 쉽게 접근할 수 있도록 `final_bins/` 디렉토리에 배치합니다. 이 디렉토리는 <span style="color:#00B050">BIN_ASSESSMENT</span> 모듈의 주요 입력으로 사용됩니다.

## <span style="color:#FF9300">ASSEMBLY_BINNING</span>에서 사용되는 도구

| 도구 | 목적 | 버전 | 기본 매개변수 | 선택할 수 있는 매개변수 |
|------|---------|---------|---------------------|--------------------------------|
| MEGAHIT | De novo 어셈블리 | 1.2.9 | `megahit_presets`에 따라 다양 | `--presets ${params.megahit_presets}` |
| Bowtie2 | 리드 매핑 | 2.5.2 | `--sensitive` | 이 스크립트에 지정되지 않음 |
| MetaBAT2 | 메타게놈 빈닝 | 2.15 | `-m 1500` | 이 스크립트에 지정되지 않음 |
| SemiBin2 | 메타게놈 빈닝 | 2.1.0 | 미리 훈련된 인간 장내 모델을 사용한 `single_easy_bin` 모드 | `--semibin2_mode ${mode}` | 
| DAS Tool | 빈 정제 | 1.1.7 | `--score_threshold=0` | 이 스크립트에 지정되지 않음 |

## 사용 참고 사항

- 스크립트는 진행하기 전에 입력 디렉토리의 존재 및 비어 있지 않음을 확인합니다.
- SemiBin2는 `--semibin2_mode ${mode}`를 설정하여 자체 감독 모드 또는 사전 제작된 환경 모델과 함께 실행할 수 있습니다:
  - 참조 게놈이 없는 새로운 환경의 경우 `self` 사용
  - 사용 가능한 환경 모델: `human_gut`, `dog_gut`, `ocean`, `soil`, `cat_gut`, `human_oral`, `mouse_gut`, `pig_gut`, `built_environment`, `wastewater`, `chicken_caecum`, `global`
- 복잡한 메타게놈의 경우 더 나은 어셈블리를 위해 `--megahit_presets meta-large` 사용 고려
- 민감한 어셈블리(더 많은 계산이 필요)의 경우 `--megahit_presets meta-sensitive` 사용
- **<span style="color:#FF9300">ASSEMBLY_BINNING</span>** 워크플로우는 <span style="color:#FF0000">RAWREAD_QC</span> 워크플로우의 출력과 함께 작동하도록 설계되었습니다.
- 결과 빈은 <span style="color:#00B050">BIN_ASSESSMENT</span> 모듈에서 품질 및 분류학적 분류에 대해 평가할 수 있습니다.

## 다음 단계

이 모듈로 MAG를 생성한 후, <span style="color:#00B050">BIN_ASSESSMENT</span>로 진행하여:
- CheckM2 및 GUNC를 사용한 게놈 품질 평가
- GTDB-Tk를 사용한 분류 분류
- 품질 지표에 따른 빈 필터링
- 다운스트림 분석을 위한 메타데이터와 결과 결합
