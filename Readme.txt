Link to Download Third Party Libraries and Dataset:
https://www.dropbox.com/sh/6pbwqb4cr0b8q7o/AADyhvIh6ppLl4EuZAUx6QVma?dl=0
1. 'Annotated Posts' contains the annotated posts. One file for each post.
2. 'Data' corresponds to the posts extracted from StackOverflow for purpose of this assignment.
3. 'stanford' corresponds to the third party library used for CRF Classifier.

System Requirements:
1. Windows 7 or higher
2. Python 2.7
3. JAVA SE Runtime Environment 8
4. JAVAHOME must be set to the java directory cont in system environment variables

Installation:
1. nltk is required for this project. Before proceeding further, see the below section which explains how to install nltk.
2. Download the stanford, Annotated Posts, Data directory from the link mentioned above.
3. Extract the folders in the project directory.
4. Run 'TestNER.py' to train and test the model.

NOTE: Do not change the name of any directory.
NOTE: The program might take long to run as it iterates k-1 times for each value of k in range 2 to 10. To change the value, open TestNER.py and change the relevant part inside kcrossValidation().

Installing NLTK:
1. Run the followinf command in cmd, 'pip install nltk'.
2. Open python console.
3. Run the command download.nltk()
4. A NLTK Downloader UI will popup.
5. Download All Packages.

Output:
1. The generated test files for each iteration can be found under 'TestFiles' directory.
2. The generated result files (predictions by the trained model) for each iteration can be found under 'Results' directory.
3. The generated files for error analysis in terms of Precision, Recall, F1 etc.  for each iteration can be found under 'Scores' directory.

File Naming Convention (Output by the Program):
The files under 'TestFiles', 'Scores', 'Results' directory follow the following naming convention - test_kfold_(k)_iter_(i).tsv, score_kfold_(k)_iter_(i).txt, result_kfold_(k)_iter_(i).tsv, for TestFiles, Scores and Results respectively, where, k corresponds to the k value of k fold and i corresponds to the ith iteration for k fold cross validation.

ScoreFile:
The score files in Scores directory shows the results of prediction as shown below:
	Entity	P	R	F1	TP	FP	FN
            API	0.3556	0.4399	0.3933	304	551	387
         Totals	0.3556	0.4399	0.3933	304	551	387
Here, P is Precision, R is Recall, F1 is F-Measure, TP is number of True Positives, FP is number of False Positives and FN is number of False Negatives.

ResultFile:
The result files in Results directory has information regarding the tokens, their expected output and the predicted output. A sample is shown as below:

		I	O	O
		have	O	O
		tried	O	O
		SetForeground	B-API	B-API
		(	I-API	I-API
		)	I-API	I-API
		but	O	O
		it	O	O

The output in each line corresponds to the token, expected output, predicted output respectively.
