# NuPoSe: Predicting Nucleosome positioning and identifying the related features

<p align='justify'> 
NuPoSe is a deep-learning framework that predicts nucleosome positioning and identifies related features. Figure 1 illustrates NuPoSe's framework, which comprises four main steps.
</p><br>

![NuPoSe](https://github.com/MasoudiYosef/NuPoSe/assets/83264279/73dd3cd5-7a70-4d45-8b58-1047fb2c4296)
<p align='center'>Figure 1: The framework of NuPoSe</p><br>

<p align='justify'>
In the first step (Figure 1a), high-coverage data of paired-end 147 bp length MNase-seq fragments from seven human lymphoblastoid cell lines (GSE36979) were aligned to the human reference genome (GRCh37). Subsequently, the alignment scores were smoothed, and the dyad positions were determined. The file named <i>DyadMNase.zip</i> contains all the necessary files and bash-format commands, which can be executed on the Ubuntu operating system. Using the determined dyad positions, two groups of DNAs were generated: the positive group representing 201-bases nucleosomal DNA and the negative group representing 201-bases non-nucleosomal DNA.
</p>


<p align='justify'>
In the second step (Figure 1b), a total of 336 di-nucleotide, tri-nucleotide, and tetra-nucleotide sequence patterns were defined for each DNA strand in the positive and negative datasets. Subsequently, five groups of features were extracted for each sequence pattern. The python-format file named FeatureExtraction.py contains the source code for extracting these features. To execute this source code, the following commands were used:
  <br><br>
<b>python3 FeatureExtraction.py PG<br>
python3 FeatureExtraction.py NG</b>
  <br><br>
Here, 'PG' and 'NG' refer to two text files containing 201-base nucleosomal and non-nucleosomal DNAs, respectively. Running these source codes converts every 201-base DNA sequence into a set of over 32,000 features.
</p>

<p align='justify'>
In the third step (Figure 1c), the extracted features underwent a two-step feature selection process: (i) Calculating Pearson correlation coefficients between features to remove redundant ones and (ii) Generating 100 subsets of nucleosome positioning features based on a combination of the <i>Trader</i>i> optimization algorithm and the SVM classifier. The python-format file named <i>Trader.py</i>i> contains the source code for this feature selection process. Running the following command will initiate the feature selection process as described.<br><br>
  <b>python3 Trader.py</b><br><br>
</p>

<p align='justify'>
In the final step (Figure 1d), each of the subsets of features generated in the previous step is analyzed using a ResNet-based deep neural network. The related source codes are based on the Keras deep learning package and can be executed using the following command:<br><br>
  <b>python3 Res.py</b><br><br>
  Here <i>Res.py</i> is a python-format file available in the current repository.
</p>

<p align='justify'>
We have also included a standalone version of the nucleosome positioning classification model (<b>NuPoSe</b>) in this repository. To use NuPoSe, please download the <i>NuPoSe.zip</i> file to one of your computer directories. After extracting the contents, run the following command: <br><br>
<b>python3 NuPoSe.py</b><br><br>
Please note that you should save your dataset as <i>DS.txt</i>, where each row of this plain text file represents a 201-base sequence. Running the above command will generate a text file named <i>SC</i>, with the number of rows equal to the number of sequences in the input file. In other words, the <i>SC</i> file will contain the prediction scores for each sequence in the input file. Additionally, you will need <b>numpy</b> and <b>Keras 2.7.0</b> libraries to run <b>NuPoSe</b>.
</p>
